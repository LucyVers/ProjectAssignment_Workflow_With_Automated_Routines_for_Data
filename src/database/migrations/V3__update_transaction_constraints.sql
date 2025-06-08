-- Remove existing unique constraint on transaction_id
ALTER TABLE transactions DROP CONSTRAINT IF EXISTS transactions_transaction_id_key;

-- Add compound unique constraint on transaction_id and transaction_type
ALTER TABLE transactions ADD CONSTRAINT transactions_transaction_id_type_key UNIQUE (transaction_id, transaction_type);
 
-- Update transaction_type column comment to reflect new values
COMMENT ON COLUMN transactions.transaction_type IS 'Type of transaction: debit or credit'; 