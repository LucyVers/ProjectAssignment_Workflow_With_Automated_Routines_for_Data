# Project Backlog

## Project Requirements and Process
### Individual Project Management [Relates to: Phase 1 - Setup and Analysis]
- [x] Set up Personal Workflow
  - [x] Establish daily progress tracking
  - [x] Define weekly goals and milestones
  - [x] Schedule regular progress reviews
  - [x] Document decisions and changes
- [x] Project Visualization
  - [x] Set up personal project board (GitHub Projects eller liknande)
  - [x] Keep board updated with current progress
  - [x] Use for planning and progress tracking

### Development Environment Setup [Relates to: Phase 1 - Setup and Analysis]
- [x] Personal Development Environment
  - [x] Document setup process
  - [x] Configure database environment
  - [x] Set up testing environment
  - [x] Verify data access and processing
- [x] Version Control
  - [x] Set up git repository
  - [x] Create branching strategy (feature/bugfix/main)
  - [x] Document version control workflow
  - [x] Implement backup strategy
## Current Sprint (May 28 - June 2, 2025)
### In Progress 🔄
- [ ] Data Integration ⬅️ NÄSTA FOKUS [Relates to: Phase 2 - Data and Database]
  - [ ] Data Analysis Requirements
    - [ ] Analyze CSV format and structure
    - [ ] Document data quality issues
    - [ ] Identify validation rules needed
    - [ ] Create data quality strategy document
  - [ ] Notebook Development
    - [ ] Create validation notebook
    - [ ] Implement data analysis
    - [ ] Generate quality reports
    - [ ] Document validation process
  - [ ] Review data files from original project
  - [ ] Plan data migration strategy
  - [ ] Create data validation framework
  - [ ] Analyze CSV data format (transactions.csv, sebank_customers_with_accounts.csv)
  - [ ] Document data patterns and potential issues
- [ ] Validation Integration [Relates to: Phase 2 & Implementation Details - Validation System]
  - [ ] Analyze validate-transactions.ipynb
  - [ ] Plan validation implementation
  - [ ] Set up validation framework
  - [ ] Implement fraud detection rules
  - [ ] Add transaction pattern analysis

### Must Have (Critical Features)
- [x] Initial Project Setup [Completed in Phase 1]
  - [x] Basic project structure
  - [x] Documentation framework
  - [x] Version control setup
  - [x] Development environment
- [x] File Integration [Completed in Phase 1]
  - [x] Core model files
  - [x] Database files
  - [x] Utility files
- [ ] Data Integration ⬅️ NÄSTA FOKUS [Relates to: Phase 2 - Data and Database]
  - [ ] Data Analysis Requirements
    - [ ] Analyze CSV format and structure
    - [ ] Document data quality issues
    - [ ] Identify validation rules needed
    - [ ] Create data quality strategy document
  - [ ] Notebook Development
    - [ ] Create validation notebook
    - [ ] Implement data analysis
    - [ ] Generate quality reports
    - [ ] Document validation process
  - [ ] Review data files from original project
  - [ ] Plan data migration strategy
  - [ ] Create data validation framework
  - [ ] Analyze CSV data format (transactions.csv, sebank_customers_with_accounts.csv)
  - [ ] Document data patterns and potential issues
- [ ] Database Schema Implementation ⬅️ PRIORITET [Relates to: Phase 2 & Database Tasks]
  - [ ] Database Integration
    - [ ] Set up migrations system
    - [ ] Implement transaction support
    - [ ] Add rollback capability
    - [ ] Export validated data to PostgreSQL
  - [ ] Test new schema
  - [ ] Create rollback plan
  - [ ] Document migration process
  - [ ] Add new tables for:
    - [ ] Interest rates
    - [ ] Approval logs
    - [ ] Transaction monitoring
    - [ ] Fraud detection
    - [ ] Criminal activity tracking
- [ ] Data Processing Pipeline [Relates to: Phase 3 - Implementation]
  - [ ] Set up data import pipeline for CSV files
  - [ ] Implement data validation rules
  - [ ] Create error handling system
  - [ ] Implement transaction rollback mechanism
  - [ ] Add support for international transactions
  - [ ] Handle approximately 1 million transactions per day
  - [ ] Process both domestic and international transactions

