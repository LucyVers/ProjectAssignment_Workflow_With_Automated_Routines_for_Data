import pandas as pd
import re
from datetime import datetime
from typing import Dict, List, Set, Tuple

class DataValidator:
    def __init__(self, data: str | pd.DataFrame):
        """Initialize validator with data file path or DataFrame"""
        if isinstance(data, str):
            self.df = pd.read_csv(data)
        else:
            self.df = data
        self.validation_results = {
            'personnummer': {},
            'address': {},
            'phone': {},
            'account_numbers': {}
        }

    def validate_all(self) -> Dict:
        """Run all validations and return results"""
        self.validate_personnummer()
        self.validate_addresses()
        self.validate_phone_numbers()
        self.validate_account_numbers()
        return self.validation_results

    def validate_personnummer(self) -> None:
        """Validate Swedish personal identity numbers"""
        results = {
            'invalid_check_digits': [],
            'invalid_dates': [],
            'unreasonable_ages': [],
            'duplicates': [],
            'missing_guardian_info': [],
            'invalid_guardian_info': []
        }
        
        # Get unique personnummer to check for duplicates
        unique_pnr = self.df['Personnummer'].unique()
        if len(unique_pnr) < len(self.df['Personnummer']):
            results['duplicates'] = self.df[self.df['Personnummer'].duplicated()]['Personnummer'].tolist()

        for idx, row in self.df.iterrows():
            pnr = row['Personnummer']
            # Split into date and number parts
            date_part = pnr.split('-')[0]
            number_part = pnr.split('-')[1]
            
            # Validate date
            try:
                year = int('19' + date_part[:2])  # Assuming 1900s for now
                month = int(date_part[2:4])
                day = int(date_part[4:6])
                date = datetime(year, month, day)
                
                # Calculate age
                age = (datetime.now() - date).days / 365.25
                
                # Check for minors (under 18)
                if age < 18:
                    guardian_info = row.get('guardian_info', None)
                    if guardian_info is None or pd.isna(guardian_info) or str(guardian_info).strip() == '':
                        results['missing_guardian_info'].append({
                            'personnummer': pnr,
                            'age': round(age, 1)
                        })
                    elif not self._validate_guardian_info(guardian_info):
                        results['invalid_guardian_info'].append({
                            'personnummer': pnr,
                            'guardian_info': guardian_info
                        })
                
                # Check age reasonability (15-120 years)
                if age < 15 or age > 120:
                    results['unreasonable_ages'].append(pnr)
            except ValueError:
                results['invalid_dates'].append(pnr)

            # Validate check digit
            if not self._verify_personnummer_check_digit(pnr):
                results['invalid_check_digits'].append(pnr)

        self.validation_results['personnummer'] = results

    def validate_addresses(self) -> None:
        """Validate both Swedish and international addresses in our bank data"""
        results = {
            'invalid_format': [],
            'missing_postal_code': [],
            'invalid_postal_code_format': {
                'swedish': [],    # Swedish postal codes must be exactly 5 digits
                'international': []  # Other formats depend on country
            },
            'missing_city': [],
            'missing_country': [],
            'address_stats': {
                'swedish': 0,
                'international': 0
            }
        }

        for _, row in self.df.iterrows():
            address = row['Address']
            country = row.get('Country', '').strip()
            
            # Check if we have country information
            if not country:
                results['missing_country'].append(address)
                continue

            # Basic format check: should contain comma
            if ',' not in address:
                results['invalid_format'].append(f"Missing comma: {address}")
                continue
            
            # Split into parts
            street_part, location_part = address.split(',', 1)
            location_part = location_part.strip()

            # Different validation for Swedish vs international addresses
            if country.lower() in ['sweden', 'sverige', 'se']:
                results['address_stats']['swedish'] += 1
                
                # Check postal code format (5 digits) for Swedish addresses
                postal_code_match = re.search(r'\b\d{5}\b', location_part)
                if not postal_code_match:
                    results['missing_postal_code'].append(address)
                    continue
                
                postal_code = postal_code_match.group()
                
                # Validate exact format for Swedish postal codes
                if not re.match(r'^\d{5}$', postal_code):
                    results['invalid_postal_code_format']['swedish'].append(
                        f"Invalid Swedish format: {postal_code} in {address}"
                    )
            else:
                results['address_stats']['international'] += 1
                
                # For international addresses, just verify some kind of postal code exists
                if not re.search(r'\b[\w\d]+\b', location_part):
                    results['missing_postal_code'].append(address)
            
            # Check city exists (for all addresses)
            city_part = re.sub(r'\b[\w\d-]+\b', '', location_part).strip()
            if not city_part:
                results['missing_city'].append(address)

        self.validation_results['address'] = results

    def validate_phone_numbers(self) -> None:
        """Validate and standardize phone numbers"""
        results = {
            'formats': {
                'international': [],  # +46 (0)XXX XXX XX XX
                'local': [],         # 0XX-XXX XX XX
                'other': []          # Any other format
            },
            'invalid': [],
            'standardization': {
                'original_to_standard': {},  # Maps original numbers to standardized format
                'failed_standardization': []
            }
        }

        for phone in self.df['Phone'].unique():
            if not isinstance(phone, str):
                results['invalid'].append(f"Not a string: {phone}")
                continue

            # Clean the number first
            cleaned = self._clean_phone_number(phone)
            
            # Try to standardize
            try:
                standardized = self._standardize_phone_number(cleaned)
                if standardized:
                    results['standardization']['original_to_standard'][phone] = standardized
                    
                    # Categorize the original format
                    if re.match(r'^\+46 \(0\)\d{3} \d{3} \d{2} \d{2}$', phone):
                        results['formats']['international'].append(phone)
                    elif re.match(r'^\d{3}-\d{3} \d{2} \d{2}$', phone):
                        results['formats']['local'].append(phone)
                    else:
                        results['formats']['other'].append(phone)
                else:
                    results['standardization']['failed_standardization'].append(phone)
            except ValueError as e:
                results['invalid'].append(f"{phone}: {str(e)}")

        self.validation_results['phone'] = results

    def _clean_phone_number(self, phone: str) -> str:
        """Remove all non-digit characters except + from phone number"""
        # Keep + for international format
        if phone.startswith('+'):
            cleaned = '+' + ''.join(c for c in phone[1:] if c.isdigit())
        else:
            cleaned = ''.join(c for c in phone if c.isdigit())
        return cleaned

    def _standardize_phone_number(self, phone: str) -> str:
        """
        Standardize phone number to international format: +46 (0)XXX XXX XX XX
        Returns standardized number or None if cannot be standardized
        """
        # Remove any remaining spaces or special characters
        digits = self._clean_phone_number(phone)
        
        # Handle different cases
        if digits.startswith('+46'):
            # Already international format, just need formatting
            national_number = digits[3:]  # Remove +46
        elif digits.startswith('00'):
            # International format starting with 00
            national_number = digits[4:]  # Remove 0046
        elif digits.startswith('0'):
            # National format
            national_number = digits[1:]  # Remove leading 0
        else:
            # Assume it's a national number without leading 0
            national_number = digits

        # Validate length (Swedish numbers should be 9 digits without country code)
        if len(national_number) != 9:
            raise ValueError(f"Invalid length for Swedish phone number: {len(national_number)} digits")

        # Format to standard: +46 (0)XXX XXX XX XX
        return f"+46 (0){national_number[:3]} {national_number[3:6]} {national_number[6:8]} {national_number[8:]}"

    def validate_account_numbers(self) -> None:
        """Validate bank account numbers."""
        results = {
            'invalid_format': [],
            'duplicates': []
        }
        
        # Get unique account numbers
        unique_accounts = self.df['BankAccount'].unique()
        
        # Check for duplicates
        if len(unique_accounts) < len(self.df['BankAccount']):
            results['duplicates'] = self.df[self.df['BankAccount'].duplicated()]['BankAccount'].tolist()
        
        # Validate format for each unique account
        for account in unique_accounts:
            if not self._validate_account_format(account):
                results['invalid_format'].append(account)
                
        self.validation_results['account_numbers'] = results

    @staticmethod
    def _verify_personnummer_check_digit(pnr: str) -> bool:
        """Verify the check digit of a Swedish personal identity number"""
        # Remove hyphen and get first 9 digits
        digits = pnr.replace('-', '')
        if len(digits) != 10:
            return False
        
        # Calculate check digit
        sum = 0
        for i in range(9):
            digit = int(digits[i])
            if i % 2 == 0:
                doubled = digit * 2
                sum += doubled // 10 + doubled % 10
            else:
                sum += digit
        
        check_digit = (10 - (sum % 10)) % 10
        return check_digit == int(digits[9])

    @staticmethod
    def _load_swedish_postal_codes() -> Set[str]:
        """Load valid Swedish postal codes"""
        # TODO: Implement loading from official source
        # For now, return a small test set
        return {'14010', '12345', '98765'}  # Example postal codes

    @staticmethod
    def _load_swedish_cities() -> Set[str]:
        """Load valid Swedish city names"""
        # TODO: Implement loading from official source
        # For now, return a small test set
        return {'Stockholm', 'Göteborg', 'Malmö', 'Uppsala', 'Gävle'}  # Example cities

    @staticmethod
    def _validate_guardian_info(guardian_info: str) -> bool:
        """
        Validate guardian information format.
        Expected format: 'Name: [Guardian Name], Relation: [Relation], Personnummer: [Guardian Personnummer]'
        """
        if not isinstance(guardian_info, str):
            return False
            
        # Check if all required fields are present
        required_fields = ['Name:', 'Relation:', 'Personnummer:']
        if not all(field in guardian_info for field in required_fields):
            return False
            
        # Extract guardian's personnummer and validate it
        match = re.search(r'Personnummer:\s*(\d{6}-\d{4})', guardian_info)
        if not match:
            return False
            
        guardian_pnr = match.group(1)
        # Validate guardian's personnummer format
        if not re.match(r'^\d{6}-\d{4}$', guardian_pnr):
            return False
            
        # Extract relation and validate
        match = re.search(r'Relation:\s*(\w+)', guardian_info)
        if not match:
            return False
            
        relation = match.group(1).lower()
        valid_relations = {'parent', 'guardian', 'mother', 'father', 'förälder', 'vårdnadshavare'}
        if relation not in valid_relations:
            return False
            
        return True

    def _validate_account_format(self, account: str) -> bool:
        """Validate bank account number format."""
        if not isinstance(account, str):
            return False
            
        # Check length
        if len(account) != 24:  # SE8902 + 4 letters + 14 digits = 24
            return False
            
        # Validate format using regex
        if not re.match(r'^SE8902[A-Z]{4}\d{14}$', account):
            return False
            
        return True

