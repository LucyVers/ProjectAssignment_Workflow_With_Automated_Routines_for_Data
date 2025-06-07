"""
Simple test to just load and peek at the CSV files.
"""
import pandas as pd
import sys
from pathlib import Path

def test_load():
    print("Starting simple data load test...")
    
    # Print working directory
    print(f"Current working directory: {Path.cwd()}")
    
    try:
        # Try to load transactions
        print("\nTrying to load transactions.csv...")
        trans_path = "data/working/transactions.csv"
        if Path(trans_path).exists():
            print(f"Found {trans_path}")
            trans_df = pd.read_csv(trans_path)
            print("\nFirst 3 rows of transactions:")
            print(trans_df.head(3))
            print(f"\nTotal transactions: {len(trans_df)}")
        else:
            print(f"Error: Cannot find {trans_path}")
        
        # Try to load customers
        print("\nTrying to load sebank_customers_with_accounts.csv...")
        cust_path = "data/working/sebank_customers_with_accounts.csv"
        if Path(cust_path).exists():
            print(f"Found {cust_path}")
            cust_df = pd.read_csv(cust_path)
            print("\nFirst 3 rows of customers:")
            print(cust_df.head(3))
            print(f"\nTotal customers: {len(cust_df)}")
        else:
            print(f"Error: Cannot find {cust_path}")
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print(f"Python path: {sys.path}")

if __name__ == "__main__":
    test_load() 