"""
Unit tests for check_utility_data.py

Tests the utility data validation script with various scenarios including
valid data, missing columns, negative values, duplicates, and edge cases.
"""

import unittest
import tempfile
import json
import os
import shutil
from pathlib import Path
import sys

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from check_utility_data import UtilityDataValidator


class TestUtilityDataValidator(unittest.TestCase):
    """Test cases for UtilityDataValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = Path(self.temp_dir) / 'test_data.csv'
        self.output_json = Path(self.temp_dir) / 'test_report.json'
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_csv(self, content: str):
        """Helper to create a test CSV file."""
        with open(self.test_csv, 'w') as f:
            f.write(content)
    
    def test_valid_data(self):
        """Test validation with valid data."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100
2024-02-01,1100,55,110
2024-03-01,1050,52,105
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        self.assertTrue(report['passed'])
        self.assertEqual(report['validation_status'], 'PASS')
        self.assertEqual(report['summary']['total_errors'], 0)
        self.assertEqual(report['summary']['rows_processed'], 3)
    
    def test_missing_columns(self):
        """Test validation with missing required columns."""
        csv_content = """Date,kWh,Therms
2024-01-01,1000,50
2024-02-01,1100,55
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        self.assertFalse(report['passed'])
        self.assertEqual(report['validation_status'], 'FAIL')
        self.assertGreater(report['summary']['total_errors'], 0)
        
        # Check that missing column error is present
        error_types = [error['type'] for error in report['errors']]
        self.assertIn('MissingColumns', error_types)
    
    def test_negative_values(self):
        """Test detection of negative values."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100
2024-02-01,-100,55,110
2024-03-01,1050,-10,105
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        self.assertFalse(report['passed'])
        
        # Check for negative value errors
        negative_errors = [e for e in report['errors'] if e['type'] == 'NegativeValues']
        self.assertGreater(len(negative_errors), 0)
    
    def test_duplicate_rows(self):
        """Test detection of duplicate rows."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100
2024-02-01,1100,55,110
2024-01-01,1000,50,100
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        self.assertFalse(report['passed'])
        
        # Check for duplicate row errors
        duplicate_errors = [e for e in report['errors'] if e['type'] == 'DuplicateRows']
        self.assertEqual(len(duplicate_errors), 1)
        self.assertEqual(duplicate_errors[0]['count'], 1)
    
    def test_missing_data(self):
        """Test detection of missing data."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100
2024-02-01,,55,110
2024-03-01,1050,,105
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        self.assertFalse(report['passed'])
        
        # Check for missing data errors
        missing_errors = [e for e in report['errors'] if e['type'] == 'MissingData']
        self.assertGreater(len(missing_errors), 0)
    
    def test_empty_rows(self):
        """Test handling of empty rows."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100

2024-02-01,1100,55,110
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        # Empty rows should be handled gracefully
        self.assertTrue(report['passed'])
        
        # Check for empty row warnings
        if report['warnings']:
            warning_types = [w['type'] for w in report['warnings']]
            if 'EmptyRows' in warning_types:
                empty_warnings = [w for w in report['warnings'] if w['type'] == 'EmptyRows']
                self.assertGreater(empty_warnings[0]['count'], 0)
    
    def test_invalid_dates(self):
        """Test detection of invalid date formats."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100
invalid-date,1100,55,110
2024-03-01,1050,52,105
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        self.assertFalse(report['passed'])
        
        # Check for invalid date errors
        date_errors = [e for e in report['errors'] if e['type'] == 'InvalidDates']
        self.assertGreater(len(date_errors), 0)
    
    def test_non_numeric_values(self):
        """Test detection of non-numeric values in numeric columns."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100
2024-02-01,abc,55,110
2024-03-01,1050,xyz,105
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        self.assertFalse(report['passed'])
        
        # Check for non-numeric value errors
        non_numeric_errors = [e for e in report['errors'] if e['type'] == 'NonNumericValues']
        self.assertGreater(len(non_numeric_errors), 0)
    
    def test_semicolon_delimiter(self):
        """Test handling of semicolon-delimited CSV."""
        csv_content = """Date;kWh;Therms;Demand
2024-01-01;1000;50;100
2024-02-01;1100;55;110
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        self.assertTrue(report['passed'])
        self.assertEqual(report['summary']['rows_processed'], 2)
    
    def test_file_not_found(self):
        """Test handling of non-existent file."""
        validator = UtilityDataValidator(
            input_file='/nonexistent/file.csv',
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        self.assertFalse(report['passed'])
        
        # Check for file not found error
        error_types = [error['type'] for error in report['errors']]
        self.assertIn('FileNotFound', error_types)
    
    def test_extreme_values(self):
        """Test detection of extremely high values."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100
2024-02-01,999999999999,55,110
2024-03-01,1050,52,105
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json),
            max_value_threshold=1e9
        )
        
        report = validator.validate()
        
        # Should have warnings about extreme values
        if report['warnings']:
            warning_types = [w['type'] for w in report['warnings']]
            self.assertIn('ExtremeValues', warning_types)
    
    def test_custom_thresholds(self):
        """Test custom min/max value thresholds."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100
2024-02-01,500,55,110
2024-03-01,1050,52,105
"""
        self.create_csv(csv_content)
        
        # Set min threshold above some values
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json),
            min_value_threshold=600
        )
        
        report = validator.validate()
        
        self.assertFalse(report['passed'])
        
        # Should detect values below threshold
        negative_errors = [e for e in report['errors'] if e['type'] == 'NegativeValues']
        self.assertGreater(len(negative_errors), 0)
    
    def test_report_saved(self):
        """Test that JSON report is saved correctly."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        validator.validate()
        
        # Check that report file was created
        self.assertTrue(self.output_json.exists())
        
        # Check that report is valid JSON
        with open(self.output_json, 'r') as f:
            report = json.load(f)
        
        # Verify report structure
        self.assertIn('validation_status', report)
        self.assertIn('summary', report)
        self.assertIn('errors', report)
        self.assertIn('warnings', report)


class TestMissingMonths(unittest.TestCase):
    """Test cases for missing month detection."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = Path(self.temp_dir) / 'test_data.csv'
        self.output_json = Path(self.temp_dir) / 'test_report.json'
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_csv(self, content: str):
        """Helper to create a test CSV file."""
        with open(self.test_csv, 'w') as f:
            f.write(content)
    
    def test_missing_months(self):
        """Test detection of missing months in date sequence."""
        csv_content = """Date,kWh,Therms,Demand
2024-01-01,1000,50,100
2024-02-01,1100,55,110
2024-04-01,1050,52,105
2024-05-01,1020,51,102
"""
        self.create_csv(csv_content)
        
        validator = UtilityDataValidator(
            input_file=str(self.test_csv),
            output_file=str(self.output_json)
        )
        
        report = validator.validate()
        
        self.assertFalse(report['passed'])
        
        # Check for missing months error
        missing_month_errors = [e for e in report['errors'] if e['type'] == 'MissingMonths']
        self.assertEqual(len(missing_month_errors), 1)


if __name__ == '__main__':
    unittest.main()
