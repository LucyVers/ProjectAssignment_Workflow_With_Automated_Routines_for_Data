from src.data_processing.workflow import format_phone_number
import pandas as pd

# Test cases
test_numbers = [
    # Svenska nummer
    "08-123 45 67",         # Svenskt lokalt (Stockholm)
    "0470-123 45 67",       # Svenskt lokalt (Växjö)
    "031-123 45 67",        # Svenskt lokalt (Göteborg)
    "+46 8 123 45 67",      # Svenskt internationellt
    "+46(8)123 45 67",      # Svenskt redan i rätt format
    
    # Internationella nummer
    "+1 555 123 4567",      # USA
    "+44 20 1234 5678",     # UK
    "+47 21 234 567",       # Norge
    "+45 32 123 456",       # Danmark
    "+33 1 23 45 67 89",    # Frankrike
    
    # Specialfall
    "",                     # Tom sträng
    None,                   # None
    "123456",              # Ogiltigt format
    "+abc123",             # Ogiltiga tecken
]

print("Testing phone number formatting:")
print("-" * 50)
for number in test_numbers:
    formatted = format_phone_number(number)
    print(f"Original: {number}")
    print(f"Formatted: {formatted}")
    print("-" * 50) 