import yaml
import pandas as pd
from pathlib import Path

from Ingestion.reader import read_partner_file
from Transformation.standardize import standardize_columns
from Validation.checks import validate_data

# Imp paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_DIR = PROJECT_ROOT / "Configuration"
OUTPUT_DIR = PROJECT_ROOT / "Data" / "Processed"
ERROR_DIR = PROJECT_ROOT / "Data" / "Errors"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ERROR_DIR.mkdir(parents=True, exist_ok=True)

# Required Schema (7 fields)

STANDARD_SCHEMA = [
    "external_id",
    "first_name",
    "last_name",
    "dob",
    "email",
    "phone",
    "partner_code"
]

# Loading all partner configuration files.
def load_configs():
    
    configs = []
    for file in CONFIG_DIR.iterdir():
        if file.suffix == ".yaml":
            with open(file) as f:
                configs.append(yaml.safe_load(f))
    return configs

# Executing the Pipeline.
def main():
    
    all_partners_data = []
    
    for config in load_configs():
        partner_code = config["partner_code"]
        
        try:
            # Step 1: Ingestion
            df = read_partner_file(config)
            total_received = len(df)
            
            # Step 2: Transformation (includes annotations)
            df = standardize_columns(df, config)
            
            # Step 3: Validation
            processed_df, error_df = validate_data(df)
            
            successfully_processed = len(processed_df)
            sent_to_error = len(error_df)
            
            # Step 4: Ensuring only standard schema columns
            processed_df = processed_df[STANDARD_SCHEMA]
            
            # Step 5: Writing outputs
            processed_file = OUTPUT_DIR / f"{partner_code.lower()}_processed.csv"
            processed_df.to_csv(processed_file, index=False)
            
            if not error_df.empty:
                error_file = ERROR_DIR / f"{partner_code.lower()}_errors.csv"
                error_df.to_csv(error_file, index=False)
            
            # Adding to unified dataset
            all_partners_data.append(processed_df)
            
            # Simple terminal summary output
            print(f"\nProcessing file: {config['file_path']}")
            print(f"Total records received: {total_received}")
            print(f"Successfully processed records: {successfully_processed}")
            print(f"Records sent to error file: {sent_to_error}")
            
        except Exception as e:
            print(f"\nERROR processing {partner_code}: {str(e)}")
            continue
    
    # Creating unified output
    if all_partners_data:
        unified_df = pd.concat(all_partners_data, ignore_index=True)
        unified_df = unified_df[STANDARD_SCHEMA]
        unified_file = OUTPUT_DIR / "unified_eligibility.csv"
        unified_df.to_csv(unified_file, index=False)


if __name__ == "__main__":
    main()