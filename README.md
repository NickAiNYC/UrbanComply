# UrbanComply

UrbanComply is a compliance automation platform for urban energy benchmarking and reporting.

## Utility Data Validation Script

The `check_utility_data.py` script automates the validation of utility data CSV files for compliance with LL84/33 benchmarking requirements.

### Features

- **File Format Validation**: Validates CSV format and column structure
- **Column Presence Check**: Ensures all required columns are present (Date, kWh, Therms, Demand)
- **Missing Data Detection**: Identifies missing values and missing months in date sequences
- **Negative Value Detection**: Flags negative or irrational values in numeric columns
- **Unit Mismatch Detection**: Identifies potential unit measurement inconsistencies
- **Duplicate Row Detection**: Finds duplicate entries in the data
- **Empty Row Handling**: Gracefully handles and removes empty rows
- **Flexible Delimiters**: Supports various CSV delimiters (comma, semicolon, tab, pipe)
- **Comprehensive Logging**: Detailed logs for debugging and compliance tracking
- **JSON Report Generation**: Creates structured validation reports in JSON format

### Installation

1. Clone the repository:
```bash
git clone https://github.com/NickAiNYC/UrbanComply.git
cd UrbanComply
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### Basic Usage

Validate a utility data CSV file:
```bash
python check_utility_data.py utility_data.csv
```

This will:
- Validate the input file `utility_data.csv`
- Generate a validation report as `validation_report.json`
- Log all operations to console and `validation.log`

#### Custom Output File

Specify a custom output file for the validation report:
```bash
python check_utility_data.py utility_data.csv -o my_report.json
```

#### Custom Thresholds

Set custom minimum and maximum value thresholds:
```bash
python check_utility_data.py utility_data.csv --min-value 0 --max-value 1000000
```

#### Verbose Logging

Enable verbose logging for detailed debugging:
```bash
python check_utility_data.py utility_data.csv -v
```

#### Complete Example

```bash
python check_utility_data.py data/utility_data.csv \
    -o reports/validation_report.json \
    --min-value 0 \
    --max-value 5000000 \
    -v
```

### Command-Line Options

```
positional arguments:
  input_file            Path to the utility data CSV file

optional arguments:
  -h, --help            Show help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to the output JSON report file (default: validation_report.json)
  --min-value MIN_VALUE
                        Minimum acceptable value for numeric columns (default: 0.0)
  --max-value MAX_VALUE
                        Maximum acceptable value for numeric columns (default: 1e9)
  --date-format DATE_FORMAT
                        Expected date format (e.g., %Y-%m-%d). Auto-detected if not specified.
  -v, --verbose         Enable verbose logging
```

### Input File Format

The input CSV file must contain the following columns:
- **Date**: Date of the utility reading (e.g., 2024-01-01, 01/01/2024)
- **kWh**: Electricity consumption in kilowatt-hours
- **Therms**: Gas consumption in therms
- **Demand**: Peak electricity demand in kW

Example:
```csv
Date,kWh,Therms,Demand
2024-01-01,1250.5,45.2,150
2024-02-01,1180.3,42.8,145
2024-03-01,1100.0,38.5,140
```

### Output Report Format

The validation report is generated as a JSON file with the following structure:

```json
{
  "timestamp": "2024-01-16T12:00:00.000000",
  "input_file": "utility_data.csv",
  "validation_status": "PASS",
  "passed": true,
  "summary": {
    "total_errors": 0,
    "total_warnings": 0,
    "rows_processed": 12
  },
  "errors": [],
  "warnings": []
}
```

#### Error Types

The validator can detect the following error types:
- `FileNotFound`: Input file does not exist
- `InvalidFileFormat`: Unable to parse CSV file
- `MissingColumns`: Required columns are missing
- `InvalidDates`: Date values cannot be parsed
- `MissingData`: Missing values in required columns
- `MissingMonths`: Gaps in monthly date sequence
- `DuplicateRows`: Duplicate data entries
- `NegativeValues`: Negative values in numeric columns
- `NonNumericValues`: Non-numeric values in numeric columns

#### Warning Types

- `EmptyRows`: Empty rows found and removed
- `ExtremeValues`: Values exceeding the maximum threshold
- `PotentialUnitMismatch`: Values that may indicate unit conversion errors

### Exit Codes

- `0`: Validation passed successfully
- `1`: Validation failed (errors detected)

### Testing

Run the test suite:
```bash
python -m pytest tests/test_check_utility_data.py -v
```

Or using unittest:
```bash
python -m unittest discover tests -v
```

### Examples

#### Valid Data Example

Sample file (`tests/sample_valid_data.csv`):
```csv
Date,kWh,Therms,Demand
2024-01-01,1250.5,45.2,150
2024-02-01,1180.3,42.8,145
2024-03-01,1100.0,38.5,140
```

Run validation:
```bash
python check_utility_data.py tests/sample_valid_data.csv
```

Output:
```
2024-01-16 12:00:00 - INFO - Starting validation of tests/sample_valid_data.csv
2024-01-16 12:00:00 - INFO - Loading CSV file...
2024-01-16 12:00:00 - INFO - Successfully loaded CSV with delimiter ','
2024-01-16 12:00:00 - INFO - All required columns present
2024-01-16 12:00:00 - INFO - Validation report saved to validation_report.json
============================================================
VALIDATION SUMMARY
============================================================
Status: PASS
Total Errors: 0
Total Warnings: 0
Rows Processed: 3
============================================================
```

#### Invalid Data Example

Sample file with errors (`tests/sample_invalid_data.csv`):
```csv
Date,kWh,Therms,Demand
2024-01-01,1250.5,45.2,150
2024-02-01,-100.0,42.8,145
2024-03-01,,38.5,140
```

Run validation:
```bash
python check_utility_data.py tests/sample_invalid_data.csv
```

The script will detect:
- Negative value in kWh column (row 2)
- Missing value in kWh column (row 3)
- Exit with code 1

### Integration

The script can be easily integrated into automated workflows:

#### Shell Script
```bash
#!/bin/bash
python check_utility_data.py "$1" -o "report_$(date +%Y%m%d).json"
if [ $? -eq 0 ]; then
    echo "Validation passed"
else
    echo "Validation failed - check report for details"
    exit 1
fi
```

#### Python Integration
```python
from check_utility_data import UtilityDataValidator

validator = UtilityDataValidator(
    input_file='utility_data.csv',
    output_file='report.json'
)
report = validator.validate()

if report['passed']:
    print("Validation successful!")
else:
    print(f"Validation failed with {len(report['errors'])} errors")
```

### Requirements

- Python 3.10 or higher
- pandas >= 2.0.0
- numpy >= 1.24.0

### Success Metrics

- ✅ Automates 90%+ of the validation process
- ✅ Robust error handling prevents crashes
- ✅ Detailed error logs for debugging and compliance
- ✅ CLI support with configurable parameters
- ✅ Handles edge cases (duplicates, empty rows, incorrect delimiters)

### License

See LICENSE file for details.