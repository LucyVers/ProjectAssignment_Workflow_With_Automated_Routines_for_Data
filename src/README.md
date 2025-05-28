# Source Code Structure

This directory contains the main source code for the bank transaction processing system.

## Directory Structure

### `/models`
Contains the core business model classes:
- `account.py`: Account management and operations
- `bank.py`: Bank entity and operations
- `customer.py`: Customer information and management
- `transaction.py`: Transaction processing and validation

### `/database`
Database-related components:
- `db.py`: Database connection and operations
- `/migrations`: Database schema and migrations
  - `initial_schema.sql`: Initial database structure

### `/utils`
Utility and helper functions:
- `interest.py`: Interest calculation utilities
- `manager.py`: Management-related utilities
- `officer.py`: Officer-related operations

### Root Files
- `app.py`: Main application entry point and example usage

## Code Organization

The code is organized following these principles:
1. Separation of concerns
2. Modular design
3. Clear dependencies
4. Easy to test structure

## Usage

The main application can be run through `app.py`, which demonstrates basic usage of the banking system components. 