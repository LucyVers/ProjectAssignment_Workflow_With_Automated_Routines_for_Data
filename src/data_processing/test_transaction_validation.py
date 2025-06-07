"""
Simple test to validate transactions without database interaction.
"""
import pandas as pd
from pathlib import Path
from src.data_processing.transaction_validator import TransactionValidator
from src.models.database_models import Transaction, session_scope
from src.data_processing.workflow import validate_and_load, prepare_transaction_data
import json
from collections import Counter

def test_transaction_validation():
    print("Starting transaction validation test...")
    
    # Initialize validator
    validator = TransactionValidator()
    
    try:
        # Load transactions
        print("\nLoading transactions.csv...")
        trans_path = "data/working/transactions_updated.csv"  # Using updated file
        if not Path(trans_path).exists():
            print(f"Error: Cannot find {trans_path}")
            return
            
        trans_df = pd.read_csv(trans_path)
        print(f"Loaded {len(trans_df)} transactions")
        
        # Test first 10 transactions
        print("\nValidating first 10 transactions:")
        
        # Statistics
        valid_count = 0
        invalid_count = 0
        error_types = Counter()
        
        for idx, row in trans_df.head(10).iterrows():
            # Convert row to dict for validation
            transaction = row.to_dict()
            
            # Validate transaction
            errors = validator.validate_transaction(transaction)
            
            # Update statistics
            if errors:
                invalid_count += 1
                for error in errors:
                    error_types[error] += 1
            else:
                valid_count += 1
            
            # Print results
            print(f"\nTransaction {idx + 1}:")
            print(f"ID: {transaction['transaction_id']}")
            print(f"Amount: {transaction['amount']} {transaction['currency']}")
            print(f"Type: {transaction['transaction_type']}")
            if errors:
                print("ERRORS FOUND:")
                for error in errors:
                    print(f"  - {error}")
            else:
                print("Status: Valid")
        
        # Print summary
        print("\n=== VALIDATION SUMMARY ===")
        print(f"Total transactions tested: {valid_count + invalid_count}")
        print(f"Valid transactions: {valid_count}")
        print(f"Invalid transactions: {invalid_count}")
        
        if error_types:
            print("\nError type frequency:")
            for error, count in error_types.most_common():
                print(f"  {error}: {count}")
                
        # Now test database import with a small batch
        print("\n=== TESTING DATABASE IMPORT ===")
        result = validate_and_load(
            transactions_path=trans_path,
            batch_size=1
        )
        
        print("\nChecking database entries:")
        with session_scope() as session:
            transactions = session.query(Transaction).all()
            print(f"\nTotal transactions in database: {len(transactions)}")
            for t in transactions:
                print(f"\nTransaction {t.transaction_id}:")
                print(f"  Type: {t.transaction_type}")
                print(f"  Amount: {t.amount} {t.currency}")
                print(f"  Account: {t.account_id}")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    test_transaction_validation() 