# Data Quality Management System

## Project Overview
This project implements an automated workflow system for data quality management, focusing on transaction data processing and validation. The system includes comprehensive data validation, automated workflows, and detailed reporting capabilities.

## Core Features
- Data validation framework using Great Expectations
- Automated workflow management with Prefect
- Database integration with SQLAlchemy and Alembic migrations
- Comprehensive logging and error handling
- Automated testing suite

## Implementation Status
All core requirements have been successfully implemented:

### Data Processing
- CSV transaction data handling
- Database setup with migrations
- Validation framework

### Automation
- Workflow management
- Automated testing
- Report generation

### Data Models
Implemented with validation for:
- Account numbers (SE8902[A-Z]{4}\d{14})
- Personal ID (YYMMDD-XXXX)
- Postal codes (5 digits)
- Phone numbers (Swedish format)

## Project Structure
```
project/
├── src/
│   ├── data_processing/
│   ├── database/
│   ├── validation/
│   └── workflow/
├── tests/
├── docs/
│   ├── development/
│   └── user_guides/
└── notebooks/
```

## Documentation
- [Project Requirements](docs/project_requirements.txt)
- [Development Logs](docs/development/daily_logs/)
- [TODO List](TODO.md)

## Setup and Installation
[Installation instructions will be added]

## Usage
[Usage instructions will be added]

## Contributing
[Contributing guidelines will be added]

## License
[License information will be added]