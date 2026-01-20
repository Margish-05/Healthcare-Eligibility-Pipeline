from pathlib import Path
import pandas as pd


def read_partner_file(config):
    
    project_root = Path(__file__).resolve().parents[2]
    
    file_path = project_root / config["file_path"]
    
    # Validate file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    # Validate file is not empty
    if file_path.stat().st_size == 0:
        raise ValueError(f"Input file is empty: {file_path}")
    
    return pd.read_csv(
        file_path,
        delimiter=config["delimiter"],
        dtype=str,
        keep_default_na=False
    )