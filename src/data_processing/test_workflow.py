"""
Test version of the workflow that processes only 100 records.
"""
from prefect import flow, task
import pandas as pd
from pathlib import Path
import logging

from transaction_validator import TransactionValidator
from data_validator import DataValidator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_workflow(
    transactions_path: str = "data/working/transactions.csv",
    customers_path: str = "data/working/sebank_customers_with_accounts.csv",
    sample_size: int = 100
):
    """
    Test workflow that processes only a sample of records.
    """
    logger.info(f"Starting test workflow with sample size: {sample_size}")
    
    try:
        # Load and sample data
        logger.info("Loading data...")
        transactions_df = pd.read_csv(transactions_path).head(sample_size)
        customers_df = pd.read_csv(customers_path).head(sample_size)
        logger.info(f"Loaded {len(transactions_df)} transactions and {len(customers_df)} customers")
        
        # Validate transactions
        logger.info("\nValidating transactions...")
        transaction_validator = TransactionValidator()
        transaction_results = []
        invalid_transactions = []
        
        for idx, row in transactions_df.iterrows():
            transaction = row.to_dict()
            errors = transaction_validator.validate_transaction(transaction)
            
            # Store results
            transaction_results.append({
                'valid': len(errors) == 0,
                'errors': errors,
                'transaction': transaction
            })
            
            if errors:
                invalid_transactions.append({
                    'idx': idx + 1,
                    'id': transaction['transaction_id'],
                    'amount': transaction['amount'],
                    'currency': transaction['currency'],
                    'type': transaction['transaction_type'],
                    'errors': errors
                })
        
        # Print invalid transactions first (if any)
        if invalid_transactions:
            print("\n=== INVALID TRANSACTIONS ===")
            for t in invalid_transactions:
                print(f"\nTransaction {t['idx']}:")
                print(f"ID: {t['id']}")
                print(f"Amount: {t['amount']} {t['currency']}")
                print(f"Type: {t['type']}")
                print("ERRORS:")
                for error in t['errors']:
                    print(f"  - {error}")
        
        # Validate customers
        logger.info("\nValidating customers...")
        customer_validator = DataValidator(customers_df)
        customer_results = customer_validator.validate_all()
        
        # Print customer validation summary
        print("\n=== CUSTOMER VALIDATION SUMMARY ===")
        print("\n1. Personnummer Issues:")
        pnr_results = customer_results['personnummer']
        print(f"- Invalid check digits: {len(pnr_results['invalid_check_digits'])}")
        if pnr_results['invalid_check_digits']:
            print("  Examples:", pnr_results['invalid_check_digits'][:3])
            
        print(f"- Invalid dates: {len(pnr_results['invalid_dates'])}")
        if pnr_results['invalid_dates']:
            print("  Examples:", pnr_results['invalid_dates'][:3])
            
        print(f"- Unreasonable ages: {len(pnr_results['unreasonable_ages'])}")
        if pnr_results['unreasonable_ages']:
            print("  Examples:", pnr_results['unreasonable_ages'][:3])
            
        print(f"- Duplicates: {len(pnr_results['duplicates'])}")
        if pnr_results['duplicates']:
            print("  Examples:", pnr_results['duplicates'][:3])
        
        print("\n2. Address Issues:")
        addr_results = customer_results['address']
        print(f"- Invalid format: {len(addr_results['invalid_format'])}")
        if addr_results['invalid_format']:
            print("  Examples:", addr_results['invalid_format'][:3])
            
        print(f"- Missing postal code: {len(addr_results['missing_postal_code'])}")
        if addr_results['missing_postal_code']:
            print("  Examples:", addr_results['missing_postal_code'][:3])
            
        print(f"- Missing city: {len(addr_results['missing_city'])}")
        if addr_results['missing_city']:
            print("  Examples:", addr_results['missing_city'][:3])
        
        print("\n3. Phone Number Issues:")
        phone_results = customer_results['phone']
        print(f"- Invalid numbers: {len(phone_results['invalid'])}")
        if phone_results['invalid']:
            print("  Examples:", phone_results['invalid'][:3])
        
        # Calculate overall statistics
        valid_transactions = sum(1 for r in transaction_results if r['valid'])
        
        print("\n=== OVERALL STATISTICS ===")
        print(f"Total transactions processed: {len(transactions_df)}")
        print(f"Valid transactions: {valid_transactions}")
        print(f"Invalid transactions: {len(transactions_df) - valid_transactions}")
        
        # Show summary of what would be exported
        print("\n=== EXPORT SUMMARY ===")
        print("Transaction amount ranges that would be exported:")
        valid_amounts = [r['transaction']['amount'] for r in transaction_results if r['valid']]
        if valid_amounts:
            print(f"- Minimum amount: {min(valid_amounts):.2f} SEK")
            print(f"- Maximum amount: {max(valid_amounts):.2f} SEK")
            print(f"- Average amount: {sum(valid_amounts)/len(valid_amounts):.2f} SEK")
        
        # Count transaction types
        valid_types = [r['transaction']['transaction_type'] for r in transaction_results if r['valid']]
        incoming = sum(1 for t in valid_types if t == 'incoming')
        outgoing = sum(1 for t in valid_types if t == 'outgoing')
        print(f"\nTransaction types to export:")
        print(f"- Incoming: {incoming}")
        print(f"- Outgoing: {outgoing}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_workflow() 