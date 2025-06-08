# User Manual - Data Quality Management System
Last updated: June 7, 2025

## Project Overview
This project implements a data quality management system for a Swedish bank, handling approximately 1 million transactions per day across 25,000 accounts. The system processes CSV-format transaction data, validates it, and stores it in a PostgreSQL database using Prefect for workflow automation.

## Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Git
- Prefect 2.x

## Installation Steps

### 1. Clone the Repository
```bash
git clone [repository-url]
cd ProjectAssignment_Workflow_With_Automated_Routines_for_Data2
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
1. Create PostgreSQL database:
```bash
createdb bank_db
```

2. Configure database connection:
   - Copy `.env.example` to `.env`
   - Update database connection parameters in `.env`:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bank_db
DB_USER=your_username
DB_PASSWORD=your_password
```

3. Run database migrations:
```bash
alembic upgrade head
```

## Using the System

### 1. Data Files
The system processes two main data files in the `data/working/` directory:
- `transactions.csv` - Transaction data
- `sebank_customers_with_accounts.csv` - Customer and account data
- `transactions_updated.csv` - Generated file with validated transactions

### 2. Running the System
The system uses Prefect for workflow automation. There are two main workflows:

1. Import Account Data:
```python
from src.data_processing.workflow import import_accounts

# Run with default settings
result = import_accounts()

# Or specify custom paths and batch size
result = import_accounts(
    customers_path="data/working/sebank_customers_with_accounts.csv",
    batch_size=500
)
```

2. Process Transactions:
```python
from src.data_processing.workflow import validate_and_load

# Run with default settings
result = validate_and_load()

# Or specify custom settings
result = validate_and_load(
    transactions_path="data/working/transactions.csv",
    customers_path="data/working/sebank_customers_with_accounts.csv",
    batch_size=500
)
```

### 3. Data Validation
The system includes comprehensive validation:
- Transaction amount limits (0.01-100,000 SEK)
- Account number format (SE8902[A-Z]{4}\d{14})
- Personal ID format (YYMMDD-XXXX)
- Geographic data validation
- Fraud detection

### 4. Project Structure
```
/
├── src/
│   ├── data_processing/       # Core processing logic
│   │   ├── workflow.py       # Main workflow definitions
│   │   ├── data_validator.py # Data validation logic
│   │   └── transaction_validator.py # Transaction validation
│   ├── utils/                # Utility functions
│   ├── database/             # Database operations
│   └── models/              # Data models
├── data/
│   └── working/             # Active data files
└── tests/                   # Test suite
```

### 5. Key Components
1. Data Processing (`src/data_processing/`)
   - `workflow.py` - Main entry point with Prefect workflows
   - `data_validator.py` - Data validation logic
   - `transaction_validator.py` - Transaction-specific validation

2. Data Files (`data/working/`)
   - Contains the active CSV files being processed
   - Stores validation results

3. Database Models (`src/models/`)
   - Defines database structure
   - Handles data relationships

## Troubleshooting

### Common Issues

1. Database Connection Error
```
Solution: Check .env file configuration and ensure PostgreSQL is running
```

2. Import Errors
```
Solution: Verify CSV file format and location
```

3. Validation Failures
```
Solution: Check data format and review validation logs
```

## Support and Documentation
For more detailed information, refer to:
- [Project Documentation](docs/README.md)
- [Data Quality Strategy](docs/development/data_quality_strategy.md)
- [Implementation Plan](docs/implementation/implementation_plan.md)

## Project Requirements Fulfillment
This system fulfills the course requirements by:
1. Handling data flow through structured applications and databases
2. Implementing testing and validation
3. Using migrations and transaction rollbacks
4. Managing workflows with Prefect automation
5. Processing ~1M transactions/day
6. Managing ~25,000 accounts
7. Handling both domestic and international transactions
8. Implementing fraud detection and error correction 