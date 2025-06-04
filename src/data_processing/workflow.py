"""
Automated workflow for data validation and processing using Prefect.
"""
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd
from typing import Tuple, Dict, List
import logging
from pathlib import Path

from .transaction_validator import TransactionValidator
from ..utils.validators import validate_customer
from ..utils.monitoring import monitor
from ..models.database_models import session_scope

logger = logging.getLogger(__name__)

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def load_data(transactions_path: str, customers_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load transaction and customer data from CSV files.
    """
    transactions_df = pd.read_csv(transactions_path)
    customers_df = pd.read_csv(customers_path)
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
    validation_results = []
    
    for _, row in customers_df.iterrows():
        errors = validate_customer(row.to_dict())
        validation_results.append({
            'index': _,
            'valid': len(errors) == 0,
            'errors': errors
        })
        
        # Log validation result
        monitor.log_validation_result(
            validation_type='customer',
            passed=len(errors) == 0,
            errors=errors
        )
    
    # Create mask for valid/invalid customers
    valid_mask = [r['valid'] for r in validation_results]
    
    # Split dataframe
    valid_customers = customers_df[valid_mask].copy()
    invalid_customers = customers_df[~pd.Series(valid_mask)].copy()
    
    return valid_customers, invalid_customers

@task
def export_to_database(valid_transactions: pd.DataFrame, valid_customers: pd.DataFrame) -> bool:
    """
    Export validated data to database with transaction support.
    """
    try:
        with session_scope() as session:
            # Export customers first (due to foreign key constraints)
            valid_customers.to_sql('customers', session.bind, if_exists='append', index=False)
            valid_transactions.to_sql('transactions', session.bind, if_exists='append', index=False)
            logger.info("Successfully exported data to database")
        return True
    except Exception as e:
        logger.error(f"Database export failed: {str(e)}")
        return False

@task
def generate_report() -> Dict:
    """
    Generate validation and processing report.
    """
    return monitor.get_metrics_report()

@flow(name="data_validation_flow")
def validate_and_load(
    transactions_path: str = "../data/original/transactions.csv",
    customers_path: str = "../data/original/sebank_customers_with_accounts.csv"
) -> Dict:
    """
    Main workflow for data validation and loading.
    """
    logger.info("Starting data validation workflow")
    
    # Load data
    transactions_df, customers_df = load_data(transactions_path, customers_path)
    logger.info(f"Loaded {len(transactions_df)} transactions and {len(customers_df)} customer records")
    
    # Validate transactions
    valid_transactions, invalid_transactions = validate_transactions(transactions_df)
    
    # Export valid data to database
    export_success = export_to_database(valid_transactions, customers_df)
    
    # Prepare report
    report = {
        'total_transactions': len(transactions_df),
        'valid_transactions': len(valid_transactions),
        'invalid_transactions': len(invalid_transactions),
        'database_export_success': export_success
    }
    
    logger.info(f"Workflow completed. Report: {report}")
    return report

if __name__ == "__main__":
    validate_and_load() 