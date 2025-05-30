# Data Quality Validation Rules

## Related Documents
- [Customer Data Analysis](customer_data_analysis.md) - See "Validation Results (May 31, 2025)" for latest findings
- [KYC Requirements](../../sources/regulatory_documents/kyc_requirements.md)
- [FI Requirements](../../sources/regulatory_documents/fi_requirements.md)
- [Swedish Transaction Patterns](../../sources/regulatory_documents/swedish_transaction_patterns.md)

## Recent Validation Findings
**Important**: Recent validation (May 31, 2025) has identified several critical issues that require immediate attention. See [Customer Data Analysis](customer_data_analysis.md) for full details.

Key findings requiring rule updates:
- 419 duplicate personnummer detected
- 55 cases of potentially underage customers
- 998 invalid postal codes
- 886 invalid city names
- 459 non-standardized phone numbers

## Overview
This document defines the validation rules for my banking data quality system, based on the analysis of perfect quality patterns observed in 2024 data and current KYC/AML requirements. These rules will be used to validate both customer and transaction data.

## Acceptable Formats and Thresholds

### Data Formats
1. Account Numbers
   - Format: `SE8902[A-Z]{4}[0-9]{14}`
   - Length: Exactly 24 characters
   - Example: SE8902EPWK73250364544965

2. Personal Information
   - Personnummer: `YYMMDD-XXXX`
     * **NEW**: Additional check for duplicates required
     * **NEW**: Age verification check required (minimum age: 15)
   - Phone Numbers:
     * **Preferred Formats**:
       - International: `+46 (0)XXX XXX XX`
       - Local: `XXX-XXX XX XX`
     * **NEW**: Standardization required for non-compliant formats
   - Address Format:
     * **NEW**: Enhanced validation against current postal codes
     * **NEW**: City name verification against municipality list
     - Street: `[Street Name] [Number]`
     - Postal Code: `[5 digits]`
     - City: Valid Swedish municipality name

3. Transaction Data
   - Amount Format: Decimal number with 2 decimal places
   - Currency: ISO 4217 format (e.g., SEK, EUR, USD)
   - Timestamp: ISO 8601 format (YYYY-MM-DD HH:mm:ss)

### Threshold Values
1. Transaction Amounts
   - Minimum: 1 SEK
   - Maximum per transaction type:
     - Regular transfer (private): 50,000 SEK per day
     - Regular transfer (business): 500,000 SEK per day
     - Salary payment: 20,000 - 80,000 SEK (amounts over 100,000 SEK require verification)
     - Mortgage/rent payment: 4,000 - 20,000 SEK
     - Utility bills: 500 - 5,000 SEK
     - Insurance payments: 100 - 3,000 SEK
     - Loan payments: 1,000 - 15,000 SEK

2. Transaction Frequency
   - Maximum transactions per day:
     - Private accounts: 10 transactions
     - Business accounts: 30 transactions
   - Minimum time between transactions: 1 minute
   - International transactions:
     - Requires pre-approved international transfer capability
     - Maximum 3 international transfers per month
     - Additional documentation required for amounts over 15,000 SEK
     - Monthly limit: 150,000 SEK

3. Account Limits
   - Maximum accounts per private customer: 3
   - Maximum accounts per business customer: 5
   - Special approval required for international transfer capabilities
   - Minimum account age for international transfers: 3 months

## 1. Account Validation Rules

### 1.1 Account Number Format
- **Rule**: All account numbers must follow SE8902XXXX[14 digits] format
- **Pattern**: `SE8902[A-Z]{4}[0-9]{14}`
- **Validation Steps**:
  1. Check length (24 characters)
  2. Verify prefix (SE8902)
  3. Validate character types (4 uppercase letters followed by 14 digits)
- **Error Handling**: Reject any account numbers not matching this format

### 1.2 Account Existence
- **Rule**: All accounts in transactions must exist in customer database
- **Validation Steps**:
  1. Check sender account exists
  2. Check receiver account exists (for domestic transactions)
- **Error Handling**: Flag transactions with non-existent accounts for review

## 2. Transaction Validation Rules

### 2.1 Pre-Transaction Validation
- **Rule**: Verify transaction eligibility before processing
- **Validation Steps**:
  1. Customer Status Check:
     - Verify customer KYC status is current
     - Check risk classification level
     - Confirm no pending due diligence items
     - Verify account privileges match transaction type
  2. Transaction Type Validation:
     - Check if transaction type is allowed for customer risk level
     - Verify customer is approved for international transfers (if applicable)
     - Confirm transaction purpose is valid
  3. Amount Pre-validation:
     - Check against customer's risk-based limits
     - Verify against daily/monthly cumulative limits
     - Compare with typical transaction patterns
- **Error Handling**:
  - Block transaction if KYC status incomplete
  - Require additional approval for high-risk customers
  - Flag for review if outside normal patterns

