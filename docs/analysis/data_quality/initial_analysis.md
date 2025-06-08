# Initial Data Quality Analysis

## Overview
This document tracks my systematic approach to analyzing data quality in the banking transaction system. The analysis focuses on two main data sources:
1. Transaction data (transactions.csv)
2. Customer data (sebank_customers_with_accounts.csv)

## Project Context
- Swedish bank handling ~1M transactions/day
- Approximately 25,000 accounts
- Mix of domestic and international transactions
- Need to handle data quality issues and fraud attempts

## Analysis Process

### Step 1: Initial Data Overview (2025-05-29)

#### 1.1 Customer Data Analysis
- Total rows in customer file: 1,001 (including header)
- Unique customers: 581 (based on personnummer)
- Multiple accounts per customer identified
- Data structure:
  - Customer name
  - Address
  - Phone
  - Personnummer
  - Bank Account number (IBAN format)

For detailed findings, see:
- [Customer Data Analysis](customer_data_analysis.md)
- [Duplicate IDs Analysis](duplicate_ids_analysis.md)

#### 1.2 Transaction Data Analysis
- Total transactions: 100,001 (including header)
- Geographic distribution:
  - Sweden: 80,306 transactions (80.3%)
  - Other Nordic countries: Significant presence
    - Norway: 951
    - Denmark: 918
    - Iceland: 892
    - Finland: 870
  - International: Various countries worldwide

For detailed transaction analysis, see:
- [Transaction Validation Rules](validation_rules.md)
- [Missing Country Analysis](missing_country_analysis.md)

#### 1.3 Initial Data Quality Issues Identified
1. Missing Data:
   - 500 transactions with empty country fields
   - See [Missing Country Analysis](missing_country_analysis.md) for resolution
2. Data Consistency Issues:
   - Inconsistent country name formatting (e.g., "United States of America" vs "USA")
   - See [Data Relationships Analysis](data_relationships.md) for standardization
3. Distribution Anomalies:
   - Some countries have very few transactions (requires further investigation)
   - Detailed in [Transaction Validation Rules](validation_rules.md)

### Next Steps
Proposed areas for deeper analysis:

1. Transaction Amounts:
   - Analyze distribution of transaction amounts
   - Identify potential outliers
   - Look for suspicious patterns
   - See [Transaction Validation Rules](validation_rules.md)

2. Missing Data Investigation:
   - Detailed analysis of the 500 transactions with missing country data
   - Determine if there are patterns in these missing values
   - Resolution documented in [Missing Country Analysis](missing_country_analysis.md)

3. Transaction Types:
   - Analyze distribution of incoming vs outgoing transactions
   - Look for patterns in transaction types by country
   - See [Transaction Validation Rules](validation_rules.md)

## Methodology
My analysis follows these principles:
1. Systematic documentation of all findings
2. Data-driven decision making
3. Focus on both patterns and anomalies
4. Progressive refinement of analysis
5. Clear documentation of all steps and findings

## Tools Used
- Command line tools for initial data exploration
- Python scripts for detailed analysis (to be developed)
- Version control for tracking changes
- Markdown documentation for clarity and accessibility 