"""
Script to update transaction types in the transactions CSV file from incoming/outgoing to debit/credit.
"""
import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_transaction_types(input_file: str, output_file: str) -> None:
    """
    Update transaction types in the CSV file.
    """
    logger.info(f"Reading transactions from {input_file}")
    df = pd.read_csv(input_file)
    
    # Print column names
    logger.info(f"Columns in CSV: {df.columns.tolist()}")
    
    # Map old types to new types
    type_mapping = {
        'incoming': 'debit',   # Money coming in (positive amount)
        'outgoing': 'credit'   # Money going out (negative amount)
    }
    
    # Convert types
    old_types = df['transaction_type'].unique()  # Using correct column name
    logger.info(f"Found transaction types: {old_types}")
    
    df['transaction_type'] = df['transaction_type'].map(type_mapping)
    
    # Verify conversion
    new_types = df['transaction_type'].unique()
    logger.info(f"New transaction types: {new_types}")
    
    # Save updated file
    logger.info(f"Saving updated transactions to {output_file}")
    df.to_csv(output_file, index=False)
    logger.info("Done!")

if __name__ == "__main__":
    data_dir = Path("data/working")
    input_file = data_dir / "transactions.csv"
    output_file = data_dir / "transactions_updated.csv"
    
    update_transaction_types(str(input_file), str(output_file)) 