### Should Have (Important Features)
- [ ] Core Functionality Implementation [Relates to: Phase 3 & Implementation Details]
  - [ ] Implement Interest calculations
  - [ ] Add Manager approval system
  - [ ] Create Officer verification system
  - [ ] Add support for 25,000 bank accounts
- [ ] Testing Framework [Relates to: Phase 6 - Testing and Optimization]
  - [ ] Create unit tests
  - [ ] Set up integration tests
  - [ ] Implement performance testing
  - [ ] Test with 100,000 transaction dataset
  - [ ] Test with 1 million transaction dataset

### Could Have (Desired Features)
- [ ] Security Enhancements [Relates to: Phase 6 - Security Testing]
  - [ ] Implement role-based access
  - [ ] Set up audit logging
  - [ ] Add transaction monitoring
  - [ ] Implement fraud detection system
  - [ ] Add criminal activity detection
- [ ] Workflow Automation [Relates to: Phase 4]
  - [ ] Set up automated testing
  - [ ] Create deployment pipeline
  - [ ] Implement monitoring system
  - [ ] Automate data quality checks
  - [ ] Generate quality reports

## Done ✓ (May 28, 2024)
### File Integration [Part of Phase 1]
- [x] Core Model Files
  - [x] account.py → src/models/account.py
  - [x] bank.py → src/models/bank.py
  - [x] customer.py → src/models/customer.py
  - [x] transaction.py → src/models/transaction.py
- [x] Database Files
  - [x] db.py → src/database/db.py
  - [x] create_db.sql → migrations/initial_schema.sql
- [x] Utility Files (Enhanced Versions)
  - [x] interest.py → src/utils/interest.py
  - [x] manager.py → src/utils/manager.py
  - [x] officer.py → src/utils/officer.py

### Database Improvements [Part of Phase 2]
- [x] Created enhanced schema with new tables
- [x] Added foreign key constraints
- [x] Added performance indexes
- [x] Added audit logging support

### Documentation [Relates to: Phase 5]
- [x] Set up documentation structure
- [x] Created integration checklist
- [x] Added daily development logs
- [x] Documented database changes
- [x] Created LICENSE.md with proper attribution
- [x] Updated documentation structure

## Project Phases (Overall Plan)
### Phase 1: Setup and Analysis ✓
[Related sections: Individual Project Management, Development Environment Setup]
- [x] Create project repository
- [x] Set up basic project structure
- [x] Create initial documentation
- [x] Investigate starter project code
- [x] Integrate starter project code
- [x] Set up development environment
- [x] Created and configured PostgreSQL database
- [x] Verified database connectivity

### Phase 2: Data and Database 🔄
[Related sections: Data Integration, Database Schema Implementation]
- [ ] Analyze provided CSV data
  - [ ] Study transactions.csv structure and format
  - [ ] Study customer data structure (sebank_customers_with_accounts.csv)
  - [ ] Document data patterns and potential issues
  - [ ] Identify potential fraud patterns
  - [ ] Analyze international transaction requirements
- [ ] Design database schema
  - [ ] Create database migration scripts
  - [ ] Design tables for transactions
  - [ ] Design tables for customers and accounts
  - [ ] Implement data validation rules
  - [ ] Add fraud detection support
  - [ ] Support for international transactions

### Phase 3: Implementation
[Related sections: Core Functionality Implementation, Data Processing Pipeline]
- [ ] Set up data processing pipeline
- [ ] Develop testing framework
- [ ] Implement core functionality

### Phase 4: Workflow Automation
[Related sections: Could Have - Workflow Automation]
- [ ] Set up automated workflow
- [ ] Create automated testing pipeline
- [ ] Implement validation checks
- [ ] Set up reporting system

### Phase 5: Documentation and Reporting
[Related sections: Documentation, Project Deliverables]
- [ ] Create technical documentation
  - [ ] API documentation
  - [ ] Database schema documentation
  - [ ] Setup and installation guide
