# KYC (Know Your Customer) Requirements

## Related Documents
- [Transaction Validation Rules](../../analysis/data_quality/validation_rules.md)
- [FI Requirements](./fi_requirements.md)
- [Swedish Transaction Patterns](./swedish_transaction_patterns.md)

## Document Relationships
This document is part of a larger regulatory framework and should be read in conjunction with:
1. Transaction Monitoring Requirements (fi_requirements.md)
2. Validation Rules (validation_rules.md)
3. Swedish Transaction Patterns (swedish_transaction_patterns.md)

## 1. Basic KYC Requirements

### 1.1 Customer Due Diligence (CDD)
- Mandatory for all business relationships
- Required for single transactions over EUR 15,000
- Required for multiple transactions totaling EUR 15,000 or more
- Required for transactions over EUR 1,000 as per Regulation 2015/847
- Cash transaction limit: EUR 10,000 (requires special documentation)

### 1.2 Customer Identification
- Verify customer's identity using valid Swedish ID or equivalent
- Collect and verify:
  * Full name
  * Personal identity number (personnummer)
  * Address
  * Contact information
- Verification thoroughness based on customer risk level
- Document verification process and stored information
- Technical requirements:
  * Data must be in digital, structured format
  * Secure storage and transmission required
  * System must support real-time verification

## 2. Enhanced Due Diligence (EDD)

### 2.1 High-Risk Situations Requiring EDD
- Politically Exposed Persons (PEPs)
- Family members and known associates of PEPs
- Customers from high-risk third countries
- Complex or unusually large transactions
- Unusual transaction patterns
- Transactions without clear economic purpose

### 2.2 PEP Requirements
- Identify source of funds
- Obtain senior management approval
- Enhanced ongoing monitoring
- Continue enhanced monitoring for 18 months after PEP status ends

## 3. Risk-Based Approach

### 3.1 Risk Assessment
- Based on general risk assessment
- Individual customer risk evaluation
- Consider product and service risks
- Geographic risk factors
- Transaction patterns

### 3.2 Risk Mitigation
- Adjust monitoring intensity based on risk level
- Document risk assessment process
- Regular review and updates
- Special attention to high-risk customers

## 4. Documentation Requirements

### 4.1 Required Information
- Customer identification data
- Beneficial ownership information
- Business relationship purpose and nature
- Source of funds (for high-risk customers)
- Transaction records
- Risk assessment documentation

### 4.2 Record Keeping
- Maintain records for 5 years
- 10 years for suspected money laundering cases
- Ensure accessibility and traceability
- Secure storage of sensitive information

## 5. Beneficial Ownership

### 5.1 Identification Requirements
- Identify natural persons with controlling influence
- Investigate ownership and control structures
- Verify beneficial owner's identity
- Document ownership structure

### 5.2 Alternative Measures
- If beneficial owner cannot be determined, identify:
  * Board chairman
  * CEO
  * Equivalent executive position
- Exception for low-risk government entities

## 6. Ongoing Monitoring

### 6.1 Transaction Monitoring
- Monitor business relationship continuously
- Review transaction patterns
- Compare against expected behavior
- Flag unusual activities

### 6.2 Profile Updates
- Regular review of customer information
- Update risk assessments
- Verify continued accuracy of data
- Document all changes

## 7. Rejection/Termination Requirements

### 7.1 When to Reject/Terminate
- Insufficient customer information
- Unable to verify identity
- Suspected money laundering
- Unacceptable risk level

### 7.2 Process Requirements
- Document decision basis
- Report suspicious activities
- Maintain confidentiality
- Follow termination procedures

## 8. System Requirements

### 8.1 Technical Requirements
- Electronic monitoring system capability
- Digital, structured, and processable data format
- Secure information transfer channels
- Real-time verification capabilities
- Integration with transaction monitoring systems

### 8.2 Data Management
- Standardized data formats for:
  * Customer information
  * Transaction data
  * Risk assessments
  * Monitoring alerts
- Automated data validation
- Regular data quality checks
- Secure backup procedures

### 8.3 Integration Requirements
- Connection to transaction monitoring systems
- Integration with risk assessment tools
- Links to external verification sources
- Interface with reporting systems

## References
1. Finansinspektionen's Guidelines on Customer Due Diligence (2025)
2. Anti-Money Laundering Act (2017:630)
3. FFFS 2017:11 (Finansinspektionen's regulations)
4. EU AML Directives (5AMLD, 6AMLD)
5. Related Internal Documents:
   - Transaction Monitoring Requirements (fi_requirements.md)
   - Validation Rules (validation_rules.md)
   - Swedish Transaction Patterns (swedish_transaction_patterns.md)

## Last Updated
2025-01-03 (Based on latest Finansinspektionen guidelines) 