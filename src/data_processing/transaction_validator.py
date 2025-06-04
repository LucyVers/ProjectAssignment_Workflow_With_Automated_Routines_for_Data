"""
Transaction validation module implementing the rules defined in validation_rules.md
"""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class TransactionValidator:
    def __init__(self):
        # Transaction amount limits
        self.MIN_AMOUNT = Decimal('1.00')  # 1 SEK
        self.MAX_PRIVATE_DAILY = Decimal('50000.00')  # 50,000 SEK
        self.MAX_BUSINESS_DAILY = Decimal('500000.00')  # 500,000 SEK
        self.SALARY_MIN = Decimal('20000.00')
        self.SALARY_MAX = Decimal('80000.00')
        
        # Transaction frequency limits
        self.MAX_DAILY_PRIVATE = 10
        self.MAX_DAILY_BUSINESS = 30
        self.MIN_TIME_BETWEEN = timedelta(minutes=1)
        
        # International transfer limits
        self.MAX_INTERNATIONAL_MONTHLY = 3
        self.INTERNATIONAL_AMOUNT_LIMIT = Decimal('15000.00')
        self.INTERNATIONAL_MONTHLY_LIMIT = Decimal('150000.00')

    def validate_transaction(self, transaction: Dict) -> List[str]:
        """
        Validates a single transaction against all rules.
        Returns a list of validation errors, empty list if valid.
        """
        errors = []
        
        # Basic validation
        errors.extend(self._validate_amount(transaction))
        errors.extend(self._validate_currency(transaction))
        errors.extend(self._validate_accounts(transaction))
        
        # Business rule validation
        errors.extend(self._validate_transaction_type(transaction))
        errors.extend(self._validate_frequency(transaction))
        
        # International transfer validation
        if self._is_international(transaction):
            errors.extend(self._validate_international(transaction))
        
        return errors

    def _validate_amount(self, transaction: Dict) -> List[str]:
        """Validates transaction amount."""
        errors = []
        amount = Decimal(str(transaction.get('amount', 0)))
        
        if amount < self.MIN_AMOUNT:
            errors.append(f"Transaction amount {amount} SEK is below minimum {self.MIN_AMOUNT} SEK")
            
        if transaction.get('account_type') == 'private':
            if amount > self.MAX_PRIVATE_DAILY:
                errors.append(f"Transaction amount {amount} SEK exceeds private daily limit {self.MAX_PRIVATE_DAILY} SEK")
        else:  # business
            if amount > self.MAX_BUSINESS_DAILY:
                errors.append(f"Transaction amount {amount} SEK exceeds business daily limit {self.MAX_BUSINESS_DAILY} SEK")
                
        return errors

    def _validate_currency(self, transaction: Dict) -> List[str]:
        """Validates transaction currency."""
        errors = []
        currency = transaction.get('currency', '').upper()
        
        if not currency:
            errors.append("Currency is required")
        elif currency not in ['SEK', 'EUR', 'USD', 'DKK', 'NOK', 'GBP', 'JPY', 'RMB', 'ZAR', 'ZMW']:
            errors.append(f"Unsupported currency: {currency}")
            
        return errors

    def _validate_accounts(self, transaction: Dict) -> List[str]:
        """Validates sender and receiver account numbers."""
        errors = []
        
        # Account number format: SE8902XXXX[14 digits]
        account_pattern = r'^SE8902[A-Z]{4}\d{14}$'
        
        sender = transaction.get('sender_account', '')
        receiver = transaction.get('receiver_account', '')
        
        if not sender or not receiver:
            errors.append("Both sender and receiver accounts are required")
            return errors
            
        import re
        if not re.match(account_pattern, sender):
            errors.append(f"Invalid sender account format: {sender}")
        if not re.match(account_pattern, receiver):
            errors.append(f"Invalid receiver account format: {receiver}")
            
        return errors

    def _validate_transaction_type(self, transaction: Dict) -> List[str]:
        """Validates transaction type."""
        errors = []
        valid_types = ['incoming', 'outgoing']
        
        t_type = transaction.get('transaction_type', '').lower()
        if not t_type:
            errors.append("Transaction type is required")
        elif t_type not in valid_types:
            errors.append(f"Invalid transaction type: {t_type}")
            
        return errors

    def _validate_frequency(self, transaction: Dict) -> List[str]:
        """Validates transaction frequency."""
        # This would typically check against a database of recent transactions
        # For now, we'll just validate the transaction timestamp
        errors = []
        
        timestamp = transaction.get('timestamp')
        if not timestamp:
            errors.append("Transaction timestamp is required")
            
        return errors

    def _is_international(self, transaction: Dict) -> bool:
        """Determines if a transaction is international."""
        sender_country = transaction.get('sender_country', 'Sweden')
        receiver_country = transaction.get('receiver_country', 'Sweden')
        
        return sender_country != 'Sweden' or receiver_country != 'Sweden'

    def _validate_international(self, transaction: Dict) -> List[str]:
        """Validates international transaction specific rules."""
        errors = []
        amount = Decimal(str(transaction.get('amount', 0)))
        
        if amount > self.INTERNATIONAL_AMOUNT_LIMIT:
            errors.append(
                f"International transaction amount {amount} SEK exceeds limit "
                f"{self.INTERNATIONAL_AMOUNT_LIMIT} SEK"
            )
            
        return errors 