### 2.2 Geographic and Counterparty Validation
- **Rule**: Validate transaction geography and counterparty based on risk
- **Validation Steps**:
  1. Geographic Risk Assessment:
     - Verify sender/receiver countries against risk lists
     - Check for high-risk jurisdictions
     - Validate against customer's approved countries
     - Apply enhanced validation for high-risk countries
  2. Counterparty Validation:
     - Screen counterparty against sanctions lists
     - Check for PEP connections
     - Verify first-time recipient status
     - Review counterparty risk rating
  3. Documentation Requirements:
     - Determine required documentation based on risk
     - Verify documentation completeness
     - Check documentation validity
- **Error Handling**:
  - Block transactions to sanctioned countries/entities
  - Require enhanced documentation for high-risk destinations
  - Flag new counterparty relationships for review

### 2.3 Amount and Frequency Validation
- **Rule**: Apply risk-based transaction limits and monitoring
- **Validation Steps**:
  1. Basic Amount Validation:
     - Check minimum amount (≥ 1 SEK)
     - Verify against maximum limits by type:
       * Regular transfer (private): ≤ 50,000 SEK per day
       * Regular transfer (business): ≤ 500,000 SEK per day
       * Salary payment: 20,000 - 80,000 SEK
       * Other types: [existing limits]
  2. Risk-Based Amount Controls:
     - Apply stricter limits for high-risk customers
     - Enhanced due diligence triggers:
       * Transactions over EUR 15,000
       * Cash transactions over EUR 10,000
       * Wire transfers over EUR 1,000
     - Cumulative amount monitoring:
       * Daily totals against risk profile
       * Monthly patterns analysis
       * Unusual amount clustering
  3. Frequency Monitoring:
     - Track transaction frequency against risk profile
     - Monitor pattern changes
     - Apply risk-based frequency limits:
       * Low risk: standard limits
       * Medium risk: enhanced monitoring
       * High risk: restricted limits
- **Error Handling**:
  - Block transactions exceeding risk-based limits
  - Require additional approval based on amount/risk combination
  - Flag unusual patterns for investigation

### 2.4 Documentation and Reporting
- **Rule**: Ensure proper documentation and reporting based on transaction characteristics
- **Validation Steps**:
  1. Documentation Requirements:
     - Determine required documentation based on:
       * Transaction amount
       * Customer risk level
       * Transaction type
       * Geographic risk
     - Verify documentation completeness
     - Validate document authenticity
  2. Regulatory Reporting Checks:
     - Identify reportable transactions
     - Verify reporting requirements met
     - Track reporting deadlines
  3. Record Keeping:
     - Maintain transaction audit trail
     - Document approval decisions
     - Store supporting documentation
     - Track verification steps
- **Error Handling**:
  - Hold transactions pending documentation
  - Flag missing or incomplete records
  - Escalate reporting violations

## 3. Customer Data Validation

### 3.1 Personal Information
- **Rule**: Customer information must be complete and valid
- **Validation Steps**:
  1. Verify personnummer format (YYMMDD-XXXX)
  2. Validate phone number format
  3. Check address format and postal code
- **Error Handling**: Flag incomplete or invalid customer records

### 3.2 Data Consistency
- **Rule**: Customer information must be consistent across all accounts
- **Validation Steps**:
  1. Check for matching customer details across multiple accounts
  2. Verify address consistency
  3. Ensure phone number consistency
- **Error Handling**: Flag inconsistent customer records

## 4. Relationship Validation

### 4.1 Customer-Account Relationships
- **Rule**: All accounts must have valid customer relationships
- **Validation Steps**:
  1. Verify each account is linked to exactly one customer
  2. Check customer-account relationship validity
- **Error Handling**: Flag orphaned or incorrectly linked accounts

### 4.2 Transaction Relationships
- **Rule**: All transactions must have valid relationship chains
- **Validation Steps**:
  1. Verify sender-receiver relationship validity
  2. Check transaction type matches account types
  3. Validate transaction purpose
- **Error Handling**: Flag transactions with invalid relationships

## Implementation Priority

### High Priority
1. Account number format validation
2. Geographic data validation
3. Currency and amount validation
4. Basic customer information validation

### Medium Priority
1. Relationship validation
2. Extended customer data validation
3. Transaction chain validation

### Low Priority
1. Advanced pattern detection
2. Historical data validation
3. Statistical anomaly detection

## Next Steps
1. Design monitoring system based on these rules
2. Create validation implementation plan
3. Develop test cases for each rule
4. Set up automated validation pipeline

## 1. Transaction Amount Thresholds

### 1.1 Regular Domestic Transactions
- Minimum amount: 1 SEK
- Maximum per transaction:
  - Private accounts: 150,000 SEK per day
  - Business accounts: 500,000 SEK per day
  - Special approval required for higher amounts

### 1.2 Salary Payments
- Typical range: 20,000 - 80,000 SEK per month
- Amounts over 100,000 SEK require additional verification
- Annual bonus payments may exceed these limits but require special documentation

