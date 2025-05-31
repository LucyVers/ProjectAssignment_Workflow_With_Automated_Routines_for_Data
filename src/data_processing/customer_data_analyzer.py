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
            'data_quality': self.check_data_quality(),
            'duplicate_personnummer': self.analyze_duplicate_personnummer(),
            'age_verification': self.analyze_age_verification(),
            'address_validation': self.analyze_address_validation(),
            'phone_numbers': self.analyze_phone_numbers()
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
    
    def analyze_duplicate_personnummer(self) -> Dict:
        """Analyze patterns in duplicate personnummer"""
        duplicates = defaultdict(list)
        patterns = defaultdict(int)
        risks = defaultdict(list)
        
        # Find all duplicates
        dup_series = self.df['Personnummer'].value_counts()
        duplicate_pnrs = dup_series[dup_series > 1]
        
        # Analyze each duplicate
        for pnr, count in duplicate_pnrs.items():
            # Get all records for this personnummer
            records = self.df[self.df['Personnummer'] == pnr]
            
            # Store basic info
            duplicates[pnr] = {
                'count': count,
                'records': records.to_dict('records'),
                'unique_names': records['Customer'].unique().tolist(),
                'unique_addresses': records['Address'].unique().tolist(),
                'unique_phones': records['Phone'].unique().tolist(),
                'accounts': records['BankAccount'].tolist()
            }
            
            # Analyze patterns
            if len(records['Customer'].unique()) > 1:
                patterns['different_names'] += 1
                risks[pnr].append('Multiple names for same personnummer')
            
            if len(records['Address'].unique()) > 1:
                patterns['different_addresses'] += 1
                risks[pnr].append('Multiple addresses for same personnummer')
            
            if len(records['Phone'].unique()) > 1:
                patterns['different_phones'] += 1
                risks[pnr].append('Multiple phone numbers for same personnummer')
            
            # Check for age-related patterns
            birth_year = int(pnr[:2])
            current_year = pd.Timestamp.now().year % 100
            age = current_year - birth_year if birth_year <= current_year else 100 + current_year - birth_year
            
            if age < 18:
                patterns['underage'] += 1
                risks[pnr].append('Underage customer with multiple accounts')
            
            if count > 3:
                patterns['high_account_count'] += 1
                risks[pnr].append(f'High number of accounts ({count})')
        
        return {
            'total_duplicates': len(duplicate_pnrs),
            'duplicates': dict(duplicates),
            'patterns': dict(patterns),
            'risks': {k: v for k, v in risks.items() if v},  # Only include entries with risks
            'summary': {
                'total_records_affected': sum(duplicate_pnrs),
                'average_duplicates_per_pnr': sum(duplicate_pnrs) / len(duplicate_pnrs),
                'max_duplicates': max(duplicate_pnrs),
                'pattern_distribution': dict(patterns)
            }
        }
    
    def analyze_age_verification(self) -> Dict:
        """Analyze age-related cases and verify compliance"""
        age_analysis = {
            'underage_cases': defaultdict(list),
            'age_groups': defaultdict(int),
            'risk_levels': defaultdict(list),
            'guardian_status': defaultdict(list)
        }
        
        current_year = pd.Timestamp.now().year % 100
        
        for _, row in self.df.iterrows():
            pnr = row['Personnummer']
            birth_year = int(pnr[:2])
            
            # Calculate age
            age = current_year - birth_year if birth_year <= current_year else 100 + current_year - birth_year
            
            # Analyze underage cases
            if age < 18:
                case_info = {
                    'personnummer': pnr,
                    'age': age,
                    'customer_name': row['Customer'],
                    'account': row['BankAccount'],
                    'address': row['Address']
                }
                
                # Categorize by age group
                if age < 13:
                    age_analysis['age_groups']['under_13'] += 1
                    age_analysis['risk_levels']['high'].append(pnr)
                elif age < 16:
                    age_analysis['age_groups']['13_to_15'] += 1
                    age_analysis['risk_levels']['medium'].append(pnr)
                else:
                    age_analysis['age_groups']['16_to_17'] += 1
                    age_analysis['risk_levels']['low'].append(pnr)
                
                age_analysis['underage_cases'][pnr].append(case_info)
                
                # Check for guardian indicators in address
                has_guardian = bool(re.search(r'c/o|C/O|care of|guardian of', row['Address'], re.IGNORECASE))
                if has_guardian:
                    age_analysis['guardian_status']['with_guardian'].append(pnr)
                else:
                    age_analysis['guardian_status']['no_guardian'].append(pnr)
        
        # Add summary statistics
        age_analysis['summary'] = {
            'total_underage': sum(len(cases) for cases in age_analysis['underage_cases'].values()),
            'age_group_distribution': dict(age_analysis['age_groups']),
            'risk_level_distribution': {
                level: len(cases) for level, cases in age_analysis['risk_levels'].items()
            },
            'guardian_status_distribution': {
                status: len(cases) for status, cases in age_analysis['guardian_status'].items()
            }
        }
        
        return age_analysis
    
    def analyze_address_validation(self) -> Dict:
        """Analyze address formats and validate against standards"""
        address_analysis = {
            'postal_codes': defaultdict(list),
            'cities': defaultdict(list),
            'format_issues': defaultdict(int),
            'geographic_patterns': defaultdict(int)
        }
        
        # Swedish postal code regex pattern (5 digits)
        postal_code_pattern = re.compile(r'^\d{5}$')
        
        for _, row in self.df.iterrows():
            address = row['Address']
            
            # Extract postal code and city
            match = re.search(r'(\d{5})\s+([^,]+)$', address)
            if match:
                postal_code = match.group(1)
                city = match.group(2).strip()
                
                # Validate postal code format
                if not postal_code_pattern.match(postal_code):
                    address_analysis['format_issues']['invalid_postal_code'] += 1
                    address_analysis['postal_codes']['invalid'].append({
                        'postal_code': postal_code,
                        'address': address,
                        'customer': row['Customer'],
                        'personnummer': row['Personnummer']
                    })
                
                # Check city name format and common issues
                if not city.isalpha():
                    address_analysis['format_issues']['invalid_city_chars'] += 1
                if any(char.islower() for char in city):
                    address_analysis['format_issues']['lowercase_city'] += 1
                
                address_analysis['cities']['all'].append(city)
                
                # Geographic analysis based on postal code regions
                region = postal_code[:2]
                address_analysis['geographic_patterns'][region] += 1
            else:
                address_analysis['format_issues']['invalid_format'] += 1
        
        # Calculate statistics
        address_analysis['summary'] = {
            'total_addresses': len(self.df),
            'invalid_postal_codes': len(address_analysis['postal_codes']['invalid']),
            'unique_cities': len(set(address_analysis['cities']['all'])),
            'format_issues': dict(address_analysis['format_issues']),
            'geographic_distribution': dict(address_analysis['geographic_patterns'])
        }
        
        return address_analysis
    
    def analyze_phone_numbers(self) -> Dict:
        """Analyze phone number formats and propose standardization"""
        phone_analysis = {
            'formats': defaultdict(list),
            'patterns': defaultdict(int),
            'issues': defaultdict(list),
            'conversion_rules': defaultdict(list)
        }
        
        # Standard Swedish phone number patterns
        patterns = {
            'international': re.compile(r'^\+46\s*\(\d{1,4}\)\s*\d{3}\s*\d{2}\s*\d{2}$'),
            'local': re.compile(r'^\d{2,4}-\d{2,3}\s*\d{2}\s*\d{2}$'),
            'mobile': re.compile(r'^07\d{1,2}-\d{3}\s*\d{2}\s*\d{2}$')
        }
        
        for _, row in self.df.iterrows():
            phone = row['Phone'].strip()
            
            # Analyze format
            format_found = False
            for format_type, pattern in patterns.items():
                if pattern.match(phone):
                    phone_analysis['formats'][format_type].append({
                        'number': phone,
                        'customer': row['Customer'],
                        'personnummer': row['Personnummer']
                    })
                    format_found = True
                    break
            
            if not format_found:
                # Analyze non-standard format
                digits = ''.join(filter(str.isdigit, phone))
                phone_analysis['patterns'][len(digits)] += 1
                
                # Identify specific issues
                if len(digits) < 8:
                    phone_analysis['issues']['too_short'].append(phone)
                elif len(digits) > 12:
                    phone_analysis['issues']['too_long'].append(phone)
                
                # Create conversion rule
                if digits.startswith('0'):
                    if len(digits) == 10:  # Likely mobile or area code
                        phone_analysis['conversion_rules']['local_to_international'].append({
                            'original': phone,
                            'converted': f'+46 ({digits[1:3]}) {digits[3:6]} {digits[6:8]} {digits[8:]}'
                        })
        
        # Calculate statistics
        phone_analysis['summary'] = {
            'total_numbers': len(self.df),
            'standard_format': sum(len(numbers) for numbers in phone_analysis['formats'].values()),
            'non_standard': len(self.df) - sum(len(numbers) for numbers in phone_analysis['formats'].values()),
            'format_distribution': {
                format_type: len(numbers) for format_type, numbers in phone_analysis['formats'].items()
            },
            'digit_length_distribution': dict(phone_analysis['patterns'])
        }
        
        return phone_analysis
    
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

    print("\nDuplicate Personnummer Analysis:")
    print("------------------------------")
    for pattern, count in results['duplicate_personnummer']['patterns'].items():
        print(f"\n{pattern}: {count} instances")
    
    print("\nRisks:")
    for pnr, risks in results['duplicate_personnummer']['risks'].items():
        print(f"\nPersonnummer: {pnr}")
        for risk in risks:
            print(f"  - {risk}")
    
    print("\nSummary:")
    for key, value in results['duplicate_personnummer']['summary'].items():
        print(f"{key}: {value}")

    print("\nAge Verification Analysis:")
    print("-------------------------")
    for key, value in results['age_verification']['summary'].items():
        print(f"{key}: {value}")

    print("\nAddress Validation Analysis:")
    print("----------------------------")
    for key, value in results['address_validation']['summary'].items():
        print(f"{key}: {value}")

    print("\nPhone Numbers Analysis:")
    print("----------------------")
    for key, value in results['phone_numbers']['summary'].items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main() 