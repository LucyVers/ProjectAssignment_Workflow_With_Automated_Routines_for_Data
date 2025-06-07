"""
Test workflow for data validation without database export.
"""
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd
from typing import Tuple, Dict, List
import logging
from pathlib import Path

from src.data_processing.transaction_validator import TransactionValidator
from src.data_processing.data_validator import DataValidator
from src.utils.monitoring import monitor

logger = logging.getLogger(__name__)

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def load_data(transactions_path: str, customers_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load transaction and customer data from CSV files.
    """
    logger.info(f"Loading data from {transactions_path} and {customers_path}")
    transactions_df = pd.read_csv(transactions_path)
    customers_df = pd.read_csv(customers_path)
    logger.info(f"Loaded {len(transactions_df)} transactions and {len(customers_df)} customers")
    return transactions_df, customers_df

@task
def validate_transactions(transactions_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate transactions and split into valid and invalid.
    """
    logger.info("Starting transaction validation")
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
        if idx % 1000 == 0:  # Log every 1000 transactions
            logger.info(f"Processed {idx} transactions")
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
    logger.info("Starting customer validation")
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
        if idx % 100 == 0:  # Log every 100 customers
            logger.info(f"Processed {idx} customers")
        if errors:
            logger.warning(f"Customer {idx} errors: {errors}")
    
    # Create mask for valid/invalid customers
    valid_mask = [r['valid'] for r in results]
    
    # Split dataframe
    valid_customers = customers_df[valid_mask].copy()
    invalid_customers = customers_df[~pd.Series(valid_mask)].copy()
    
    # Log summary
    logger.info(f"Valid customers: {len(valid_customers)}")
    logger.info(f"Invalid customers: {len(invalid_customers)}")
    
    return valid_customers, invalid_customers

@task
def generate_report() -> Dict:
    """
    Generate validation and processing report.
    """
    return monitor.get_metrics_report()

@flow(name="data_validation_test_flow")
def validate_data(
    transactions_path: str = "data/working/transactions.csv",
    customers_path: str = "data/working/sebank_customers_with_accounts.csv"
) -> Dict:
    """
    Test workflow for data validation only (no database export).
    """
    logger.info("Starting data validation test workflow")
    
    # Load data
    transactions_df, customers_df = load_data(transactions_path, customers_path)
    
    # Validate both transactions and customers
    valid_transactions, invalid_transactions = validate_transactions(transactions_df)
    valid_customers, invalid_customers = validate_customers(customers_df)
    
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
        'validation_details': validation_report
    }
    
    logger.info(f"Validation test workflow completed. Report: {report}")
    return report

if __name__ == "__main__":
    validate_data() 