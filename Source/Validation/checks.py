import pandas as pd

#Validating data and separating into valid/error records.
def validate_data(df: pd.DataFrame):
    """ 
    Validation Criteria:
    1. Hard Error: Missing external_id -> Goes ONLY to error file
    2. Soft Error: Invalid phone/DOB -> Goes to BOTH processed and error files
    
    """
    if df is None or df.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    df = df.copy()
    
    # Ensuring if error flag columns exist
    if "_phone_invalid" not in df.columns:
        df["_phone_invalid"] = False
    if "_dob_invalid" not in df.columns:
        df["_dob_invalid"] = False
    
    # Task 1: Missing External ID (HARD ERROR)
    external_id = df.get("external_id")
    
    if external_id is None:
        df["error_reason"] = "MISSING_EXTERNAL_ID"
        return pd.DataFrame(columns=df.columns), df
    
    missing_external_id = (
        external_id.isna() | 
        (external_id.astype(str).str.strip() == "")
    )
    
    # Task 2: Invalid Phone or DOB (SOFT ERRORS)
    has_phone_error = df["_phone_invalid"] == True
    has_dob_error = df["_dob_invalid"] == True
    
    # Building error DataFrame
    error_mask = missing_external_id | has_phone_error | has_dob_error
    error_df = df[error_mask].copy()
    
    if not error_df.empty:
        error_reasons = []
        
        for idx, row in error_df.iterrows():
            reasons = []
            
            # Priority for hadd error
            if missing_external_id[idx]:
                reasons.append("Missing External ID")
        
            # Adding soft errors
            if has_phone_error[idx]:
                reasons.append("Invalid Phone Number")
            if has_dob_error[idx]:
                reasons.append("Invalid DOB")
            
            # Combine all reasons using |
            error_reasons.append(" | ".join(reasons))
        
        error_df["error_reason"] = error_reasons
    
    # Building processed DataFrame
    # Processed file includes: i). All rows EXCEPT those with missing external_id, 
                            # ii). Additionally, rows with invalid phone/DOB ARE included (with annotations)
    processed_df = df[~missing_external_id].copy()
    
    # Cleaning up by removing internal error flags
    # These flags are only for internal tracking and they do NOT appear in final CSV files
    cols_to_drop = ["_phone_invalid", "_dob_invalid"]
    
    if not processed_df.empty:
        processed_df = processed_df.drop(columns=cols_to_drop, errors="ignore")
    
    if not error_df.empty:
        error_df = error_df.drop(columns=cols_to_drop, errors="ignore")
    
    return processed_df, error_df