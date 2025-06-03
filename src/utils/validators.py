"""
Validation utilities for bank transactions and customer data.
"""
from typing import Dict, List, Optional
import re
from datetime import datetime

def validate_personnummer(personnummer: str) -> bool:
    """
    Validate Swedish personal identity number.
    Format: YYYYMMDD-XXXX
    """
    if not isinstance(personnummer, str):
        return False
    
    pattern = r'^\d{8}-\d{4}$'
    if not re.match(pattern, personnummer):
        return False
    
    # Extract date components
    try:
        date_str = personnummer[:8]
        datetime.strptime(date_str, '%Y%m%d')
    except ValueError:
        return False
    
    return True

def validate_account_number(account: str) -> bool:
    """
    Validate bank account number.
    Format: SE8902XXXX00000000000000 (SE + 24 digits)
    """
    if not isinstance(account, str):
        return False
    
    pattern = r'^SE\d{24}$'
    return bool(re.match(pattern, account))

def validate_transaction(transaction: Dict) -> List[str]:
    """
    Validate a transaction dictionary.
    Returns list of validation errors, empty list if valid.
    """
    errors = []
    
    # Required fields
    required_fields = ['transaction_id', 'from_account', 'to_account', 'amount', 'timestamp']
    for field in required_fields:
        if field not in transaction:
            errors.append(f"Missing required field: {field}")
    
    # Account number format
    if 'from_account' in transaction:
        if not validate_account_number(transaction['from_account']):
            errors.append("Invalid from_account format")
    
    if 'to_account' in transaction:
        if not validate_account_number(transaction['to_account']):
            errors.append("Invalid to_account format")
    
    # Amount validation
    if 'amount' in transaction:
        try:
            amount = float(transaction['amount'])
            if amount <= 0:
                errors.append("Amount must be positive")
        except (ValueError, TypeError):
            errors.append("Invalid amount format")
    
    # Timestamp validation
    if 'timestamp' in transaction:
        try:
            datetime.fromisoformat(transaction['timestamp'])
        except (ValueError, TypeError):
            errors.append("Invalid timestamp format")
    
    return errors

def validate_customer(customer: Dict) -> List[str]:
    """
    Validate customer information.
    Returns list of validation errors, empty list if valid.
    """
    errors = []
    
    # Required fields
    required_fields = ['personnummer', 'name', 'address', 'phone']
    for field in required_fields:
        if field not in customer:
            errors.append(f"Missing required field: {field}")
    
    # Personnummer validation
    if 'personnummer' in customer:
        if not validate_personnummer(customer['personnummer']):
            errors.append("Invalid personnummer format")
    
    # Phone number validation
    if 'phone' in customer:
        phone = customer['phone']
        if not isinstance(phone, str) or not phone.replace('+', '').replace('-', '').isdigit():
            errors.append("Invalid phone number format")
    
    return errors 