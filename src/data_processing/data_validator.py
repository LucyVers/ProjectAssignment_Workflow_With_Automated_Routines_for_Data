import pandas as pd
import re
from datetime import datetime
from typing import Dict, List, Set, Tuple

class DataValidator:
    def __init__(self, data_file: str):
        """Initialize validator with data file path"""
        self.df = pd.read_csv(data_file)
        self.validation_results = {
            'personnummer': {},
            'address': {},
            'phone': {}
        }

    def validate_all(self) -> Dict:
        """Run all validations and return results"""
        self.validate_personnummer()
        self.validate_addresses()
        self.validate_phone_numbers()
        return self.validation_results

    def validate_personnummer(self) -> None:
        """Validate Swedish personal identity numbers"""
        results = {
            'invalid_check_digits': [],
            'invalid_dates': [],
            'unreasonable_ages': [],
            'duplicates': []
        }
        
        # Get unique personnummer to check for duplicates
        unique_pnr = self.df['Personnummer'].unique()
        if len(unique_pnr) < len(self.df['Personnummer']):
            results['duplicates'] = self.df[self.df['Personnummer'].duplicated()]['Personnummer'].tolist()

        for pnr in unique_pnr:
            # Split into date and number parts
            date_part = pnr.split('-')[0]
            number_part = pnr.split('-')[1]
            
            # Validate date
            try:
                year = int('19' + date_part[:2])  # Assuming 1900s for now
                month = int(date_part[2:4])
                day = int(date_part[4:6])
                date = datetime(year, month, day)
                
                # Check age reasonability (15-120 years)
                age = (datetime.now() - date).days / 365.25
                if age < 15 or age > 120:
                    results['unreasonable_ages'].append(pnr)
            except ValueError:
                results['invalid_dates'].append(pnr)

            # Validate check digit
            if not self._verify_personnummer_check_digit(pnr):
                results['invalid_check_digits'].append(pnr)

        self.validation_results['personnummer'] = results

    def validate_addresses(self) -> None:
        """Validate Swedish addresses"""
        results = {
            'invalid_postal_codes': [],
            'invalid_cities': [],
            'format_issues': []
        }
        
        # Load Swedish postal codes (to be implemented)
        valid_postal_codes = self._load_swedish_postal_codes()
        valid_cities = self._load_swedish_cities()

        for _, row in self.df.iterrows():
            address = row['Address']
            
            # Check format: "street, postal_code city"
            match = re.match(r'^([^,]+),\s*(\d{5})\s+(.+)$', address)
            if not match:
                results['format_issues'].append(address)
                continue
            
            street, postal_code, city = match.groups()
            
            # Validate postal code
            if postal_code not in valid_postal_codes:
                results['invalid_postal_codes'].append(f"{postal_code} ({address})")
            
            # Validate city
            if city not in valid_cities:
                results['invalid_cities'].append(f"{city} ({address})")

        self.validation_results['address'] = results

    def validate_phone_numbers(self) -> None:
        """Validate and categorize phone numbers"""
        results = {
            'formats': {
                'international': [],
                'local': [],
                'other': []
            },
            'invalid': [],
            'standardization_needed': []
        }

        for phone in self.df['Phone'].unique():
            if re.match(r'^\+46 \(0\)\d{3} \d{3} \d{2}$', phone):
                results['formats']['international'].append(phone)
            elif re.match(r'^\d{3}-\d{3} \d{2} \d{2}$', phone):
                results['formats']['local'].append(phone)
            else:
                results['formats']['other'].append(phone)
                results['standardization_needed'].append(phone)

        self.validation_results['phone'] = results

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

def main():
    """Main function to run validations"""
    validator = DataValidator('data/working/sebank_customers_with_accounts.csv')
    results = validator.validate_all()
    
    print("\n=== VALIDATION RESULTS ===\n")
    
    print("Personnummer Validation:")
    print("----------------------")
    for issue, items in results['personnummer'].items():
        print(f"\n{issue.replace('_', ' ').title()}:")
        if items:
            print(f"Found {len(items)} issues:")
            for item in items[:5]:  # Show first 5 examples
                print(f"  - {item}")
            if len(items) > 5:
                print(f"  ... and {len(items)-5} more")
        else:
            print("No issues found")
    
    print("\nAddress Validation:")
    print("-----------------")
    for issue, items in results['address'].items():
        print(f"\n{issue.replace('_', ' ').title()}:")
        if items:
            print(f"Found {len(items)} issues:")
            for item in items[:5]:  # Show first 5 examples
                print(f"  - {item}")
            if len(items) > 5:
                print(f"  ... and {len(items)-5} more")
        else:
            print("No issues found")
    
    print("\nPhone Number Analysis:")
    print("-------------------")
    formats = results['phone']['formats']
    print("\nFormat Distribution:")
    for format_type, numbers in formats.items():
        print(f"{format_type.title()}: {len(numbers)} numbers")
    
    if results['phone']['standardization_needed']:
        print(f"\nNumbers Needing Standardization: {len(results['phone']['standardization_needed'])}")
        print("Examples:")
        for number in results['phone']['standardization_needed'][:5]:
            print(f"  - {number}")
        if len(results['phone']['standardization_needed']) > 5:
            print(f"  ... and {len(results['phone']['standardization_needed'])-5} more")

if __name__ == "__main__":
    main() 