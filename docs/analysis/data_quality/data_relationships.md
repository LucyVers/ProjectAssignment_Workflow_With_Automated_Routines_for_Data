# Data Relationships: Customers and Transactions

## Overview
This document analyzes the relationships between customer data (`sebank_customers_with_accounts.csv`) and transaction data (`transactions.csv`).

## Recent Updates
**Important**: Validation results from May 31, 2025 have identified significant relationship issues. See [Customer Data Analysis](customer_data_analysis.md) for full details.

Key relationship findings:
- Multiple accounts sharing same personnummer (419 cases)
- Potential identity verification issues (55 underage cases)
- Address relationship inconsistencies (postal code/city mismatches)

## Data Structure Analysis

### Customer Data Structure
1. Key Fields:
   - Customer Name
   - Personnummer (YYMMDD-XXXX)
   - Bank Account Numbers (SE8902XXXX...)
   
2. Relationships:
   - One customer can have multiple accounts
   - Each account is unique
   - Customer information is consistent across accounts

### Transaction Data Structure
1. Key Fields:
   - transaction_id (UUID format)
   - timestamp
   - amount
   - currency
   - sender_account (SE8902... format)
   - receiver_account (SE8902... format)
   - sender_country
   - sender_municipality
   - receiver_country
   - receiver_municipality
   - transaction_type
   - notes

2. Transaction Types:
   - incoming
   - outgoing

## Key Relationships

### Account Linkage
1. Primary Connection:
   - Customer accounts (from customer data) appear as sender_account or receiver_account in transactions
   - Account format consistent: SE8902... in both datasets

2. Transaction Flow:
   - Outgoing: Customer account as sender_account
   - Incoming: Customer account as receiver_account

### Data Validation Points
1. Account Format Consistency
   - Both datasets use SE8902 prefix
   - Account numbers are 20 characters after prefix
   - Format: SE8902XXXX[14 digits]

2. Geographic Information
   - Transactions include municipality data
   - Can be linked to customer addresses
   - Helps verify transaction legitimacy

3. Timeline Considerations
   - Transaction timestamps allow temporal analysis
   - Can track account activity over time

## Data Quality Considerations

### Validation Requirements
1. Account Validation
   - Verify all transaction accounts exist in customer database
   - Check for inactive or closed accounts
   - Validate account format consistency

2. Transaction Validation
   - Ensure transaction amounts are reasonable
   - Verify currency matches account type
   - Check geographic information consistency

3. Customer Information Validation
   - Verify customer details for all involved accounts
   - Check for suspicious patterns
   - Monitor transaction frequency

### Quality Metrics
1. Data Completeness
   - All required fields present
   - No missing relationships
   - Complete transaction information

2. Data Consistency
   - Account number formats match
   - Geographic information aligns
   - Customer details consistent
   - **NEW**: Additional consistency checks required for:
     - Personnummer uniqueness
     - Address component relationships
     - Phone number standardization

## Next Steps
1. Implement Validation Rules
   - Create account format validators
   - Set up transaction validators
   - Establish relationship checks
   - Create duplicate personnummer checks
   - Set up age verification
   - Establish address relationship validation

2. Create Monitoring System
   - Track transaction patterns
   - Monitor account activity
   - Alert on anomalies
   - Track relationship integrity
   - Monitor duplicate cases

3. Develop Quality Reports
   - Account activity summaries
   - Transaction pattern analysis
   - Relationship integrity checks

## Related Documents
- [Customer Data Analysis](customer_data_analysis.md) - See "Validation Results (May 31, 2025)"
- [Validation Rules](validation_rules.md)
- [Data Quality Strategy](../../development/data_quality_strategy.md) 