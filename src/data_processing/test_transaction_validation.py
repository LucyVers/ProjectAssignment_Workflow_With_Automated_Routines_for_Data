"""
Simple test to validate transactions without database interaction.
"""
import pandas as pd
from pathlib import Path
from transaction_validator import TransactionValidator
import json
from collections import Counter

def test_transaction_validation():
    print("Starting transaction validation test...")
    
    # Initialize validator
    validator = TransactionValidator()
    
    try:
        # Load transactions
        print("\nLoading transactions.csv...")
        trans_path = "data/working/transactions.csv"
        if not Path(trans_path).exists():
            print(f"Error: Cannot find {trans_path}")
            return
            
        trans_df = pd.read_csv(trans_path)
        print(f"Loaded {len(trans_df)} transactions")
        
        # Test first 100 transactions
        print("\nValidating first 100 transactions:")
        
        # Statistics
        valid_count = 0
        invalid_count = 0
        error_types = Counter()
        
        for idx, row in trans_df.head(100).iterrows():
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
        print(f"Total transactions checked: {valid_count + invalid_count}")
        print(f"Valid transactions: {valid_count}")
        print(f"Invalid transactions: {invalid_count}")
        
        if error_types:
            print("\nError type breakdown:")
            for error, count in error_types.most_common():
                print(f"- {error}: {count} occurrences")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_transaction_validation() 