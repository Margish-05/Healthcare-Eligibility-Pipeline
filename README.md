# Healthcare Eligibility Pipeline

A **configuration-driven ETL pipeline** for ingesting, transforming, and standardizing healthcare member eligibility data from multiple partners with varying file formats.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Adding a New Partner](#adding-a-new-partner)
- [Output Files](#output-files)
- [Data Validation](#data-validation)
- [CI/CD](#cicd)
- [Requirements](#requirements)
- [Design Principles](#design-principles)
- [Troubleshooting](#troubleshooting)

---

## Overview

This pipeline solves the challenge of processing healthcare eligibility data from multiple partners, each using different file formats and column structures. The solution is **100% configuration-driven**, enabling new partner onboarding without code changes.

### Problem Solved

Healthcare organizations receive member eligibility files from various insurance partners:
- **Partner A**: Pipe-delimited files (`|`) with columns like `MBI`, `FNAME`
- **Partner B**: CSV files (`,`) with columns like `subscriber_id`, `first_name`

This pipeline unifies all partner data into a single standardized dataset while maintaining data quality through validation and error handling.

---

## Key Features

### Core Capabilities
- **Configuration-Driven**: Add new partners via YAML config files (zero code changes)
- **Flexible Format Support**: Handles any delimiter (pipe, comma, tab, etc.)
- **Dynamic Column Mapping**: Maps partner columns to standard schema via configuration
- **Inline Annotations**: Flags invalid data with clear annotations while preserving records
- **Automated CI/CD**: GitHub Actions workflow ensures code quality on every commit

### Data Transformations
- **Names** - Title Case (`john` → `John`)
- **Emails** - Lowercase (`JOHN@EMAIL.COM` → `john@email.com`)
- **Phone Numbers** - `XXX-XXX-XXXX` format with validation
- **Dates** - ISO-8601 format (`YYYY-MM-DD`) with validation

### Data Quality Features
- **External ID Validation**: Ensures all records have valid identifiers
- **Graceful Error Handling**: Invalid phone/date formats are annotated and flagged
- **Dual Tracking**: Problem records appear in both processed (annotated) and error files
- **Comprehensive Logging**: Detailed error reports with specific failure reasons

---

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Margish-05/healthcare-eligibility-pipeline.git
cd healthcare-eligibility-pipeline

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

```bash
python Source/main.py
```

### Expected Output

```
Processing file: Data/Raw/acme.txt
Total records received: 5
Successfully processed records: 4
Records sent to error file: 3

Processing file: Data/Raw/bettercare.csv
Total records received: 4
Successfully processed records: 4
Records sent to error file: 2
```

---

## Project Structure

```
Healthcare Eligibility Pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml                      # CI/CD automation
├── Configuration/
│   ├── acme_health.yaml                # Acme Health config
│   └── better_care.yaml                # Better Care config
├── Data/
│   ├── Errors/                         # Invalid records
│   |   ├── acme_errors.csv
│   |   └── bettercare_errors.csv                                                            
│   ├── Processed/                      # Standardized output
│   |   ├── acme_processed.csv
│   |   └── bettercare_processed.csv
│   |   └── unified_eligibility.csv                      
│   └── Raw/                            # Source files
│       ├── acme.txt
│       └── bettercare.csv
├── Source/
│   ├── Ingestion/
│   │   └── reader.py                   # File reading logic
│   ├── Transformation/
│   │   └── standardize.py              # Data transformations
│   ├── Utilities/
│   │   └── helpers.py                  # Helper functions
│   ├── Validation/
│   │   └── checks.py                   # Data quality checks
│   └── main.py                         # Pipeline orchestrator
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Configuration

### Partner Configuration Example

**Configuration/acme_health.yaml:**
```yaml
partner_code: ACME
file_path: Data/Raw/acme.txt
delimiter: "|"

column_mapping:
  MBI: external_id
  FNAME: first_name
  LNAME: last_name
  DOB: dob
  EMAIL: email
  PHONE: phone
```

### Configuration Options

| Field | Description | Example |
|-------|-------------|---------|
| `partner_code` | Unique partner identifier | `ACME` |
| `file_path` | Path to input file | `Data/Raw/acme.txt` |
| `delimiter` | File delimiter character | `\|`, `,`, `\t` |
| `column_mapping` | Source - Target column mapping | `MBI: external_id` |

---

## Usage

### Basic Execution

```bash
# Run with all partners
python Source/main.py
```

### Output Location

- **Processed Files**: `Data/Processed/`
  - Individual partner files: `{partner}_processed.csv`
  - Unified dataset: `unified_eligibility.csv`

- **Error Files**: `Data/Errors/`
  - Individual partner errors: `{partner}_errors.csv`

### Verifying Output

```bash
# View unified output
cd Data/Processed/unified_eligibility.csv

# View error records
cd Data/Errors/acme_errors.csv
```

---

## Adding a New Partner

### Step 1: Create Configuration File

Create `Configuration/newpartner.yaml`:

```yaml
partner_code: NEWP
file_path: Data/Raw/newpartner.csv
delimiter: ","

column_mapping:
  subscriber_id: external_id
  first_name: first_name
  last_name: last_name
  date_of_birth: dob
  email: email
  phone: phone
```

### Step 2: Add Data File

Place new partner's file in `Data/Raw/newpartner.csv`

### Step 3: Run Pipeline

```bash
python Source/main.py
```

**Done** the pipeline automatically:
- Discovers the new configuration
- Reads the file with specified delimiter
- Maps columns using your configuration
- Applies standard transformations
- Includes data in unified output

---

## Output Files

### Unified Eligibility Dataset

**File**: `Data/Processed/unified_eligibility.csv`

**Schema** (7 columns):
```csv
external_id,first_name,last_name,dob,email,phone,partner_code
1234567890A,John,Doe,1955-03-15,john.doe@email.com,555-123-4567,ACME
BC-001,Alice,Johnson,1965-08-10,alice.j@test.com,555-222-3333,BETTERCARE
```

### Error Files (Per Partner)

**Example**: `Data/Errors/acme_errors.csv`

Contains records with data quality issues:
```csv
external_id,first_name,last_name,dob,email,phone,partner_code,error_reason
,Racey,Minch,1999-09-21,racey@email.com,789-789-7412,,Missing External ID
7878787872C,Mace,Jace,1985-08-22,mace@email.com,7897989899898*(Invalid Phone Number),ACME,Invalid Phone Number
```
### Processed Files (Per Partner)

**Example**: `Data/Processed/acme_processed.csv`

Contains standardized records with:
- Valid external_id
- All transformations applied
- Invalid data marked with inline annotations

**Sample with annotation**:
```csv
external_id,first_name,last_name,dob,email,phone,partner_code
7878787872C,Mace,Jace,1985-08-22,mace@email.com,7897989899898*(Invalid Phone Number),ACME
```
---

## Data Validation

### Validation Rules

#### External ID (Hard Validation)
- **Rule**: Must be present and non-empty
- **Action**: Records without external_id go **only** to error file
- **Reason**: External ID is mandatory for record identification

#### Phone Number (Soft Validation)
- **Valid**: 10 digits or 11 digits starting with 1
- **Format**: `XXX-XXX-XXXX`
- **Invalid**: Any other digit count
- **Action**: Annotated as `{original}*(Invalid Phone Number)`
- **Tracking**: Appears in both processed (with annotation) and error files

#### Date of Birth (Soft Validation)
- **Valid**: Parseable date between 1900 and current year + 1
- **Format**: `YYYY-MM-DD` (ISO-8601)
- **Invalid**: Unparseable dates, invalid day/month combinations
- **Action**: Annotated as `{original}*(Invalid DOB)`
- **Tracking**: Appears in both processed (with annotation) and error files

### Annotation Examples

| Input | Validation | Output |
|-------|-----------|--------|
| `5551234567` |  Valid (10 digits) | `555-123-4567` |
| `555123456789` | Invalid (12 digits) | `555123456789*(Invalid Phone Number)` |
| `03/15/1955` | Valid date | `1955-03-15` |
| `1995-22-22` | Invalid month | `1995-22-22*(Invalid DOB)` |

---

## CI/CD

This project uses **GitHub Actions** for automated testing on every commit.

### Workflow Triggers
- Push to `main` branch
- Pull requests to `main` branch

### What Gets Tested
1. Code checkout
2. Python 3.11 setup
3. Dependency installation
4. Input file validation
5. Configuration file validation
6. Pipeline execution
7. Output file verification
8. Schema validation (7 columns)
9. Annotation feature validation

---

## Requirements

**Python Version**: 3.11+

**Dependencies**:
```
pandas==2.1.4
python-dateutil==2.8.2
PyYAML==6.0.1
```

**Install all dependencies**:
```bash
pip install -r requirements.txt
```

---

## Design Principles

### Configuration-Driven Architecture
- **Zero Hardcoded Values**: All file paths, delimiters, column mappings in YAML
- **Extensible**: Add partners without touching source code
- **Maintainable**: Clear separation between logic and configuration

### Data Quality First
- **Validation**: Ensures external_id presence
- **Error Handling**: Gracefully handles malformed data
- **Transparency**: Clear annotations show exactly what's invalid
- **Audit Trail**: Error files document all issues
---

## Troubleshooting

### Issue: "FileNotFoundError"
**Cause**: Input file path in config doesn't match actual file location

**Solution**:
```bash
# Verify file exists
ls Data/Raw/

# Check path in configuration file
# Windows Command Prompt:
type Configuration/your_partner.yaml
```

---

### Issue: "Column not found"
**Cause**: Column mapping references non-existent column in source file

**Solution**:
```bash
# Check actual column names in file
# Windows PowerShell:
Get-Content Data\Raw\your_file.csv -First 1

```
---
**Scalability**: Designed for configuration-driven expansion. For large-scale processing (hundreds of records), consider migrating to PySpark.
---

## Author

**Margish Patel**
- GitHub: [Margish-05](https://github.com/Margish-05)
- LinkedIn: [Margish Patel](https://linkedin.com/in/margish-p-39b0b21b9)
- Email: margish45@gmail.com