- [ ] Implement reporting system
  - [ ] Create transaction analysis reports
  - [ ] Set up error logging and monitoring
  - [ ] Generate data quality metrics

### Phase 6: Testing and Optimization
[Related sections: Testing Framework, Security Enhancements]
- [ ] Test with 100,000 transaction dataset
  - [ ] Verify processing speed
  - [ ] Check error handling
  - [ ] Validate data quality rules
- [ ] Test with 1 million transaction dataset
  - [ ] Verify system can handle daily load
  - [ ] Monitor performance metrics
  - [ ] Test international transactions
- [ ] Performance optimization
- [ ] Security testing
  - [ ] Test fraud detection
  - [ ] Verify criminal activity detection
  - [ ] Validate international transaction handling

### Phase 7: Final Delivery
[Related sections: Project Deliverables, Final Presentation]
- [ ] Final testing and validation
- [ ] Complete documentation
- [ ] Prepare presentation
- [ ] Write individual project analysis

## Implementation Details
### Interest System [Relates to: Core Functionality Implementation]
1. Basic Implementation
   - [ ] Implement basic interest calculation
   - [ ] Add unit tests for calculations
   - [ ] Integrate with Account class

2. Advanced Features
   - [ ] Add compound interest support
   - [ ] Implement rate change tracking
   - [ ] Add interest history logging

### Manager System [Relates to: Core Functionality Implementation]
1. Core Functionality
   - [ ] Implement loan approval logic
   - [ ] Add credit limit management
   - [ ] Create risk assessment system

2. Security Features
   - [ ] Add approval audit logging
   - [ ] Implement authorization checks
   - [ ] Create activity reporting

### Officer System [Relates to: Core Functionality Implementation]
1. Basic Features
   - [ ] Implement account approval
   - [ ] Add credit approval logic
   - [ ] Create customer verification

2. Monitoring
   - [ ] Add transaction monitoring
   - [ ] Implement alert system
   - [ ] Create activity logs

## Project Deliverables [Relates to: Phase 7]
### Technical Deliverables
- [ ] Source Code
  - [ ] Complete implementation
  - [ ] Clean and documented code
  - [ ] All tests passing
  - [ ] Performance optimized
- [ ] Database
  - [ ] Final schema
  - [ ] Migration scripts
  - [ ] Data validation rules
  - [ ] Sample data sets
- [ ] Documentation
  - [ ] Technical documentation
  - [ ] API documentation
  - [ ] Setup guides
  - [ ] User manuals

### Process Documentation
- [ ] Project Management Documentation
  - [ ] Daily progress logs
  - [ ] Weekly review notes
  - [ ] Decision documentation
  - [ ] Progress tracking
- [ ] Project Analysis
  - [ ] Data quality analysis
  - [ ] Performance metrics
  - [ ] Security assessment
  - [ ] Risk analysis

### Individual Deliverables
- [ ] Individual Project Analysis
  - [ ] Document implementation decisions
  - [ ] Analyze data quality work
  - [ ] Reflect on technical solutions
  - [ ] Discuss challenges and solutions
- [ ] Process Analysis
  - [ ] Reflect on project management approach
  - [ ] Analyze methods used
  - [ ] Document what worked well
  - [ ] Suggest improvements for future projects

### Final Presentation
- [ ] Prepare Demonstration
  - [ ] Show workflow automation
  - [ ] Demonstrate data validation
  - [ ] Present quality metrics
  - [ ] Show error handling
- [ ] Seminar Preparation
  - [ ] Prepare group discussion points
  - [ ] Document key learnings
  - [ ] Prepare technical deep-dive
  - [ ] Ready examples of challenges solved

### Submission Requirements
- [ ] GitHub Repository
  - [ ] Clean and organized code
  - [ ] Complete documentation
  - [ ] README with setup instructions
  - [ ] List of team members with git usernames
- [ ] Individual Submission
  - [ ] Link to group repository
  - [ ] Personal project analysis
  - [ ] Individual reflection document
  - [ ] Process analysis 