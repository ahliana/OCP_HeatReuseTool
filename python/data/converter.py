"""
Data Type Conversion Utilities

This module provides robust data type conversion functions that handle
various international number formats (European vs American), currency symbols,
and edge cases commonly found in CSV data.
"""

import re
import math
import pandas as pd


def universal_float_convert(value):
    """
    European-priority universal number parser
    Handles both American and European CSV data formats correctly
    
    Properly detects American thousands separators (comma + exactly 3 digits)
    vs European decimal separators
    
    Args:
        value: Input value to convert (string, number, or None)
        
    Returns:
        float: Converted numeric value, or 0.0 if conversion fails
        
    Examples:
        >>> universal_float_convert("1,493")  # European thousands
        1493.0
        >>> universal_float_convert("12.5")   # Standard decimal
        12.5
        >>> universal_float_convert("€1,375.2")  # Currency
        1375.2
    """
    # Handle None, NaN, and empty values
    if value is None:
        return 0.0
    
    try:
        if pd.isna(value):
            return 0.0
    except (TypeError, ValueError):
        pass
    
    # Handle numeric types that are already numbers
    if isinstance(value, (int, float)):
        if math.isnan(value) or math.isinf(value):
            return 0.0
        return float(value)
    
    # Convert to string and clean
    try:
        str_val = str(value).strip()
    except (UnicodeError, AttributeError):
        return 0.0
    
    # Handle empty string
    if not str_val:
        return 0.0
    
    # Handle special text cases
    special_cases = {
        'nan', 'none', 'null', 'n/a', 'na', '#n/a', '#value!', '#ref!', 
        '#div/0!', '#num!', 'inf', '-inf', 'infinity', '-infinity',
        'true', 'false', 'yes', 'no', 'error', 'err',
        'nichts', 'nul', 'erreur', 'infinito', 'niets', 'ingen'
    }
    if str_val.lower() in special_cases:
        return 0.0
    
    # Store original
    original_str = str_val
    
    # Handle scientific notation early
    scientific_patterns = [
        r'^-?[\d,]+\.?\d*[eE][+-]?\d+$',  # Standard: 1.5e3, 1,5e3
    ]
    for pattern in scientific_patterns:
        if re.match(pattern, str_val):
            try:
                sci_val = str_val.replace(',', '.')
                return float(sci_val)
            except (ValueError, OverflowError):
                continue
    
    # Handle percentage
    is_percentage = False
    if '%' in str_val:
        is_percentage = True
        str_val = str_val.replace('%', '')
    
    # Remove currency symbols
    currency_pattern = r'[$€£¥₹₽¢₦₪₨₩₫₡₵₸₴₺₼CHF|USD|EUR|GBP]'
    str_val = re.sub(currency_pattern, '', str_val, flags=re.IGNORECASE)
    
    # Remove text words
    text_patterns = [
        r'\b(ca\.?|etwa|circa|environ|ongeveer)\b',
        r'[()[\]{}"\']',
    ]
    for pattern in text_patterns:
        str_val = re.sub(pattern, '', str_val, flags=re.IGNORECASE)
    
    # Clean whitespace
    str_val = ' '.join(str_val.split())
    
    # Keep only numbers, separators, and signs
    str_val = re.sub(r'[^\d.,\s+\-\']', '', str_val).strip()
    
    if not str_val:
        return 0.0
    
    # Handle sign
    is_negative = False
    if str_val.startswith('-'):
        is_negative = True
        str_val = str_val[1:].strip()
    elif str_val.startswith('+'):
        str_val = str_val[1:].strip()
    
    if not str_val:
        return 0.0
    
    try:
        result = None
        
        # STRATEGY 1: Simple cases (no ambiguity)
        if re.match(r'^\d+$', str_val):
            # Pure integer: 123
            result = float(str_val)
            
        # STRATEGY 2: Clear multi-separator patterns (unambiguous)
        elif re.match(r'^\d{1,3}(\.\d{3})+,\d+$', str_val):
            # German: 1.234.567,89 (dots=thousands, comma=decimal)
            result = float(str_val.replace('.', '').replace(',', '.'))
            
        elif re.match(r'^\d{1,3}(\s\d{3})+,\d+$', str_val):
            # French: 1 234 567,89 (spaces=thousands, comma=decimal)
            result = float(str_val.replace(' ', '').replace(',', '.'))
            
        elif re.match(r'^\d{1,3}(\'\d{3})+\.\d+$', str_val):
            # Swiss: 1'234'567.89 (apostrophes=thousands, dot=decimal)
            result = float(str_val.replace('\'', ''))
            
        elif re.match(r'^\d{1,3}(,\d{3})+\.\d+$', str_val):
            # American with decimal: 1,234,567.89 (commas=thousands, dot=decimal)
            result = float(str_val.replace(',', ''))
            
        # STRATEGY 3: Thousands-only patterns (no decimal part)
        elif re.match(r'^\d{1,3}(\.\d{3})+$', str_val):
            # German thousands: 1.234.567
            result = float(str_val.replace('.', ''))
            
        elif re.match(r'^\d{1,3}(\s\d{3})+$', str_val):
            # French thousands: 1 234 567
            result = float(str_val.replace(' ', ''))
            
        elif re.match(r'^\d{1,3}(\'\d{3})+$', str_val):
            # Swiss thousands: 1'234'567
            result = float(str_val.replace('\'', ''))
            
        elif re.match(r'^\d{1,3}(,\d{3})+$', str_val):
            # American thousands: 1,234,567 OR single group like 1,493
            result = float(str_val.replace(',', ''))
            
        # STRATEGY 4: Single separator - IMPROVED LOGIC
        elif re.match(r'^\d+[.,]\d+$', str_val):
            # Single separator - need to determine if thousands or decimal
            if ',' in str_val:
                parts = str_val.split(',')
                integer_part = parts[0]
                fractional_part = parts[1]
                
                # KEY FIX: Check for American thousands pattern first
                if len(fractional_part) == 3 and len(integer_part) <= 4:
                    # AMERICAN THOUSANDS: 1,493 or 12,345 (comma + exactly 3 digits)
                    # This is definitely a thousands separator, not decimal
                    result = float(integer_part + fractional_part)
                    print(f"🔍 Detected American thousands: {str_val} → {result}")
                elif len(fractional_part) <= 2:
                    # European decimal: 1,5 or 123,45 (comma + 1-2 digits)
                    result = float(integer_part + '.' + fractional_part)
                    print(f"🔍 Detected European decimal: {str_val} → {result}")
                elif len(fractional_part) > 3:
                    # 4+ digits after comma: definitely decimal (European style)
                    result = float(integer_part + '.' + fractional_part)
                    print(f"🔍 Detected European long decimal: {str_val} → {result}")
                else:
                    # Fallback for edge cases
                    result = float(integer_part + fractional_part)  # Treat as thousands
                    
            else:  # '.' in str_val
                parts = str_val.split('.')
                integer_part = parts[0]
                fractional_part = parts[1]
                
                # For dots, similar logic but reversed priorities
                if len(fractional_part) == 3 and len(integer_part) >= 2:
                    # Could be European thousands: 12.345
                    # But could also be American decimal: 12.345
                    # Check if integer part suggests thousands (longer numbers)
                    if len(integer_part) >= 4:
                        # Likely European thousands: 1234.567 → 1234567
                        result = float(integer_part + fractional_part)
                        print(f"🔍 Detected European thousands: {str_val} → {result}")
                    else:
                        # Likely American decimal: 12.345
                        result = float(str_val)
                        print(f"🔍 Detected American decimal: {str_val} → {result}")
                elif len(fractional_part) <= 2:
                    # Standard decimal: 12.34
                    result = float(str_val)
                    print(f"🔍 Detected standard decimal: {str_val} → {result}")
                else:
                    # Default to decimal for unclear cases
                    result = float(str_val)
        
        # STRATEGY 5: Mixed separators (both . and ,)
        elif '.' in str_val and ',' in str_val:
            last_dot = str_val.rfind('.')
            last_comma = str_val.rfind(',')
            
            if last_comma > last_dot:
                # Comma is last = decimal separator (European)
                before = str_val[:last_comma].replace('.', '').replace(',', '').replace(' ', '').replace('\'', '')
                after = str_val[last_comma + 1:]
                result = float(f"{before}.{after}")
                print(f"🔍 Detected European mixed format: {str_val} → {result}")
            else:
                # Dot is last = decimal separator (American)
                before = str_val[:last_dot].replace('.', '').replace(',', '').replace(' ', '').replace('\'', '')
                after = str_val[last_dot + 1:]
                result = float(f"{before}.{after}")
                print(f"🔍 Detected American mixed format: {str_val} → {result}")
        
        # STRATEGY 6: Fallback
        else:
            # Try to extract just the digits
            digits_only = re.sub(r'[^\d]', '', str_val)
            if digits_only:
                result = float(digits_only)
                print(f"🔍 Fallback digits only: {str_val} → {result}")
            else:
                return 0.0
        
        # Apply transformations
        if is_negative and result is not None:
            result = -result
        
        if is_percentage and result is not None:
            result = result / 100.0
        
        # Validate result
        if result is None or math.isnan(result) or math.isinf(result):
            return 0.0
            
        return result
        
    except (ValueError, TypeError, OverflowError):
        # Final fallback
        try:
            digits_only = re.sub(r'[^\d]', '', original_str)
            if digits_only:
                fallback = float(digits_only)
                if is_negative:
                    fallback = -fallback
                if is_percentage:
                    fallback = fallback / 100.0
                return fallback
            else:
                return 0.0
        except:
            return 0.0

# Test function for validation
def test_converter():
    """Test the universal_float_convert function with various inputs"""
    test_cases = [
        ("1,493", 1493.0, "European thousands"),
        ("1.493", 1.493, "American decimal"),  
        ("12.5", 12.5, "Standard decimal"),
        ("€1,375.2", 1375.2, "Currency"),
        ("", 0.0, "Empty string"),
        (None, 0.0, "None value"),
    ]
    
    print("🧪 Testing universal_float_convert:")
    for input_val, expected, description in test_cases:
        result = universal_float_convert(input_val)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {input_val!r} → {result} (expected {expected}) - {description}")

if __name__ == "__main__":
    test_converter()