import re
from dateutil import parser
from datetime import datetime

#Parsing date to ISO-8601 format (YYYY-MM-DD) and ddds inline annotation for invalid dates.
def parse_date(value):
    
    if not value or str(value).strip() == "":
        return "", False
    
    try:
        parsed = parser.parse(str(value), fuzzy=False)
        
        # If date is reasonable it should be between 1900 and current year + 1
        current_year = datetime.now().year
        if not (1900 <= parsed.year <= current_year + 1):
            return f"{value}*(Invalid DOB)", True # not reasonable
        
        # Checking for invalid day/month combinations
        try:
            datetime(parsed.year, parsed.month, parsed.day)
        except ValueError:
            return f"{value}*(Invalid DOB)", True #invalid day/month        
        # Valid date - return ISO-8601 format
        return parsed.strftime("%Y-%m-%d"), False
        
    except (ValueError, OverflowError):
        # Could not parse date at all
        return f"{value}*(Invalid DOB)", True

#Formatting phone number to XXX-XXX-XXXX and adding inline annotation for invalid phone numbers.
def format_phone(value):
    
    if not value or str(value).strip() == "":
        return "", False
    
    # Extracting digits
    digits = re.sub(r"\D", "", str(value))
    
    # Valid if exactly 10 digits
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}", False
    
    # Valid if 11 digits with leading 1
    if len(digits) == 11 and digits[0] == "1":
        return f"{digits[1:4]}-{digits[4:7]}-{digits[7:]}", False
    
    # Invalid if too many or too few digits
    return f"{value}*(Invalid Phone Number)", True

#Email to lowercase
def normalize_email(value):
    
    if not value or str(value).strip() == "":
        return ""

    email = str(value).lower().strip()    
    return email