def main():
    """Main function to run validations"""
    validator = DataValidator('data/working/sebank_customers_with_accounts.csv')
    results = validator.validate_all()
    
    print("\n=== VALIDATION RESULTS ===\n")
    
    # Print personnummer results
    print("Personnummer Validation:")
    print("----------------------")
    for issue, items in results['personnummer'].items():
        print(f"\n{issue.replace('_', ' ').title()}:")
        if items:
            print(f"Found {len(items)} issues:")
            if isinstance(items, list) and items and isinstance(items[0], dict):
                # Handle dictionary results (guardian info)
                for item in items[:5]:
                    if 'age' in item:
                        print(f"  - {item['personnummer']} (Age: {item['age']} years)")
                    elif 'guardian_info' in item:
                        print(f"  - {item['personnummer']} (Guardian Info: {item['guardian_info']})")
            else:
                # Handle simple list results
                for item in items[:5]:
                    print(f"  - {item}")
            if len(items) > 5:
                print(f"  ... and {len(items)-5} more")
        else:
            print("No issues found")
    
    # Print address validation results
    print("\nAddress Validation:")
    print("-----------------")
    for issue, items in results['address'].items():
        print(f"\n{issue.replace('_', ' ').title()}:")
        if items:
            print(f"Found {len(items)} issues:")
            for item in items[:5]:
                print(f"  - {item}")
            if len(items) > 5:
                print(f"  ... and {len(items)-5} more")
        else:
            print("No issues found")
    
    # Print phone validation results
    print("\nPhone Number Analysis:")
    print("-------------------")
    
    # Print format distribution
    print("\nFormat Distribution:")
    for format_type, numbers in results['phone']['formats'].items():
        print(f"{format_type.title()}: {len(numbers)} numbers")
        if numbers:
            print("Examples:")
            for number in numbers[:3]:
                standardized = results['phone']['standardization']['original_to_standard'].get(number, "Failed to standardize")
                print(f"  - {number} -> {standardized}")

    # Print standardization results
    print("\nStandardization Results:")
    failed = results['phone']['standardization']['failed_standardization']
    if failed:
        print(f"\nFailed to standardize {len(failed)} numbers:")
        for number in failed[:5]:
            print(f"  - {number}")
        if len(failed) > 5:
            print(f"  ... and {len(failed)-5} more")

    # Print invalid numbers
    invalid = results['phone']['invalid']
    if invalid:
        print(f"\nInvalid numbers found: {len(invalid)}")
        for entry in invalid[:5]:
            print(f"  - {entry}")
        if len(invalid) > 5:
            print(f"  ... and {len(invalid)-5} more")

    # Print account number validation results
    print("\nAccount Number Validation:")
    print("----------------------")
    for issue, items in results['account_numbers'].items():
        print(f"\n{issue.replace('_', ' ').title()}:")
        if items:
            print(f"Found {len(items)} issues:")
            for item in items[:5]:
                print(f"  - {item}")
            if len(items) > 5:
                print(f"  ... and {len(items)-5} more")
        else:
            print("No issues found")

if __name__ == "__main__":
    main() 