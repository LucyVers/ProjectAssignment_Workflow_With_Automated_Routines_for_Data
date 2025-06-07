import pandas as pd
from src.data_processing.workflow import prepare_account_data

# Läs in CSV-filen
df = pd.read_csv('data/working/sebank_customers_with_accounts.csv')

# Förbered kontodatan
accounts_df = prepare_account_data(df)

# Visa information om resultatet
print('\nAntal konton att importera:', len(accounts_df))
print('\nExempel på första kontot:')
print(accounts_df.iloc[0]) 