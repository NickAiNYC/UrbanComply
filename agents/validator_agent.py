"""
Validator Agent Module for UrbanComply

The Validator Agent is responsible for:
- Data validation and quality assurance
- Compliance checks against NYC DOB requirements
- Validation report generation
- Providing feedback to Process Engineer and Scriptsmith agents
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base_agent import BaseAgent


class ValidatorAgent(BaseAgent):
    """
    Agent responsible for validating utility data and ensuring compliance
    with NYC LL84/33 requirements.
    
    Wraps the check_utility_data.py validation logic and provides
    agent-based interface for the UrbanComply framework.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Validator Agent.
        
        Args:
            config: Optional configuration with keys:
                - min_value_threshold: Minimum acceptable numeric value
                - max_value_threshold: Maximum acceptable numeric value
                - output_dir: Directory for validation reports
        """
        super().__init__(name='validator', config=config)
        
        self.min_value_threshold = config.get('min_value_threshold', 0.0) if config else 0.0
        self.max_value_threshold = config.get('max_value_threshold', 1e9) if config else 1e9
        self.output_dir = config.get('output_dir', '.') if config else '.'
        
        self.validation_results: List[Dict[str, Any]] = []
    
    def get_capabilities(self) -> List[str]:
        """Return the capabilities of the Validator Agent."""
        return [
            'validate_utility_data',
            'validate_submission',
            'check_compliance',
            'generate_validation_report',
            'detect_anomalies',
            'provide_feedback_to_scriptsmith',
            'provide_feedback_to_process_engineer'
        ]
    
    def run(self, 
            input_file: str,
            output_file: Optional[str] = None,
            **kwargs) -> Dict[str, Any]:
        """
        Run validation on a utility data file.
        
        Args:
            input_file: Path to the CSV file to validate
            output_file: Optional path for the validation report
            **kwargs: Additional validation parameters
            
        Returns:
            Validation report dictionary
        """
        from check_utility_data import UtilityDataValidator
        
        self.log_activity('validation', 'started', {'input_file': input_file})
        
        try:
            # Generate output path if not provided
            if not output_file:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f"{self.output_dir}/validation_report_{timestamp}.json"
            
            # Run validation
            validator = UtilityDataValidator(
                input_file=input_file,
                output_file=output_file,
                min_value_threshold=kwargs.get('min_value', self.min_value_threshold),
                max_value_threshold=kwargs.get('max_value', self.max_value_threshold)
            )
            
            report = validator.validate()
            
            # Store result
            self.validation_results.append({
                'input_file': input_file,
                'timestamp': datetime.now().isoformat(),
                'report': report
            })
            
            status = 'completed' if report['passed'] else 'completed_with_errors'
            self.log_activity('validation', status, {
                'input_file': input_file,
                'passed': report['passed'],
                'errors': report['summary']['total_errors'],
                'warnings': report['summary']['total_warnings']
            })
            
            self.status = 'ready'
            return report
            
        except Exception as e:
            self.log_activity('validation', 'failed', 
                            {'input_file': input_file}, 
                            error_message=str(e))
            self.status = 'error'
            raise
    
    def validate_multiple(self, input_files: List[str]) -> List[Dict[str, Any]]:
        """
        Validate multiple utility data files.
        
        Args:
            input_files: List of paths to CSV files
            
        Returns:
            List of validation reports
        """
        reports = []
        for file_path in input_files:
            try:
                report = self.run(input_file=file_path)
                reports.append({
                    'file': file_path,
                    'status': 'success',
                    'report': report
                })
            except Exception as e:
                reports.append({
                    'file': file_path,
                    'status': 'error',
                    'error': str(e)
                })
        
        return reports
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all validations performed.
        
        Returns:
            Summary dictionary with statistics
        """
        total = len(self.validation_results)
        passed = len([r for r in self.validation_results if r['report']['passed']])
        failed = total - passed
        
        total_errors = sum(
            r['report']['summary']['total_errors'] 
            for r in self.validation_results
        )
        total_warnings = sum(
            r['report']['summary']['total_warnings'] 
            for r in self.validation_results
        )
        
        return {
            'total_validations': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': f"{(passed/total*100):.1f}%" if total > 0 else "N/A",
            'total_errors_found': total_errors,
            'total_warnings_found': total_warnings,
            'files_validated': [r['input_file'] for r in self.validation_results]
        }
    
    def handoff_to_process_engineer(self, 
                                     validation_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare a handoff to the Process Engineer with compliance feedback.
        
        Args:
            validation_report: The validation report to hand off
            
        Returns:
            Handoff record for Process Engineer
        """
        # Extract relevant feedback for process documentation
        feedback = {
            'validation_status': validation_report['validation_status'],
            'error_types_found': list(set(e['type'] for e in validation_report['errors'])),
            'warning_types_found': list(set(w['type'] for w in validation_report['warnings'])),
            'recommendations': self._generate_process_recommendations(validation_report)
        }
        
        return self.handoff(
            target_agent='process_engineer',
            data=feedback,
            message='Validation feedback for process documentation update'
        )
    
    def handoff_to_scriptsmith(self, 
                               validation_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare a handoff to Scriptsmith with anomaly reports for debugging.
        
        Args:
            validation_report: The validation report to hand off
            
        Returns:
            Handoff record for Scriptsmith
        """
        # Extract anomalies for script improvement
        anomalies = {
            'errors': validation_report['errors'],
            'warnings': validation_report['warnings'],
            'suggested_fixes': self._generate_script_suggestions(validation_report)
        }
        
        return self.handoff(
            target_agent='scriptsmith',
            data=anomalies,
            message='Anomaly report for automation script debugging'
        )
    
    def _generate_process_recommendations(self, 
                                          report: Dict[str, Any]) -> List[str]:
        """Generate process recommendations based on validation results."""
        recommendations = []
        
        error_types = [e['type'] for e in report['errors']]
        
        if 'MissingColumns' in error_types:
            recommendations.append(
                "Update data collection process to ensure all required columns are present"
            )
        
        if 'MissingMonths' in error_types:
            recommendations.append(
                "Implement monthly data collection reminders to prevent gaps"
            )
        
        if 'NegativeValues' in error_types:
            recommendations.append(
                "Add data entry validation to prevent negative utility values"
            )
        
        if 'DuplicateRows' in error_types:
            recommendations.append(
                "Review data import process to prevent duplicate entries"
            )
        
        return recommendations
    
    def _generate_script_suggestions(self, 
                                     report: Dict[str, Any]) -> List[str]:
        """Generate script improvement suggestions based on validation results."""
        suggestions = []
        
        error_types = [e['type'] for e in report['errors']]
        
        if 'InvalidDates' in error_types:
            suggestions.append(
                "Enhance date parsing to handle additional date formats"
            )
        
        if 'NonNumericValues' in error_types:
            suggestions.append(
                "Add data cleaning step to handle numeric values with units/symbols"
            )
        
        if 'PotentialUnitMismatch' in [w['type'] for w in report['warnings']]:
            suggestions.append(
                "Implement unit conversion detection and normalization"
            )
        
        return suggestions
