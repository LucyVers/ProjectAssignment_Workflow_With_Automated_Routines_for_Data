# Project Assignment: Workflow With Automated Routines for Data Quality in Banking Systems

This project implements an automated workflow for handling and validating bank transaction data, focusing on data quality and security. The system processes approximately 1 million transactions per day, handling both domestic and international transactions for a Swedish bank with around 25,000 accounts.

## Project Attribution

This project is built upon and extends the starter project ["python-bank-project-start"](https://github.com/WeeHorse/python-bank-project-start). While this implementation represents my individual academic work, it acknowledges and respects the foundation provided by the original project. 

**Important Note**: The original project's license terms are not explicitly stated in its repository. Before using any code from either this project or the original starter project, please:
- Check the original repository for any license updates
- Contact the original project maintainers if needed
- Ensure compliance with any applicable terms

For more information about licensing and usage rights, please see the [LICENSE.md](LICENSE.md) file.

## Project Structure

```
├── src/                    # Source code
│   ├── data_processing/    # Data processing and validation scripts
│   ├── database/          # Database related code and migrations
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── notebooks/             # Jupyter notebooks for data analysis
├── docs/                  # Documentation
│   ├── development/      # Development documentation
│   └── api/             # API documentation
├── data/                 # Data directory (gitignored for sensitive data)
└── workflows/            # Workflow configuration files
```

## Getting Started

### Prerequisites
- Python 3.x
- PostgreSQL
- Additional requirements listed in `requirements.txt`

### Installation
1. This project is based on the starter project ["python-bank-project-start"](https://github.com/WeeHorse/python-bank-project-start)

2. Clone this repository
```bash
git clone https://github.com/LucyVers/ProjectAssignment_Workflow_With_Automated_Routines_for_Data.git
cd ProjectAssignment_Workflow_With_Automated_Routines_for_Data
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Development Progress
- [x] Initial project setup
- [ ] Database schema design
- [ ] Data validation implementation
- [ ] Automated workflow setup
- [ ] Testing framework
- [ ] Documentation

## Documentation
Detailed documentation can be found in the `/docs` directory.

## Testing
Tests are located in the `/tests` directory. To run tests:
```bash
python -m pytest
```

## Copyright and License

This project is an individual academic work created by Lucy Sonberg. All rights reserved.

Copyright © 2025 Lucy Sonberg

This project and its contents are protected by copyright law. For detailed terms of use and permissions, please see [LICENSE.md](LICENSE.md).

---
*Note: This is an individual academic project. Any use, reproduction, or distribution requires explicit permission from the copyright holder.*