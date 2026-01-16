#!/usr/bin/env python3
"""
Utility Data Validation Script for UrbanComply

This script validates utility data CSV files for compliance with expected formats
and data quality standards. It checks for missing data, invalid values, and 
generates comprehensive validation reports.

Author: UrbanComply
Python: 3.10+
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd
import numpy as np


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('validation.log')
    ]
)
logger = logging.getLogger(__name__)


class UtilityDataValidator:
    """Validates utility data CSV files for compliance and data quality."""
    
    # Expected columns for utility data
    EXPECTED_COLUMNS = ['Date', 'kWh', 'Therms', 'Demand']
    
    # Numeric columns that should be validated
    NUMERIC_COLUMNS = ['kWh', 'Therms', 'Demand']
    
    def __init__(self, 
                 input_file: str,
                 output_file: str = 'validation_report.json',
                 min_value_threshold: float = 0.0,
                 max_value_threshold: float = 1e9,
                 date_format: str = None):
        """
        Initialize the validator.
        
        Args:
            input_file: Path to the input CSV file
            output_file: Path to the output JSON report file
            min_value_threshold: Minimum acceptable value for numeric columns
            max_value_threshold: Maximum acceptable value for numeric columns
            date_format: Expected date format (auto-detected if None)
        """
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.min_value_threshold = min_value_threshold
        self.max_value_threshold = max_value_threshold
        self.date_format = date_format
        self.errors = []
        self.warnings = []
        self.df = None
        
    def validate(self) -> Dict[str, Any]:
        """
        Run all validation checks on the utility data.
        
        Returns:
            Dictionary containing validation results
        """
        logger.info(f"Starting validation of {self.input_file}")
        
        # Check if file exists
        if not self._validate_file_exists():
            return self._generate_report(passed=False)
        
        # Load and validate file format
        if not self._load_csv():
            return self._generate_report(passed=False)
        
        # Validate columns
        if not self._validate_columns():
            return self._generate_report(passed=False)
        
        # Run all data quality checks
        self._check_empty_rows()
        self._check_duplicate_rows()
        self._validate_date_column()
        self._check_missing_data()
        self._validate_numeric_columns()
        self._check_negative_values()
        self._detect_unit_mismatches()
        
        # Determine if validation passed
        passed = len(self.errors) == 0
        
        return self._generate_report(passed=passed)
    
    def _validate_file_exists(self) -> bool:
        """Check if input file exists."""
        if not self.input_file.exists():
            error_msg = f"Input file not found: {self.input_file}"
            logger.error(error_msg)
            self.errors.append({
                'type': 'FileNotFound',
                'message': error_msg,
                'severity': 'critical'
            })
            return False
        return True
    
    def _load_csv(self) -> bool:
        """Load CSV file with various delimiter attempts."""
        logger.info("Loading CSV file...")
        
        # Try different delimiters
        delimiters = [',', ';', '\t', '|']
        
        for delimiter in delimiters:
            try:
                self.df = pd.read_csv(
                    self.input_file,
                    delimiter=delimiter,
                    skipinitialspace=True
                )
                
                # Check if we got reasonable columns
                if len(self.df.columns) > 1:
                    logger.info(f"Successfully loaded CSV with delimiter '{delimiter}'")
                    logger.info(f"Detected columns: {list(self.df.columns)}")
                    logger.info(f"Total rows: {len(self.df)}")
                    return True
                    
            except Exception as e:
                logger.debug(f"Failed to load with delimiter '{delimiter}': {str(e)}")
                continue
        
        # If we get here, all delimiters failed
        error_msg = "Failed to load CSV file with any standard delimiter"
        logger.error(error_msg)
        self.errors.append({
            'type': 'InvalidFileFormat',
            'message': error_msg,
            'severity': 'critical'
        })
        return False
    
    def _validate_columns(self) -> bool:
        """Validate that all expected columns are present."""
        logger.info("Validating column structure...")
        
        # Get actual columns (strip whitespace)
        actual_columns = [col.strip() for col in self.df.columns]
        self.df.columns = actual_columns
        
        missing_columns = []
        for col in self.EXPECTED_COLUMNS:
            if col not in actual_columns:
                missing_columns.append(col)
        
        if missing_columns:
            error_msg = f"Missing required columns: {missing_columns}"
            logger.error(error_msg)
            self.errors.append({
                'type': 'MissingColumns',
                'message': error_msg,
                'columns': missing_columns,
                'severity': 'critical'
            })
            return False
        
        logger.info("All required columns present")
        return True
    
    def _check_empty_rows(self):
        """Check for and remove empty rows."""
        logger.info("Checking for empty rows...")
        
        # Count rows that are completely empty
        empty_rows = self.df.isna().all(axis=1).sum()
        
        if empty_rows > 0:
            warning_msg = f"Found {empty_rows} completely empty rows - will be ignored"
            logger.warning(warning_msg)
            self.warnings.append({
                'type': 'EmptyRows',
                'message': warning_msg,
                'count': int(empty_rows)
            })
            
            # Remove empty rows
            self.df = self.df.dropna(how='all')
            logger.info(f"Removed {empty_rows} empty rows")
    
    def _check_duplicate_rows(self):
        """Check for duplicate rows."""
        logger.info("Checking for duplicate rows...")
        
        duplicates = self.df.duplicated().sum()
        
        if duplicates > 0:
            error_msg = f"Found {duplicates} duplicate rows"
            logger.error(error_msg)
            
            # Get indices of duplicate rows
            duplicate_indices = self.df[self.df.duplicated(keep=False)].index.tolist()
            
            self.errors.append({
                'type': 'DuplicateRows',
                'message': error_msg,
                'count': int(duplicates),
                'row_indices': duplicate_indices[:10],  # Show first 10
                'severity': 'high'
            })
    
    def _validate_date_column(self):
        """Validate the Date column format and values."""
        logger.info("Validating Date column...")
        
        date_col = self.df['Date']
        
        # Try to parse dates
        try:
            parsed_dates = pd.to_datetime(date_col, errors='coerce')
            invalid_dates = parsed_dates.isna().sum()
            
            if invalid_dates > 0:
                error_msg = f"Found {invalid_dates} invalid date entries"
                logger.error(error_msg)
                
                # Get examples of invalid dates
                invalid_examples = date_col[parsed_dates.isna()].head(5).tolist()
                
                self.errors.append({
                    'type': 'InvalidDates',
                    'message': error_msg,
                    'count': int(invalid_dates),
                    'examples': invalid_examples,
                    'severity': 'high'
                })
            else:
                # Store parsed dates for further analysis
                self.df['Date_parsed'] = parsed_dates
                logger.info("All dates successfully parsed")
                
        except Exception as e:
            error_msg = f"Failed to parse Date column: {str(e)}"
            logger.error(error_msg)
            self.errors.append({
                'type': 'DateParsingError',
                'message': error_msg,
                'severity': 'critical'
            })
    
    def _check_missing_data(self):
        """Check for missing data in all columns."""
        logger.info("Checking for missing data...")
        
        for col in self.EXPECTED_COLUMNS:
            if col not in self.df.columns:
                continue
                
            missing_count = self.df[col].isna().sum()
            missing_percentage = (missing_count / len(self.df)) * 100
            
            if missing_count > 0:
                error_msg = f"Column '{col}' has {missing_count} missing values ({missing_percentage:.2f}%)"
                logger.error(error_msg)
                
                # Get row indices with missing data
                missing_indices = self.df[self.df[col].isna()].index.tolist()
                
                self.errors.append({
                    'type': 'MissingData',
                    'message': error_msg,
                    'column': col,
                    'count': int(missing_count),
                    'percentage': round(missing_percentage, 2),
                    'row_indices': missing_indices[:10],  # Show first 10
                    'severity': 'high'
                })
        
        # Check for missing months in Date column
        if 'Date_parsed' in self.df.columns:
            self._check_missing_months()
    
    def _check_missing_months(self):
        """Check for missing months in the date sequence."""
        logger.info("Checking for missing months...")
        
        try:
            dates = self.df['Date_parsed'].dropna().sort_values()
            
            if len(dates) < 2:
                return
            
            # Get date range
            start_date = dates.iloc[0]
            end_date = dates.iloc[-1]
            
            # Generate expected monthly sequence
            expected_dates = pd.date_range(
                start=start_date,
                end=end_date,
                freq='MS'  # Month start
            )
            
            # Find missing months
            actual_months = dates.dt.to_period('M').unique()
            expected_months = expected_dates.to_period('M').unique()
            
            missing_months = set(expected_months) - set(actual_months)
            
            if missing_months:
                missing_list = sorted([str(m) for m in missing_months])
                error_msg = f"Found {len(missing_months)} missing months in date sequence"
                logger.error(error_msg)
                
                self.errors.append({
                    'type': 'MissingMonths',
                    'message': error_msg,
                    'count': len(missing_months),
                    'missing_months': missing_list[:12],  # Show first 12
                    'severity': 'medium'
                })
                
        except Exception as e:
            logger.warning(f"Could not check for missing months: {str(e)}")
    
    def _validate_numeric_columns(self):
        """Validate numeric columns are properly formatted."""
        logger.info("Validating numeric columns...")
        
        for col in self.NUMERIC_COLUMNS:
            if col not in self.df.columns:
                continue
            
            # Try to convert to numeric
            try:
                numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                
                # Check for non-numeric values
                non_numeric = numeric_col.isna() & self.df[col].notna()
                non_numeric_count = non_numeric.sum()
                
                if non_numeric_count > 0:
                    error_msg = f"Column '{col}' has {non_numeric_count} non-numeric values"
                    logger.error(error_msg)
                    
                    # Get examples
                    examples = self.df.loc[non_numeric, col].head(5).tolist()
                    
                    self.errors.append({
                        'type': 'NonNumericValues',
                        'message': error_msg,
                        'column': col,
                        'count': int(non_numeric_count),
                        'examples': examples,
                        'severity': 'high'
                    })
                else:
                    # Store numeric version for further checks
                    self.df[f'{col}_numeric'] = numeric_col
                    
            except Exception as e:
                error_msg = f"Failed to validate numeric column '{col}': {str(e)}"
                logger.error(error_msg)
                self.errors.append({
                    'type': 'NumericValidationError',
                    'message': error_msg,
                    'column': col,
                    'severity': 'high'
                })
    
    def _check_negative_values(self):
        """Check for negative or irrational values in numeric columns."""
        logger.info("Checking for negative values...")
        
        for col in self.NUMERIC_COLUMNS:
            numeric_col_name = f'{col}_numeric'
            
            if numeric_col_name not in self.df.columns:
                continue
            
            numeric_col = self.df[numeric_col_name]
            
            # Check for negative values
            negative_mask = numeric_col < self.min_value_threshold
            negative_count = negative_mask.sum()
            
            if negative_count > 0:
                error_msg = f"Column '{col}' has {negative_count} negative values"
                logger.error(error_msg)
                
                # Get examples
                negative_values = self.df.loc[negative_mask, col].head(5).tolist()
                negative_indices = self.df[negative_mask].index.tolist()
                
                self.errors.append({
                    'type': 'NegativeValues',
                    'message': error_msg,
                    'column': col,
                    'count': int(negative_count),
                    'examples': negative_values,
                    'row_indices': negative_indices[:10],
                    'severity': 'high'
                })
            
            # Check for extremely high values (potential errors)
            extreme_mask = numeric_col > self.max_value_threshold
            extreme_count = extreme_mask.sum()
            
            if extreme_count > 0:
                warning_msg = f"Column '{col}' has {extreme_count} extremely high values (>{self.max_value_threshold})"
                logger.warning(warning_msg)
                
                extreme_values = self.df.loc[extreme_mask, col].head(5).tolist()
                
                self.warnings.append({
                    'type': 'ExtremeValues',
                    'message': warning_msg,
                    'column': col,
                    'count': int(extreme_count),
                    'examples': extreme_values,
                    'threshold': self.max_value_threshold
                })
    
    def _detect_unit_mismatches(self):
        """Detect potential unit measurement mismatches within numeric columns."""
        logger.info("Checking for unit mismatches...")
        
        for col in self.NUMERIC_COLUMNS:
            numeric_col_name = f'{col}_numeric'
            
            if numeric_col_name not in self.df.columns:
                continue
            
            numeric_col = self.df[numeric_col_name].dropna()
            
            if len(numeric_col) < 2:
                continue
            
            # Calculate statistics
            mean_val = numeric_col.mean()
            std_val = numeric_col.std()
            
            if std_val == 0 or mean_val == 0:
                continue
            
            # Check for outliers using modified z-score (more robust)
            # Values that are more than 10x the median could indicate unit mismatch
            median_val = numeric_col.median()
            
            if median_val > 0:
                # Check for values that differ by more than 2 orders of magnitude
                outlier_mask = (numeric_col > median_val * 100) | (numeric_col < median_val / 100)
                outlier_count = outlier_mask.sum()
                
                if outlier_count > 0 and outlier_count < len(numeric_col) * 0.5:
                    warning_msg = f"Column '{col}' may have unit mismatches - {outlier_count} values differ significantly from median"
                    logger.warning(warning_msg)
                    
                    outlier_values = numeric_col[outlier_mask].head(5).tolist()
                    
                    self.warnings.append({
                        'type': 'PotentialUnitMismatch',
                        'message': warning_msg,
                        'column': col,
                        'count': int(outlier_count),
                        'median': float(median_val),
                        'examples': outlier_values
                    })
    
    def _generate_report(self, passed: bool) -> Dict[str, Any]:
        """
        Generate validation report.
        
        Args:
            passed: Whether validation passed
            
        Returns:
            Dictionary containing validation report
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'input_file': str(self.input_file),
            'validation_status': 'PASS' if passed else 'FAIL',
            'passed': passed,
            'summary': {
                'total_errors': len(self.errors),
                'total_warnings': len(self.warnings),
                'rows_processed': len(self.df) if self.df is not None else 0
            },
            'errors': self.errors,
            'warnings': self.warnings
        }
        
        # Save report to file
        try:
            with open(self.output_file, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Validation report saved to {self.output_file}")
        except Exception as e:
            logger.error(f"Failed to save report: {str(e)}")
        
        # Log summary
        logger.info("=" * 60)
        logger.info("VALIDATION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Status: {report['validation_status']}")
        logger.info(f"Total Errors: {len(self.errors)}")
        logger.info(f"Total Warnings: {len(self.warnings)}")
        if self.df is not None:
            logger.info(f"Rows Processed: {len(self.df)}")
        logger.info("=" * 60)
        
        return report


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Validate utility data CSV files for compliance and data quality',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s utility_data.csv
  %(prog)s input.csv -o report.json
  %(prog)s data.csv --min-value 0 --max-value 1000000
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Path to the utility data CSV file'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='validation_report.json',
        help='Path to the output JSON report file (default: validation_report.json)'
    )
    
    parser.add_argument(
        '--min-value',
        type=float,
        default=0.0,
        help='Minimum acceptable value for numeric columns (default: 0.0)'
    )
    
    parser.add_argument(
        '--max-value',
        type=float,
        default=1e9,
        help='Maximum acceptable value for numeric columns (default: 1e9)'
    )
    
    parser.add_argument(
        '--date-format',
        default=None,
        help='Expected date format (e.g., %%Y-%%m-%%d). Auto-detected if not specified.'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Create validator and run validation
    validator = UtilityDataValidator(
        input_file=args.input_file,
        output_file=args.output,
        min_value_threshold=args.min_value,
        max_value_threshold=args.max_value,
        date_format=args.date_format
    )
    
    report = validator.validate()
    
    # Exit with appropriate code
    sys.exit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
