import pandas as pd
import re
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class CustomerDataAnalyzer:
    def __init__(self, file_path: str):
        self.df = pd.read_csv(file_path)
        self.total_rows = len(self.df)
        self.unique_customers = len(self.df['Personnummer'].unique())
        
    def analyze_all(self) -> Dict:
        """Run all analysis and return comprehensive results"""
        return {
            'basic_stats': self.get_basic_stats(),
            'format_analysis': self.analyze_formats(),
            'consistency_check': self.check_consistency(),
            'relationship_analysis': self.analyze_relationships(),
            'data_quality': self.check_data_quality()
        }
    
    def get_basic_stats(self) -> Dict:
        """Get basic statistics about the dataset"""
        return {
            'total_rows': self.total_rows,
            'unique_customers': self.unique_customers,
            'avg_accounts_per_customer': self.total_rows / self.unique_customers,
            'fields': list(self.df.columns)
        }
    
    def analyze_formats(self) -> Dict:
        """Analyze format patterns in each field"""
        formats = {
            'personnummer_patterns': set(),
            'phone_patterns': set(),
            'address_patterns': set(),
            'account_patterns': set()
        }
        
        for _, row in self.df.iterrows():
            # Personnummer format
            formats['personnummer_patterns'].add(
                self._categorize_personnummer(row['Personnummer'])
            )
            
            # Phone format
            formats['phone_patterns'].add(
                self._categorize_phone(row['Phone'])
            )
            
            # Address format
            formats['address_patterns'].add(
                self._categorize_address(row['Address'])
            )
            
            # Bank account format
            formats['account_patterns'].add(
                self._categorize_account(row['BankAccount'])
            )
        
        return formats
    
    def check_consistency(self) -> Dict:
        """Check data consistency across records"""
        consistency = defaultdict(list)
        
        # Group by personnummer and check consistency
        for personnummer, group in self.df.groupby('Personnummer'):
            # Check customer name consistency
            if len(group['Customer'].unique()) > 1:
                consistency['inconsistent_names'].append(personnummer)
            
            # Check address consistency
            if len(group['Address'].unique()) > 1:
                consistency['inconsistent_addresses'].append(personnummer)
            
            # Check phone consistency
            if len(group['Phone'].unique()) > 1:
                consistency['inconsistent_phones'].append(personnummer)
        
        return dict(consistency)
    
    def analyze_relationships(self) -> Dict:
        """Analyze customer-account relationships"""
        relationships = {
            'accounts_per_customer': {},
            'duplicate_accounts': set(),
            'shared_accounts': set()
        }
        
        # Count accounts per customer
        account_counts = self.df.groupby('Personnummer')['BankAccount'].count()
        relationships['accounts_per_customer'] = account_counts.to_dict()
        
        # Check for duplicate accounts
        account_customers = self.df.groupby('BankAccount')['Personnummer'].apply(list)
        for account, customers in account_customers.items():
            if len(customers) > 1:
                relationships['shared_accounts'].add(account)
        
        return relationships
    
    def check_data_quality(self) -> Dict:
        """Check various data quality aspects"""
        quality = {
            'missing_values': self.df.isnull().sum().to_dict(),
            'invalid_formats': defaultdict(list),
            'suspicious_patterns': defaultdict(list)
        }
        
        # Check personnummer format
        invalid_personnummer = self.df[~self.df['Personnummer'].str.match(r'^\d{6}-\d{4}$')]
        quality['invalid_formats']['personnummer'] = invalid_personnummer['Personnummer'].tolist()
        
        # Check bank account format
        invalid_accounts = self.df[~self.df['BankAccount'].str.match(r'^SE8902[A-Z]{4}\d{14}$')]
        quality['invalid_formats']['bank_accounts'] = invalid_accounts['BankAccount'].tolist()
        
        # Check for suspicious patterns
        # Example: Same phone number for different customers
        phone_customers = self.df.groupby('Phone')['Personnummer'].nunique()
        suspicious_phones = phone_customers[phone_customers > 1]
        quality['suspicious_patterns']['shared_phones'] = suspicious_phones.to_dict()
        
        return quality
    
    @staticmethod
    def _categorize_personnummer(pnr: str) -> str:
        """Analyze personnummer format"""
        if re.match(r'^\d{6}-\d{4}$', pnr):
            return 'YYMMDD-XXXX'
        return 'invalid'
    
    @staticmethod
    def _categorize_phone(phone: str) -> str:
        """Analyze phone number format"""
        if re.match(r'^\+46 \(0\)\d{3} \d{3} \d{2}$', phone):
            return 'international'
        if re.match(r'^\d{3}-\d{3} \d{2} \d{2}$', phone):
            return 'local'
        return 'other'
    
    @staticmethod
    def _categorize_address(addr: str) -> str:
        """Analyze address format"""
        if re.match(r'^[^,]+, \d{5} [^,]+$', addr):
            return 'street, postal city'
        return 'other'
    
    @staticmethod
    def _categorize_account(account: str) -> str:
        """Analyze bank account format"""
        if re.match(r'^SE8902[A-Z]{4}\d{14}$', account):
            return 'SE8902XXXX[14 digits]'
        return 'invalid'

def main():
    # Initialize analyzer
    analyzer = CustomerDataAnalyzer('data/working/sebank_customers_with_accounts.csv')
    
    # Run analysis
    results = analyzer.analyze_all()
    
    # Print results in a structured format
    print("\n=== CUSTOMER DATA ANALYSIS RESULTS ===\n")
    
    print("Basic Statistics:")
    print("-----------------")
    for key, value in results['basic_stats'].items():
        print(f"{key}: {value}")
    
    print("\nFormat Analysis:")
    print("---------------")
    for category, patterns in results['format_analysis'].items():
        print(f"\n{category}:")
        for pattern in patterns:
            print(f"  - {pattern}")
    
    print("\nConsistency Check:")
    print("----------------")
    for issue, items in results['consistency_check'].items():
        print(f"\n{issue}:")
        print(f"  - Found {len(items)} instances")
    
    print("\nRelationship Analysis:")
    print("--------------------")
    print("\nAccounts per customer:")
    for personnummer, count in results['relationship_analysis']['accounts_per_customer'].items():
        print(f"  Customer {personnummer}: {count} accounts")
    print(f"\nShared accounts: {len(results['relationship_analysis']['shared_accounts'])}")
    
    print("\nData Quality Check:")
    print("-----------------")
    print("\nMissing values:")
    for field, count in results['data_quality']['missing_values'].items():
        if count > 0:
            print(f"  {field}: {count}")
    
    print("\nInvalid formats:")
    for field, items in results['data_quality']['invalid_formats'].items():
        if items:
            print(f"\n  {field}: {len(items)} invalid entries")
    
    print("\nSuspicious patterns:")
    for pattern, instances in results['data_quality']['suspicious_patterns'].items():
        if instances:
            print(f"\n  {pattern}: {len(instances)} instances")

if __name__ == "__main__":
    main() 