import pandas as pd
from Utilities.helpers import (
    format_phone,
    parse_date,
    normalize_email
)

#Standardize partner data to unified schema and applies inline annotations for invalid phone numbers and dates.
def standardize_columns(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Transformations:
    - external_id: Mapped from partner's ID field
    - first_name: Title Case
    - last_name: Title Case
    - dob: ISO-8601 (YYYY-MM-DD) with annotation if invalid
    - email: Lowercase
    - phone: XXX-XXX-XXXX format with annotation if invalid
    - partner_code: Added from config
    
    Internal tracking columns (for validation):
    - _phone_invalid: Boolean flag
    - _dob_invalid: Boolean flag
    """
    # Rename columns using partner mapping
    df = df.rename(columns=config["column_mapping"])
    
    # Adding partner_code
    df["partner_code"] = config["partner_code"]

    df["first_name"] = df["first_name"].str.title()
    df["last_name"] = df["last_name"].str.title()
    
    df["email"] = df["email"].apply(normalize_email)
    
    # Phone, XXX-XXX-XXXX with annotations
    phone_results = df["phone"].apply(format_phone)
    
    # Extracting formatted phone and invalid flag
    df["phone"] = phone_results.apply(lambda x: x[0])
    df["_phone_invalid"] = phone_results.apply(lambda x: x[1])
    
    # DOB, ISO-8601 with annotations
    dob_results = df["dob"].apply(parse_date)
    
    # Extracting formatted date and invalid flag
    df["dob"] = dob_results.apply(lambda x: x[0])
    df["_dob_invalid"] = dob_results.apply(lambda x: x[1])
    
    return df