### 1.3 Regular Monthly Payments
- Rent/Mortgage: 4,000 - 20,000 SEK
- Utility bills: 500 - 5,000 SEK
- Insurance: 100 - 3,000 SEK
- Loan payments: 1,000 - 15,000 SEK

### 1.4 International Transactions
- Requires pre-approved international transfer capability
- Maximum 3 international transfers per month without additional documentation
- Single transfer limit: 50,000 SEK
- Monthly limit: 150,000 SEK
- Additional documentation required for:
  - Amounts over 15,000 SEK
  - Business-related transfers
  - First-time international recipients

## 2. Transaction Frequency Rules

### 2.1 Daily Limits
- Maximum transactions per day: 
  - Private accounts: 10 transactions
  - Business accounts: 30 transactions
- Minimum time between transactions: 1 minute
- Automated recurring payments exempt from frequency limits

### 2.2 Monthly Monitoring
- Unusual patterns trigger review:
  - Sudden increase in transaction frequency
  - Multiple transactions just below limits
  - Irregular payment patterns
  - New recipients for large amounts

## 3. Account-Level Rules

### 3.1 Account Limits
- Maximum accounts per private customer: 3
- Maximum accounts per business customer: 5
- Joint accounts require verification of all parties

### 3.2 International Transfer Capability
- Not available by default
- Requires:
  - Account age: minimum 3 months
  - Clean transaction history
  - Completed enhanced due diligence
  - Valid identification and documentation

## 4. Risk-Based Validation

### 4.1 High-Risk Indicators
- Multiple transactions near threshold limits
- Frequent international transfers
- Unusual transaction patterns
- New recipients for large amounts
- Transactions with high-risk countries

### 4.2 Enhanced Due Diligence Required For
- New international transfer recipients
- Transactions over 150,000 SEK
- Business accounts with high transaction volumes
- Politically exposed persons (PEP)
- Customers from high-risk countries

## 5. KYC Validation Rules

### 5.1 Customer Risk Classification
- **Rule**: All customers must be risk-classified based on KYC criteria
- **Validation Steps**:
  1. Initial Risk Assessment:
     - Check against PEP lists
     - Verify high-risk country connections
     - Review business type and structure
     - Check transaction patterns
  2. Ongoing Risk Monitoring:
     - Monitor changes in customer behavior
     - Track transaction patterns
     - Review geographic exposure
     - Update risk classification as needed
- **Risk Levels**:
  - Low: Standard due diligence
  - Medium: Enhanced monitoring
  - High: Enhanced due diligence required
- **Error Handling**: 
  - Block account opening for unacceptable risk
  - Flag for review if risk level changes
  - Require management approval for high risk

### 5.2 Due Diligence Requirements
- **Rule**: Apply appropriate due diligence based on risk level
- **Validation Steps**:
  1. Standard Due Diligence:
     - Verify customer identity
     - Confirm address
     - Document purpose of account
     - Record expected transaction patterns
  2. Enhanced Due Diligence:
     - Verify source of funds
     - Document business structure
     - Identify beneficial owners
     - Get senior management approval
- **Documentation Requirements**:
  - Store all verification documents
  - Maintain audit trail of checks
  - Record approval decisions
  - Document risk assessments
- **Error Handling**:
  - Block transactions if due diligence incomplete
  - Flag for review if documentation expires
  - Require re-verification periodically

### 5.3 PEP and Sanctions Screening
- **Rule**: Screen all customers against PEP and sanctions lists
- **Validation Steps**:
  1. Initial Screening:
     - Check customer against PEP database
     - Screen against sanctions lists
     - Identify associated persons
     - Document screening results
  2. Ongoing Monitoring:
     - Daily sanctions screening
     - Monthly PEP screening
     - Review of associated persons
     - Document all changes
- **Error Handling**:
  - Block transactions for sanctions matches
  - Require approval for PEP relationships
  - Flag changes in PEP status
  - Document all decisions

### 5.4 Transaction Monitoring for KYC
- **Rule**: Monitor transactions against customer KYC profile
- **Validation Steps**:
  1. Profile Validation:
     - Compare to expected patterns
     - Check transaction types
     - Verify amount ranges
     - Monitor frequency
  2. Threshold Monitoring:
     - Track cumulative amounts
     - Monitor single transactions
     - Check international transfers
     - Verify documentation for large amounts
- **Specific Thresholds**:
  - EUR 15,000: Enhanced due diligence
  - EUR 10,000: Cash transaction limit
  - EUR 1,000: Wire transfer documentation
- **Error Handling**:
  - Block transactions outside profile
  - Require documentation for large amounts
  - Flag unusual patterns
  - Escalate suspicious activity

## 5. Documentation Requirements

### 5.1 Standard Transactions
- Valid Swedish ID or equivalent
- Proof of address
- Source of funds for large deposits

### 5.2 Additional Documentation
Required for:
- International transfers
- Business accounts
- High-value transactions
- New customer relationships
- Changes in transaction patterns 