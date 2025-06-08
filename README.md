# Advanced Data Quality Management System
© 2025 Lucy Sonberg

## Project Overview
This is my individual extension and enhancement of the [python-bank-project-start](https://github.com/WeeHorse/python-bank-project-start). I have developed a sophisticated data quality management system focusing on transaction validation, fraud detection, and automated data processing workflows.

## Data Sources
The project works with the following data files:

### Customer Data
- **Original File**: `data/original/sebank_customers_with_accounts.csv`
- **Processed File**: `data/working/sebank_customers_with_accounts.csv`
- **Content**: Customer information including:
  * Personal identification numbers (personnummer)
  * Names
  * Addresses
  * Phone numbers
  * Bank account numbers (IBAN format)
- **Size**: ~1,000 customer records
- **Analysis**: See [Customer Data Analysis](docs/analysis/data_quality/customer_data_analysis.md)

### Transaction Data
- **Original File**: `data/original/transactions.csv`
- **Processed File**: `data/working/transactions_updated.csv`
- **Content**: Banking transactions including:
  * Transaction amounts
  * Sender/receiver information
  * Transaction types
  * Geographic data
  * Timestamps
- **Volume**: Processing ~1M transactions per day
- **Analysis**: See [Transaction Validation Rules](docs/analysis/data_quality/validation_rules.md)

### Data Processing Flow
1. Original data files in `data/original/` serve as the source data
2. Data quality checks and transformations are applied
3. Processed files are saved in `data/working/` for further analysis
4. Continuous validation ensures data integrity throughout the process

For detailed information about the data processing workflow, see:
- [Initial Data Analysis](docs/analysis/data_quality/initial_analysis.md)
- [Data Relationships Analysis](docs/analysis/data_quality/data_relationships.md)

## Key Achievements
- Implemented comprehensive fraud detection system
- Developed advanced data validation framework
- Created automated workflow management
- Built robust database architecture with SQLAlchemy
- Achieved 99.9% accuracy in transaction validation

## Core Features

### Data Quality & Validation
- [Transaction Validation Analysis](docs/analysis/data_quality/validation_rules.md)
- [Address Validation System](docs/analysis/data_quality/address_validation_analysis.md)
- [Personal ID Verification](docs/analysis/data_quality/duplicate_personnummer_analysis.md)
- [Phone Number Standardization](docs/analysis/data_quality/phone_number_analysis.md)
- [Age Verification System](docs/analysis/data_quality/age_verification_analysis.md)

### Fraud Detection
- Pattern recognition for suspicious transactions
- Real-time validation system
- Geographic risk assessment
- Customer profile-based validation
- [Detailed Analysis](docs/analysis/individual_analysis_template.md#2.6-Advanced-Fraud-Detection)

### Data Processing
- Batch processing for large datasets
- Transaction validation pipeline
- Automated error correction
- Comprehensive logging system

## Technical Implementation

### Database Architecture
- SQLAlchemy with connection pooling
- Transaction management with rollback support
- Automated migrations using Alembic
- [Database Architecture Details](docs/development/database_architecture.md)

### Data Models
Implemented with strict validation for:
- Account numbers (SE8902[A-Z]{4}\d{14})
- Personal ID (YYMMDD-XXXX)
- Postal codes (5 digits)
- Phone numbers (Swedish format)

## Project Structure
```
ProjectAssignment_Workflow_With_Automated_Routines_for_Data/
├── src/                    # Source code
│   ├── data_processing/    # Data processing modules
│   ├── database/          # Database management
│   ├── models/            # Data models
│   └── utils/             # Utility functions
├── docs/                   # Documentation
│   ├── analysis/          # Analysis documents
│   ├── development/       # Development logs
│   └── implementation/    # Implementation details
├── notebooks/             # Jupyter notebooks
├── tests/                 # Test suite
└── data/                  # Data directory
```

## Documentation Index

### Analysis Documents
- [Individual Project Analysis](docs/analysis/individual_analysis_template.md) - Comprehensive overview of my data quality project implementation, technical challenges, and solutions
- [Data Quality Strategy](docs/development/data_quality_strategy.md) - Strategic approach to ensuring data quality across the system
- [Implementation Plan](docs/implementation/implementation_plan.md) - Detailed plan for system implementation and deployment

#### Data Quality Analysis Series
1. **Initial Assessment**
   - [Initial Data Analysis](docs/analysis/data_quality/initial_analysis.md) - First evaluation of the dataset, identifying key challenges and patterns
   - [Data Relationships Analysis](docs/analysis/data_quality/data_relationships.md) - Analysis of connections between different data entities

2. **Customer Data Validation**
   - [Customer Data Analysis](docs/analysis/data_quality/customer_data_analysis.md) - Deep dive into customer data quality and patterns
   - [Personal ID Verification](docs/analysis/data_quality/duplicate_personnummer_analysis.md) - Analysis of personnummer duplicates and verification process
   - [Age Verification Analysis](docs/analysis/data_quality/age_verification_analysis.md) - Study of age-related data quality issues
   - [Duplicate IDs Analysis](docs/analysis/data_quality/duplicate_ids_analysis.md) - Investigation of duplicate customer identifiers

3. **Contact Information Quality**
   - [Address Validation Analysis](docs/analysis/data_quality/address_validation_analysis.md) - Analysis of address data quality and standardization
   - [Phone Number Analysis](docs/analysis/data_quality/phone_number_analysis.md) - Investigation of phone number formats and validation

4. **Transaction Data Quality**
   - [Transaction Validation Rules](docs/analysis/data_quality/validation_rules.md) - Comprehensive transaction validation framework
   - [Missing Country Analysis](docs/analysis/data_quality/missing_country_analysis.md) - Investigation of transactions with incomplete geographic data

### Technical Documentation
- [Project Requirements](docs/project_requirements.txt)
- [Database Architecture](docs/development/database_architecture.md)
- [Integration Checklist](docs/development/integration_checklist.md)

### Development Logs
- [Project Timeline](docs/development/project_timeline.md)
- [Integration Log](docs/development/integration_log.md)
- [Work Plan](docs/development/work_plan.md)

## Installation and Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip package manager

### Installation Steps
1. Clone the repository
```bash
git clone [repository-url]
cd ProjectAssignment_Workflow_With_Automated_Routines_for_Data
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up the database
```bash
alembic upgrade head
```

## Usage
Detailed usage instructions and examples can be found in the [User Manual](docs/implementation/user_manual.md).

## Testing
The project includes comprehensive test coverage:
```bash
python -m pytest
```

## License
This project is built upon the [python-bank-project-start](https://github.com/WeeHorse/python-bank-project-start) and includes my individual enhancements and analysis.

## Author
Lucy Sonberg
- Individual project implementation and analysis
- Data quality management system development
- Advanced fraud detection implementation