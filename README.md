# UrbanComply

**Agent-Based Framework for NYC LL84/33 Compliance Automation**

UrbanComply is an intelligent agent framework designed to streamline New York City Local Law 84/33 energy benchmarking compliance for building owners and energy consultants.

## 🎯 Project Status

**Current Phase**: Phase 0 - Foundation Setup  
**Goal**: Launch 3-5 paying pilot customers through automated compliance workflows

## 📋 What This Project Does

UrbanComply automates the complex process of NYC building energy compliance through five specialized AI agents:

1. **Pilot Hunter**: Customer acquisition and relationship management
2. **Process Engineer**: Compliance process mapping and documentation
3. **Scriptsmith**: Automation script development
4. **Validator**: Data validation and quality assurance (✅ **Completed** - see below)
5. **Scale Scout**: Market research and partnership evaluation

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 14+ (or SQLite for development)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/NickAiNYC/UrbanComply.git
cd UrbanComply
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

5. Initialize the database:
```bash
# For PostgreSQL:
psql -U your_username -d urbancomply -f schema.sql

# For SQLite (development):
sqlite3 urbancomply.db < schema.sql
```

## ✅ Utility Data Validation Script

The `check_utility_data.py` script automates the validation of utility data CSV files for compliance with LL84/33 benchmarking requirements. This is the first completed component of the Validator agent.

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

#### Command-Line Options

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

#### Examples

```bash
# Custom output file
python check_utility_data.py utility_data.csv -o my_report.json

# Custom thresholds
python check_utility_data.py utility_data.csv --min-value 0 --max-value 1000000

# Verbose logging
python check_utility_data.py utility_data.csv -v

# Complete example
python check_utility_data.py data/utility_data.csv \
    -o reports/validation_report.json \
    --min-value 0 \
    --max-value 5000000 \
    -v
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

### Validation Error Types

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

And warning types:
- `EmptyRows`: Empty rows found and removed
- `ExtremeValues`: Values exceeding the maximum threshold
- `PotentialUnitMismatch`: Values that may indicate unit conversion errors

### Testing the Validator

Run the test suite:
```bash
python -m pytest tests/test_check_utility_data.py -v
```

Or using unittest:
```bash
python -m unittest discover tests -v
```

## 📚 Documentation

- **[Upgrades Needed](UPGRADES_NEEDED.md)**: Comprehensive assessment of required technical upgrades
- **[Week 1 Execution Plan](week1_execution_plan.md)**: Founder-as-Service implementation roadmap
- **[Agent Communication Protocol](agent_comm_protocol.md)**: How agents interact and collaborate

## 🏗️ Project Structure

```
UrbanComply/
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── schema.sql              # Database schema
├── check_utility_data.py   # Utility data validation script
├── setup.py                # Package setup configuration
├── tests/                  # Test files
│   ├── test_check_utility_data.py
│   ├── sample_valid_data.csv
│   ├── sample_invalid_data.csv
│   └── sample_comprehensive_test.csv
├── README.md               # This file
├── UPGRADES_NEEDED.md      # Technical requirements assessment
├── week1_execution_plan.md # Implementation roadmap
├── agent_comm_protocol.md  # Agent collaboration guide
└── success_dashboard_template.csv  # KPI tracking template
```

## 🔧 Required Integrations

To fully utilize UrbanComply, you'll need access to:

- **NYC Department of Buildings (DOB) API**: For building data and submissions
- **ENERGY STAR Portfolio Manager**: For energy benchmarking
- **Google Sheets**: For CRM (or alternative CRM system)
- **Calendly**: For scheduling discovery calls
- **SendGrid**: For email automation (or alternative email service)

See `.env.example` for all required credentials.

## 🎯 Success Metrics (Phase 0)

| Agent | Target | Status |
|-------|--------|--------|
| Pilot Hunter | 5 signed pilot agreements | 🟡 In Progress |
| Process Engineer | 90% edge-case coverage | 🟡 In Progress |
| Scriptsmith | ≥50% time reduction per project | 🟡 In Progress |
| Validator | Zero DOB rejections | ✅ **Validation Script Complete** |
| Scale Scout | 3 partner evaluations | 🟡 In Progress |

## 🛣️ Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [x] Project structure and documentation
- [x] Database schema design
- [x] Environment configuration
- [x] Utility data validation script (Validator agent foundation)
- [ ] Base agent framework
- [ ] Basic CLI interface

### Phase 2: MVP Agents (Weeks 3-4)
- [ ] Complete Validator agent
- [ ] Process Engineer agent
- [ ] CRM integration
- [ ] Email automation

### Phase 3: Full Agent Suite (Weeks 5-7)
- [ ] Pilot Hunter agent
- [ ] Scriptsmith agent
- [ ] Scale Scout agent
- [ ] Agent communication system

### Phase 4: Production Ready (Weeks 8-12)
- [ ] External API integrations (DOB, ENERGY STAR)
- [ ] Comprehensive testing
- [ ] Security hardening
- [ ] Deployment automation

## 🤝 Contributing

This is currently a private project in active development. Contribution guidelines will be added once the project reaches a stable state.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Resources

- [NYC Local Law 84](https://www.nyc.gov/site/buildings/codes/benchmarking.page)
- [ENERGY STAR Portfolio Manager](https://www.energystar.gov/buildings/benchmark)
- [NYC Building Information Search (BIS)](https://a810-bisweb.nyc.gov/bisweb/bispi00.jsp)

## 📞 Contact

For questions or pilot program inquiries, please contact the project maintainer.

---

**Note**: This project is in active development. For a detailed technical assessment of what's needed to move forward, see [UPGRADES_NEEDED.md](UPGRADES_NEEDED.md).
