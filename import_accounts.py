from src.data_processing.workflow import import_accounts
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Run the account import workflow
result = import_accounts(
    customers_path="data/working/sebank_customers_with_accounts.csv",
    batch_size=100  # Mindre batch-storlek för säkrare import
)

# Skriv ut resultatet
print("\nImport Results:")
print("-" * 50)
for key, value in result.items():
    print(f"{key}: {value}") 