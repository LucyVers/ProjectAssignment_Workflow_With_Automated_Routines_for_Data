"""
Simple test to validate customer data without database interaction.
"""
import pandas as pd
from pathlib import Path
from data_validator import DataValidator
import json

def test_customer_validation():
    print("Starting customer validation test...")
    
    try:
        # Load customer data
        print("\nLoading customer data...")
        customers_path = "data/working/sebank_customers_with_accounts.csv"
        if not Path(customers_path).exists():
            print(f"Error: Cannot find {customers_path}")
            return
            
        # Load data and take first 100 customers
        df = pd.read_csv(customers_path)
        df_100 = df.head(100)
        print(f"Loaded {len(df)} customers, testing first 100")
        
        # Initialize validator with first 100 customers
        validator = DataValidator(df_100)
        
        # Run all validations
        print("\nRunning all validations...")
        results = validator.validate_all()
        
        # Print results for each validation type
        print("\n=== VALIDATION RESULTS ===")
        
        # Personnummer validation results
        print("\n1. Personnummer Validation:")
        pnr_results = results['personnummer']
        print(f"- Invalid check digits: {len(pnr_results['invalid_check_digits'])}")
        if pnr_results['invalid_check_digits']:
            print("  Examples:", pnr_results['invalid_check_digits'][:3])
            
        print(f"- Invalid dates: {len(pnr_results['invalid_dates'])}")
        if pnr_results['invalid_dates']:
            print("  Examples:", pnr_results['invalid_dates'][:3])
            
        print(f"- Unreasonable ages: {len(pnr_results['unreasonable_ages'])}")
        if pnr_results['unreasonable_ages']:
            print("  Examples:", pnr_results['unreasonable_ages'][:3])
            
        print(f"- Duplicates: {len(pnr_results['duplicates'])}")
        if pnr_results['duplicates']:
            print("  Examples:", pnr_results['duplicates'][:3])
            
        print(f"- Missing guardian info: {len(pnr_results['missing_guardian_info'])}")
        if pnr_results['missing_guardian_info']:
            print("  Examples:", [x['personnummer'] for x in pnr_results['missing_guardian_info'][:3]])
            
        print(f"- Invalid guardian info: {len(pnr_results['invalid_guardian_info'])}")
        if pnr_results['invalid_guardian_info']:
            print("  Examples:", [x['personnummer'] for x in pnr_results['invalid_guardian_info'][:3]])
        
        # Address validation results
        print("\n2. Address Validation:")
        addr_results = results['address']
        print(f"- Invalid format: {len(addr_results['invalid_format'])}")
        if addr_results['invalid_format']:
            print("  Examples:", addr_results['invalid_format'][:3])
            
        print(f"- Missing postal code: {len(addr_results['missing_postal_code'])}")
        if addr_results['missing_postal_code']:
            print("  Examples:", addr_results['missing_postal_code'][:3])
            
        print(f"- Invalid Swedish postal codes: {len(addr_results['invalid_postal_code_format']['swedish'])}")
        if addr_results['invalid_postal_code_format']['swedish']:
            print("  Examples:", addr_results['invalid_postal_code_format']['swedish'][:3])
            
        print(f"- Invalid international postal codes: {len(addr_results['invalid_postal_code_format']['international'])}")
        if addr_results['invalid_postal_code_format']['international']:
            print("  Examples:", addr_results['invalid_postal_code_format']['international'][:3])
            
        print(f"- Missing city: {len(addr_results['missing_city'])}")
        if addr_results['missing_city']:
            print("  Examples:", addr_results['missing_city'][:3])
            
        print(f"- Missing country: {len(addr_results['missing_country'])}")
        if addr_results['missing_country']:
            print("  Examples:", addr_results['missing_country'][:3])
            
        print(f"- Swedish addresses: {addr_results['address_stats']['swedish']}")
        print(f"- International addresses: {addr_results['address_stats']['international']}")
        
        # Phone number validation results
        print("\n3. Phone Number Validation:")
        phone_results = results['phone']
        print(f"- International format: {len(phone_results['formats']['international'])}")
        if phone_results['formats']['international']:
            print("  Examples:", phone_results['formats']['international'][:3])
            
        print(f"- Local format: {len(phone_results['formats']['local'])}")
        if phone_results['formats']['local']:
            print("  Examples:", phone_results['formats']['local'][:3])
            
        print(f"- Other format: {len(phone_results['formats']['other'])}")
        if phone_results['formats']['other']:
            print("  Examples:", phone_results['formats']['other'][:3])
            
        print(f"- Invalid numbers: {len(phone_results['invalid'])}")
        if phone_results['invalid']:
            print("  Examples:", phone_results['invalid'][:3])
            
        print(f"- Failed standardization: {len(phone_results['standardization']['failed_standardization'])}")
        if phone_results['standardization']['failed_standardization']:
            print("  Examples:", phone_results['standardization']['failed_standardization'][:3])
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_customer_validation() 