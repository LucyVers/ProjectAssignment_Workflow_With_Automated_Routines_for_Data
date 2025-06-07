"""
Automated workflow for data validation and processing using Prefect.
"""
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta, datetime
import pandas as pd
from typing import Tuple, Dict, List
import logging
from pathlib import Path
import math
import re

from src.data_processing.transaction_validator import TransactionValidator
from src.data_processing.data_validator import DataValidator
from src.utils.monitoring import monitor
from src.models.database_models import session_scope, Customer, Account, Transaction

logger = logging.getLogger(__name__)

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def load_data(transactions_path: str = None, customers_path: str = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load data from CSV files.
    """
    transactions_df = pd.DataFrame()  # Empty DataFrame as default
    customers_df = pd.DataFrame()     # Empty DataFrame as default
    
    if transactions_path:
    transactions_df = pd.read_csv(transactions_path)
        logger.info(f"Loaded {len(transactions_df)} transactions")
    
    if customers_path:
    customers_df = pd.read_csv(customers_path)
        logger.info(f"Loaded {len(customers_df)} customer records")
    
    return transactions_df, customers_df

@task
def validate_transactions(transactions_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate transactions and split into valid and invalid.
    """
    validator = TransactionValidator()
    validation_results = []
    
    for idx, row in transactions_df.iterrows():
        # Convert row to dict for validation
        transaction = row.to_dict()
        
        # Validate transaction
        errors = validator.validate_transaction(transaction)
        
        validation_results.append({
            'index': idx,
            'valid': len(errors) == 0,
            'errors': errors
        })
        
        # Log validation result
        logger.info(f"Transaction {idx}: {'Valid' if len(errors) == 0 else 'Invalid'}")
        if errors:
            logger.warning(f"Transaction {idx} errors: {errors}")
    
    # Create mask for valid/invalid transactions
    valid_mask = [r['valid'] for r in validation_results]
    
    # Split dataframe
    valid_transactions = transactions_df[valid_mask].copy()
    invalid_transactions = transactions_df[~pd.Series(valid_mask)].copy()
    
    # Log summary
    logger.info(f"Valid transactions: {len(valid_transactions)}")
    logger.info(f"Invalid transactions: {len(invalid_transactions)}")
    
    return valid_transactions, invalid_transactions

@task
def validate_customers(customers_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate customer data and split into valid and invalid.
    """
    # Initialize DataValidator with the customer data
    validator = DataValidator(customers_df)
    
    # Run all validations
    validation_results = validator.validate_all()
    
    # Create validation results list for each customer
    results = []
    for idx, row in customers_df.iterrows():
        # Check if this customer has any validation errors
        has_errors = False
        errors = []
        
        # Check personnummer validation
        pnr = row['Personnummer']
        if pnr in validation_results['personnummer'].get('invalid_check_digits', []):
            has_errors = True
            errors.append("Invalid personnummer check digit")
        if pnr in validation_results['personnummer'].get('invalid_dates', []):
            has_errors = True
            errors.append("Invalid personnummer date")
            
        # Check address validation
        address = row['Address']
        if address in validation_results['address'].get('invalid_format', []):
            has_errors = True
            errors.append("Invalid address format")
        if address in validation_results['address'].get('missing_postal_code', []):
            has_errors = True
            errors.append("Missing postal code")
            
        # Check phone validation
        phone = row['Phone']
        if phone in validation_results['phone'].get('invalid', []):
            has_errors = True
            errors.append("Invalid phone number format")
        
        results.append({
            'index': idx,
            'valid': not has_errors,
            'errors': errors
        })
        
        # Log validation result
        monitor.log_validation_result(
            validation_type='customer',
            passed=not has_errors,
            errors=errors
        )
    
    # Create mask for valid/invalid customers
    valid_mask = [r['valid'] for r in results]
    
    # Split dataframe
    valid_customers = customers_df[valid_mask].copy()
    invalid_customers = customers_df[~pd.Series(valid_mask)].copy()
    
    return valid_customers, invalid_customers

def process_batch(df: pd.DataFrame, table_name: str, session, batch_size: int, start_idx: int) -> bool:
    """
    Process a single batch of data.
    """
    end_idx = start_idx + batch_size
    batch = df.iloc[start_idx:end_idx]
    
    try:
        batch.to_sql(table_name, session.bind, if_exists='append', index=False)
        logger.info(f"Successfully exported batch {start_idx//batch_size + 1} to {table_name} "
                   f"(rows {start_idx} to {end_idx})")
        return True
    except Exception as e:
        logger.error(f"Failed to export batch {start_idx//batch_size + 1} to {table_name}: {str(e)}")
        return False

def format_phone_number(phone: str) -> str:
    """
    Format phone numbers to international format: +XX(Y)ZZZZ...
    where:
    - XX is country code (1-3 digits)
    - Y is area code (1-4 digits)
    - Z is the rest of the number
    
    Handles:
    1. Local Swedish numbers (0X-XXX XX XX -> +46(X)XXX XX XX)
    2. International numbers (keeps them as is, just reformats if needed)
    3. Numbers with or without spaces/dashes
    """
    if not phone or pd.isna(phone):
        return None
        
    # Remove all non-digit characters except + if it exists at the start
    has_plus = phone.startswith('+')
    digits = ''.join(filter(str.isdigit, phone))
    
    # Handle Swedish local format (starting with 0)
    if digits.startswith('0'):
        # For Swedish numbers, we know the exact format:
        # 0XX-XXX XX XX or 0XXX-XXX XX XX
        if len(digits) < 9:  # Too short for a Swedish number
            return None
            
        # Remove leading 0 and split into area code and main number
        digits = digits[1:]  # Remove leading 0
        if len(digits) == 10:  # 3-digit area code
            area_code = digits[:3]
            main_number = digits[3:]
        else:  # 2-digit area code
            area_code = digits[:2]
            main_number = digits[2:]
            
        return f"+46({area_code}){main_number}"
    
    # Handle international format
    elif has_plus:
        # First 1-3 digits are country code
        if len(digits) < 4:  # Need at least: 1 digit country code, 1 digit area code, 1 digit number
            return None
            
        # Try to determine country code length (usually 1-3 digits)
        if digits.startswith('1'):  # North America
            country_code = digits[:1]
            rest = digits[1:]
        elif digits.startswith('7'):  # Russia
            country_code = digits[:1]
            rest = digits[1:]
        elif digits[:3] in ['380', '381']:  # Some 3-digit country codes
            country_code = digits[:3]
            rest = digits[3:]
        else:  # Most European/Asian countries (2 digits)
            country_code = digits[:2]
            rest = digits[2:]
            
        # For international numbers, take first 2-3 digits as area code
        area_code = rest[:3]
        main_number = rest[3:]
        
        return f"+{country_code}({area_code}){main_number}"
    
    # If number doesn't start with + or 0, it's invalid
    return None

def prepare_customer_data(customers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare customer data for database import by mapping CSV columns to database columns
    and extracting address components.
    """
    # Create a copy to avoid modifying the original data
    db_ready_df = customers_df.copy()
    
    # Drop duplicates based on personnummer to get unique customers
    db_ready_df = db_ready_df.drop_duplicates(subset=['Personnummer'])
    
    # Extract address components using regex
    address_pattern = r'(.*?),\s*(\d{5})\s*(.*)'
    address_components = db_ready_df['Address'].str.extract(address_pattern)
    db_ready_df['address'] = address_components[0]
    db_ready_df['postal_code'] = address_components[1]
    db_ready_df['city'] = address_components[2]
    
    # Map columns to match database schema
    db_ready_df = db_ready_df.rename(columns={
        'Customer': 'name',  # Changed back to 'Customer' to match the actual CSV column name
        'Phone': 'phone',
        'Personnummer': 'personnummer'
    })
    
    # Format phone numbers
    db_ready_df['phone'] = db_ready_df['phone'].apply(format_phone_number)
    
    # Add guardian_info as NULL for adults
    db_ready_df['guardian_info'] = None
    
    # Add bank_id
    db_ready_df['bank_id'] = 1
    
    # Select only the columns we need in the exact order they appear in the database
    # Order from database: id, bank_id, personnummer, name, phone, address, city, postal_code, guardian_info
    # Note: id is auto-generated, so we exclude it
    return db_ready_df[['bank_id', 'personnummer', 'name', 'phone', 'address', 'city', 'postal_code', 'guardian_info']]

def prepare_account_data(customers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare account data for database import.
    """
    # Create a copy to avoid modifying the original data
    db_ready_df = customers_df.copy()
    
    # Use existing account numbers from BankAccount column
    db_ready_df['account_number'] = db_ready_df['BankAccount']
    
    # Add other required fields
    db_ready_df['type'] = 'checking'  # Default account type
    db_ready_df['created_at'] = pd.Timestamp.now()
    db_ready_df['bank_id'] = 1  # Add bank_id
    
    # Keep personnummer for mapping to customer_id later
    db_ready_df['personnummer'] = customers_df['Personnummer']
    
    # Select only the columns we need in the exact order they appear in the database
    # plus personnummer for mapping
    return db_ready_df[['account_number', 'type', 'created_at', 'bank_id', 'personnummer']]

def prepare_transaction_data(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare transaction data for database import
    """
    # Create a copy to avoid modifying the original data
    db_ready_df = transactions_df.copy()
    
    # Map columns to match database schema
    db_ready_df = db_ready_df.rename(columns={
        'TransactionID': 'transaction_id',
        'Amount': 'amount',
        'Currency': 'currency',
        'Timestamp': 'timestamp',
        'SenderCountry': 'sender_country',
        'SenderMunicipality': 'sender_municipality',
        'ReceiverCountry': 'receiver_country',
        'ReceiverMunicipality': 'receiver_municipality',
        'TransactionType': 'transaction_type'
    })
    
    # Convert old transaction types to new debit/credit system
    type_mapping = {
        'incoming': 'debit',   # Money coming in (positive amount)
        'outgoing': 'credit'   # Money going out (negative amount)
    }
    db_ready_df['transaction_type'] = db_ready_df['transaction_type'].map(type_mapping)
    
    # Ensure correct data types
    db_ready_df['transaction_id'] = db_ready_df['transaction_id'].astype(str)
    db_ready_df['sender_account'] = db_ready_df['sender_account'].astype(str)
    db_ready_df['receiver_account'] = db_ready_df['receiver_account'].astype(str)
    db_ready_df['amount'] = pd.to_numeric(db_ready_df['amount'], errors='coerce')
    db_ready_df['currency'] = db_ready_df['currency'].astype(str)
    db_ready_df['timestamp'] = pd.to_datetime(db_ready_df['timestamp'])
    db_ready_df['sender_country'] = db_ready_df['sender_country'].astype(str)
    db_ready_df['sender_municipality'] = db_ready_df['sender_municipality'].astype(str)
    db_ready_df['receiver_country'] = db_ready_df['receiver_country'].astype(str)
    db_ready_df['receiver_municipality'] = db_ready_df['receiver_municipality'].astype(str)
    db_ready_df['transaction_type'] = db_ready_df['transaction_type'].astype(str)
    
    # Handle missing values
    db_ready_df['notes'] = db_ready_df.get('notes', '').fillna('')
    
    return db_ready_df

@task
def export_to_database(valid_transactions: pd.DataFrame, valid_customers: pd.DataFrame, 
                      batch_size: int = 1000) -> bool:
    """
    Export validated data to database with batch processing support.
    """
    try:
        with session_scope() as session:
            # Prepare data for database import
            db_ready_customers = prepare_customer_data(valid_customers)
            db_ready_accounts = prepare_account_data(valid_customers)
            db_ready_transactions = prepare_transaction_data(valid_transactions)
            
            # Process customers first
            logger.info(f"Starting customer export in batches of {batch_size}")
            total_customer_batches = math.ceil(len(db_ready_customers) / batch_size)
            
            customer_id_map = {}
            
            for batch_num in range(total_customer_batches):
                start_idx = batch_num * batch_size
                end_idx = start_idx + batch_size
                customer_batch = db_ready_customers.iloc[start_idx:end_idx]
                
                for _, row in customer_batch.iterrows():
                    # Check if customer already exists
                    existing_customer = session.query(Customer).filter_by(personnummer=row['personnummer']).first()
                    
                    if existing_customer:
                        # Update existing customer
                        existing_customer.name = row['name']
                        existing_customer.address = row['address']
                        existing_customer.postal_code = row['postal_code']
                        existing_customer.city = row['city']
                        existing_customer.phone = row['phone']
                        existing_customer.bank_id = row['bank_id']
                        existing_customer.guardian_info = row['guardian_info']
                        customer_id_map[row['personnummer']] = existing_customer.id
                    else:
                        # Create new customer
                        customer = Customer(
                            name=row['name'],
                            address=row['address'],
                            postal_code=row['postal_code'],
                            city=row['city'],
                            phone=row['phone'],
                            personnummer=row['personnummer'],
                            bank_id=row['bank_id'],
                            guardian_info=row['guardian_info']
                        )
                        session.add(customer)
                        session.flush()  # Get the ID without committing
                        customer_id_map[row['personnummer']] = customer.id
                
                session.commit()
                logger.info(f"Processed customer batch {batch_num + 1}/{total_customer_batches}")
            
            # Process accounts next
            logger.info(f"Starting account export in batches of {batch_size}")
            total_account_batches = math.ceil(len(db_ready_accounts) / batch_size)
            
            account_number_map = {}  # To store account_number -> account_id mapping
            
            for batch_num in range(total_account_batches):
                start_idx = batch_num * batch_size
                end_idx = start_idx + batch_size
                account_batch = db_ready_accounts.iloc[start_idx:end_idx]
                
                for _, row in account_batch.iterrows():
                    customer_id = customer_id_map.get(row['personnummer'])
                    if customer_id:
                        # Check if account already exists
                        existing_account = session.query(Account).filter_by(account_number=row['account_number']).first()
                        
                        if existing_account:
                            # Update existing account
                            existing_account.customer_id = customer_id
                            existing_account.bank_id = row['bank_id']
                            existing_account.type = row['type']
                            account_number_map[row['account_number']] = existing_account.id
                        else:
                            # Create new account
                            account = Account(
                                account_number=row['account_number'],
                                customer_id=customer_id,
                                bank_id=row['bank_id'],
                                type=row['type'],
                                created_at=row['created_at']
                            )
                            session.add(account)
                            session.flush()  # Get the ID without committing
                            account_number_map[row['account_number']] = account.id
                
                session.commit()
                logger.info(f"Processed account batch {batch_num + 1}/{total_account_batches}")
            
            # Finally process transactions
            logger.info(f"Starting transaction export in batches of {batch_size}")
            total_transaction_batches = math.ceil(len(db_ready_transactions) / batch_size)
            
            for batch_num in range(total_transaction_batches):
                start_idx = batch_num * batch_size
                end_idx = start_idx + batch_size
                transaction_batch = db_ready_transactions.iloc[start_idx:end_idx]
                
                for _, row in transaction_batch.iterrows():
                    # Get account IDs from the mapping
                    sender_account_id = account_number_map.get(row['sender_account'])
                    receiver_account_id = account_number_map.get(row['receiver_account'])
                    
                    if sender_account_id and receiver_account_id:
                        # Create credit entry (money leaving sender's account)
                        credit_entry = Transaction(
                            transaction_id=row['transaction_id'],  # Same transaction_id for both entries
                            account_id=sender_account_id,
                            amount=-row['amount'],  # Negative for credit (money leaving)
                            currency=row['currency'],
                            transaction_type='credit',  # This entry is a credit
                            timestamp=row['timestamp'],
                            sender_country=row['sender_country'],
                            sender_municipality=row['sender_municipality'],
                            receiver_country=row['receiver_country'],
                            receiver_municipality=row['receiver_municipality'],
                            notes=row.get('notes')
                        )
                        session.add(credit_entry)

                        # Create debit entry (money entering receiver's account)
                        debit_entry = Transaction(
                            transaction_id=row['transaction_id'],  # Same transaction_id for both entries
                            account_id=receiver_account_id,
                            amount=row['amount'],  # Positive for debit (money entering)
                            currency=row['currency'],
                            transaction_type='debit',  # This entry is a debit
                            timestamp=row['timestamp'],
                            sender_country=row['sender_country'],
                            sender_municipality=row['sender_municipality'],
                            receiver_country=row['receiver_country'],
                            receiver_municipality=row['receiver_municipality'],
                            notes=row.get('notes')
                        )
                        session.add(debit_entry)
                
                session.commit()
                logger.info(f"Processed transaction batch {batch_num + 1}/{total_transaction_batches}")
            
        return True
            
    except Exception as e:
        logger.error(f"Failed to export data to database: {str(e)}")
        raise

@task
def generate_report() -> Dict:
    """
    Generate validation and processing report.
    """
    return monitor.get_metrics_report()

@flow(name="data_validation_flow")
def validate_and_load(
    transactions_path: str = "data/working/transactions.csv",
    customers_path: str = "data/working/sebank_customers_with_accounts.csv",
    batch_size: int = 500  # Changed default to 500 for safer initial testing
) -> Dict:
    """
    Main workflow for data validation and loading.
    """
    logger.info("Starting data validation workflow")
    
    # Load data
    transactions_df, customers_df = load_data(transactions_path, customers_path)
    logger.info(f"Loaded {len(transactions_df)} transactions and {len(customers_df)} customer records")
    
    # Validate both transactions and customers
    valid_transactions, invalid_transactions = validate_transactions(transactions_df)
    valid_customers, invalid_customers = validate_customers(customers_df)
    
    # Export valid data to database with batch processing
    export_success = export_to_database(
        valid_transactions, 
        valid_customers,
        batch_size=batch_size
    )
    
    # Generate validation report
    validation_report = generate_report()
    
    # Prepare final report
    report = {
        'total_transactions': len(transactions_df),
        'valid_transactions': len(valid_transactions),
        'invalid_transactions': len(invalid_transactions),
        'total_customers': len(customers_df),
        'valid_customers': len(valid_customers),
        'invalid_customers': len(invalid_customers),
        'database_export_success': export_success,
        'validation_details': validation_report
    }
    
    logger.info(f"Workflow completed. Report: {report}")
    return report

@task
def export_accounts_to_database(valid_customers: pd.DataFrame, batch_size: int = 1000) -> bool:
    """
    Export only account data to database with batch processing support.
    """
    try:
        with session_scope() as session:
            # Prepare account data
            db_ready_accounts = prepare_account_data(valid_customers)
            
            # Get existing customer IDs from database
            customer_id_map = {}
            for _, row in valid_customers.iterrows():
                customer = session.query(Customer).filter_by(personnummer=row['Personnummer']).first()
                if customer:
                    customer_id_map[row['Personnummer']] = customer.id
            
            # Process accounts
            logger.info(f"Starting account export in batches of {batch_size}")
            total_account_batches = math.ceil(len(db_ready_accounts) / batch_size)
            
            account_number_map = {}  # To store account_number -> account_id mapping
            
            for batch_num in range(total_account_batches):
                start_idx = batch_num * batch_size
                end_idx = start_idx + batch_size
                account_batch = db_ready_accounts.iloc[start_idx:end_idx]
                
                for _, row in account_batch.iterrows():
                    customer_id = customer_id_map.get(row['personnummer'])
                    if customer_id:
                        account = Account(
                            account_number=row['account_number'],
                            customer_id=customer_id,
                            bank_id=row['bank_id'],
                            type=row['type'],
                            created_at=row['created_at']
                        )
                        session.add(account)
                        session.flush()  # Get the ID without committing
                        account_number_map[row['account_number']] = account.id
                
                session.commit()
                logger.info(f"Processed account batch {batch_num + 1}/{total_account_batches}")
            
            return True
            
    except Exception as e:
        logger.error(f"Failed to export accounts to database: {str(e)}")
        raise

@flow(name="account_import_flow")
def import_accounts(
    customers_path: str = "data/working/sebank_customers_with_accounts.csv",
    batch_size: int = 500
) -> Dict:
    """
    Workflow specifically for importing accounts.
    """
    logger.info("Starting account import workflow")
    
    # Load only customer data (which contains account information)
    _, customers_df = load_data(customers_path=customers_path)
    logger.info(f"Loaded {len(customers_df)} customer records with account information")
    
    # Validate customers (we need this to get the valid customer data structure)
    valid_customers, invalid_customers = validate_customers(customers_df)
    
    # Export only accounts to database
    export_success = export_accounts_to_database(
        valid_customers,
        batch_size=batch_size
    )
    
    # Prepare final report
    report = {
        'total_customers_with_accounts': len(customers_df),
        'valid_customers': len(valid_customers),
        'invalid_customers': len(invalid_customers),
        'database_export_success': export_success
    }
    
    logger.info(f"Account import completed. Report: {report}")
    return report

if __name__ == "__main__":
    validate_and_load() 