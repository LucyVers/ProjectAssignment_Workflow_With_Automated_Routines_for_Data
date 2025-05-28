-- Add foreign key constraints
ALTER TABLE accounts
    ADD CONSTRAINT fk_customer
    FOREIGN KEY (customer) REFERENCES customers(id),
    ADD CONSTRAINT fk_bank
    FOREIGN KEY (bank) REFERENCES banks(id);

ALTER TABLE transactions
    ADD CONSTRAINT fk_account
    FOREIGN KEY (account_nr) REFERENCES accounts(nr);

-- Add interest rates table
CREATE TABLE interest_rates (
    id serial PRIMARY KEY,
    account_type text NOT NULL,
    rate decimal(5,4) NOT NULL,
    valid_from timestamp NOT NULL DEFAULT now(),
    valid_to timestamp,
    created_by text NOT NULL
);

-- Add approval logs table
CREATE TABLE approval_logs (
    id serial PRIMARY KEY,
    approval_type text NOT NULL, -- 'loan', 'account', 'credit'
    approved_by text NOT NULL,   -- officer or manager id/name
    approved_at timestamp NOT NULL DEFAULT now(),
    customer_id int REFERENCES customers(id),
    account_nr text REFERENCES accounts(nr),
    amount decimal(15,2),        -- for loans and credits
    status text NOT NULL,        -- 'approved', 'rejected'
    reason text                  -- especially important for rejections
);

-- Add transaction monitoring table
CREATE TABLE transaction_monitoring (
    id serial PRIMARY KEY,
    transaction_id int REFERENCES transactions(id),
    monitored_at timestamp NOT NULL DEFAULT now(),
    risk_level text NOT NULL,    -- 'low', 'medium', 'high'
    flags text[],               -- array of warning flags
    reviewed_by text,           -- officer who reviewed the transaction
    review_status text,         -- 'pending', 'cleared', 'suspicious'
    notes text
);

-- Add audit log table
CREATE TABLE audit_logs (
    id serial PRIMARY KEY,
    action_time timestamp NOT NULL DEFAULT now(),
    user_id text NOT NULL,
    action_type text NOT NULL,
    table_name text NOT NULL,
    record_id text NOT NULL,
    old_values jsonb,
    new_values jsonb,
    ip_address text
);

-- Add indexes for performance
CREATE INDEX idx_transaction_account ON transactions(account_nr);
CREATE INDEX idx_transaction_time ON transactions(time);
CREATE INDEX idx_approval_type ON approval_logs(approval_type);
CREATE INDEX idx_approval_customer ON approval_logs(customer_id);
CREATE INDEX idx_monitoring_risk ON transaction_monitoring(risk_level);
CREATE INDEX idx_audit_action_time ON audit_logs(action_time);
CREATE INDEX idx_audit_user ON audit_logs(user_id);

-- Add comments for documentation
COMMENT ON TABLE interest_rates IS 'Stores historical interest rates for different account types';
COMMENT ON TABLE approval_logs IS 'Tracks all approval decisions by officers and managers';
COMMENT ON TABLE transaction_monitoring IS 'Stores transaction monitoring results and reviews';
COMMENT ON TABLE audit_logs IS 'Tracks all system changes for audit purposes'; 