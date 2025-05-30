# Customer Data Analysis

## Overview
This document contains the analysis of customer data from the file `sebank_customers_with_accounts.csv`.

## Analysis Goals
1. Understanding Customer Data Structure
   - Identify all fields and their significance
   - Analyze data quality and patterns
   - Identify potential issues or anomalies

2. Validation Based on 2024 Patterns
   - Compare with quality patterns from transaction analysis
   - Identify quality rules for customer data
   - Document validation rules

## Initial Data Analysis

### File Structure
- Total rows: 1001 (including header)
- Format: CSV (comma-separated values)
- Fields:
  1. Customer (Name)
  2. Address
  3. Phone
  4. Personnummer (Swedish personal ID)
  5. BankAccount

### Initial Observations
1. Customer-Account Relationship
   - One customer can have multiple bank accounts
   - Each account is on a separate row
   - Customer information is repeated for each account

2. Data Format Patterns
   - Bank accounts follow format: SE8902... (SEXXXX format)
   - Phone numbers have inconsistent formats:
     - Local format: "061-608 60 88"
     - International format: "+46 (0)396 101 64"
   - Addresses include postal code and city

3. Potential Quality Issues
   - Inconsistent phone number formatting
   - Repeated customer information across rows
   - Need to verify personnummer format consistency

### Next Analysis Steps
1. Verify data completeness
   - Check for missing values
   - Validate required fields
   
2. Analyze data patterns
   - Count unique customers vs accounts
   - Verify personnummer format
   - Check address format consistency

3. Compare with 2024 quality standards
   - Review against transaction data patterns
   - Identify validation rules

## Quality Issues and Solutions
(To be updated with identified issues and solutions)

## Validation Rules
(To be updated with specific rules)

### Detailed Data Analysis

1. Customer Distribution
   - Total records: 1000 (excluding header)
   - Unique customers: 581
   - Average accounts per customer: ~1.72 accounts

2. Data Format Analysis
   a. Personal ID (Personnummer)
   - Format: YYMMDD-XXXX
   - Examples: 400118-5901, 391117-9285, 981215-7254
   - Appears to be valid Swedish personal ID format
   - Consistent formatting across entries

   b. Bank Account Numbers
   - Format: SE8902XXXX... (20 characters after prefix)
   - All accounts start with SE8902
   - Followed by 4 letters and 14 digits
   - Example: SE8902EPWK73250364544965

   c. Phone Numbers
   - Two distinct formats observed:
     1. Local format: "011-396 09 07"
     2. International format: "+46 (0)918 939 10"
   - Inconsistent formatting could be a data quality issue

   d. Addresses
   - Format: "Street Name Number, Postal Code City"
   - Example: "Ängsvägen 03, 14010 Gävle"
   - Consistent formatting with:
     - Street name and number
     - 5-digit postal code
     - City name

3. Data Quality Patterns
   a. Consistency
   - Customer information is identical across multiple accounts
   - Address format is consistent
   - Personnummer format is consistent
   - Phone number format varies

   b. Completeness
   - No missing values observed in initial sample
   - All required fields are present
   - All fields follow expected patterns

   c. Potential Issues
   - Phone number format inconsistency
   - Need to verify if all personnummer are valid
   - Need to verify postal code validity

### Next Analysis Steps
1. Data Validation
   - Create validation rules for each field
   - Verify postal codes against valid Swedish postal codes
   - Validate personnummer check digits
   - Standardize phone number format

2. Relationship Analysis
   - Map customer to account relationships
   - Verify account number uniqueness
   - Check for duplicate customer records

3. Quality Metrics
   - Calculate completeness percentage
   - Measure format consistency
   - Identify any outliers or anomalies 