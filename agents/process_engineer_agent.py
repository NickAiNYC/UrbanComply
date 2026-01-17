"""
Process Engineer Agent Module for UrbanComply

The Process Engineer Agent is responsible for:
- Compliance process mapping and documentation
- Edge case scenario documentation
- NYC regulation tracking
- ENERGY STAR Portfolio Manager workflow documentation
- Handoffs to Validator and Scriptsmith agents
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from agents.base_agent import BaseAgent


class ProcessEngineerAgent(BaseAgent):
    """
    Agent responsible for documenting and managing compliance processes
    for NYC LL84/33 benchmarking.
    
    Collaborates with:
    - Pilot Hunter (receives customer data)
    - Scriptsmith (sends edge cases and error logs)
    - Validator (sends process docs for compliance checks)
    """
    
    # NYC LL84/33 Process Categories
    PROCESS_CATEGORIES = [
        'data_collection',
        'validation',
        'submission',
        'compliance_check',
        'reporting',
        'error_handling'
    ]
    
    # Standard LL84/33 workflow steps
    LL84_WORKFLOW = [
        {
            'step': 1,
            'name': 'Utility Data Collection',
            'description': 'Gather 12 months of utility data (electricity, gas) for the building',
            'required_fields': ['Date', 'kWh', 'Therms', 'Demand'],
            'responsible_party': 'Building owner or energy consultant'
        },
        {
            'step': 2,
            'name': 'Data Validation',
            'description': 'Validate utility data for completeness, accuracy, and format compliance',
            'responsible_party': 'Validator Agent'
        },
        {
            'step': 3,
            'name': 'ENERGY STAR Portfolio Manager Entry',
            'description': 'Enter or sync utility data to ENERGY STAR Portfolio Manager',
            'responsible_party': 'Building owner or authorized agent'
        },
        {
            'step': 4,
            'name': 'Generate Benchmark Report',
            'description': 'Generate the energy benchmark report from Portfolio Manager',
            'responsible_party': 'System'
        },
        {
            'step': 5,
            'name': 'NYC DOB Submission',
            'description': 'Submit benchmark data to NYC Department of Buildings',
            'responsible_party': 'Building owner or authorized agent',
            'deadline': 'May 1st annually'
        },
        {
            'step': 6,
            'name': 'Confirmation & Record Keeping',
            'description': 'Save confirmation number and maintain audit trail',
            'responsible_party': 'System'
        }
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Process Engineer Agent.
        
        Args:
            config: Optional configuration with keys:
                - output_dir: Directory for process documentation
                - regulation_year: Current regulation year (default: current year)
        """
        super().__init__(name='process_engineer', config=config)
        
        self.output_dir = config.get('output_dir', '.') if config else '.'
        self.regulation_year = config.get('regulation_year', datetime.now().year) if config else datetime.now().year
        
        # Store process documentation
        self.process_docs: Dict[str, Dict[str, Any]] = {}
        self.edge_cases: List[Dict[str, Any]] = []
        self.error_logs: List[Dict[str, Any]] = []
    
    def get_capabilities(self) -> List[str]:
        """Return the capabilities of the Process Engineer Agent."""
        return [
            'document_process',
            'track_edge_cases',
            'generate_workflow_diagram',
            'create_checklist',
            'monitor_regulations',
            'handoff_to_validator',
            'handoff_to_scriptsmith',
            'receive_from_pilot_hunter'
        ]
    
    def run(self, 
            action: str = 'generate_documentation',
            **kwargs) -> Dict[str, Any]:
        """
        Execute a process engineering action.
        
        Args:
            action: Action to perform:
                - 'generate_documentation': Create full process documentation
                - 'document_process': Document a specific process
                - 'add_edge_case': Add an edge case scenario
                - 'create_checklist': Generate a compliance checklist
            **kwargs: Action-specific parameters
            
        Returns:
            Result dictionary based on the action
        """
        self.log_activity('process_engineering', 'started', {'action': action})
        
        try:
            if action == 'generate_documentation':
                result = self.generate_full_documentation(**kwargs)
            elif action == 'document_process':
                result = self.document_process(**kwargs)
            elif action == 'add_edge_case':
                result = self.add_edge_case(**kwargs)
            elif action == 'create_checklist':
                result = self.create_compliance_checklist(**kwargs)
            else:
                raise ValueError(f"Unknown action: {action}")
            
            self.log_activity('process_engineering', 'completed', {
                'action': action,
                'result_keys': list(result.keys())
            })
            
            self.status = 'ready'
            return result
            
        except Exception as e:
            self.log_activity('process_engineering', 'failed',
                            {'action': action},
                            error_message=str(e))
            self.status = 'error'
            raise
    
    def generate_full_documentation(self, 
                                     output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive LL84/33 process documentation.
        
        Args:
            output_file: Optional path to save documentation
            
        Returns:
            Complete process documentation dictionary
        """
        documentation = {
            'title': f'NYC LL84/33 Compliance Process Documentation',
            'generated_at': datetime.now().isoformat(),
            'regulation_year': self.regulation_year,
            'overview': {
                'purpose': 'Document the complete workflow for NYC Local Law 84/33 energy benchmarking compliance',
                'applicable_buildings': 'Buildings over 25,000 sq ft (LL84) or 10,000 sq ft (LL33)',
                'deadline': 'May 1st annually',
                'penalties': 'Fines for non-compliance, public disclosure'
            },
            'workflow': self.LL84_WORKFLOW,
            'data_requirements': self._get_data_requirements(),
            'validation_rules': self._get_validation_rules(),
            'edge_cases': self.edge_cases,
            'common_errors': self._get_common_errors(),
            'automation_status': self._get_automation_status()
        }
        
        if output_file:
            self.save_report(documentation, output_file)
        
        return documentation
    
    def document_process(self,
                         process_name: str,
                         category: str,
                         description: str,
                         steps: List[Dict[str, Any]],
                         edge_cases: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Document a specific process.
        
        Args:
            process_name: Name of the process
            category: Process category (from PROCESS_CATEGORIES)
            description: Process description
            steps: List of step dictionaries
            edge_cases: Optional list of edge case descriptions
            
        Returns:
            The documented process
        """
        if category not in self.PROCESS_CATEGORIES:
            raise ValueError(f"Invalid category. Must be one of: {self.PROCESS_CATEGORIES}")
        
        process_doc = {
            'process_name': process_name,
            'category': category,
            'description': description,
            'steps': steps,
            'edge_cases': edge_cases or [],
            'automation_status': 'manual',
            'created_at': datetime.now().isoformat(),
            'created_by': self.name,
            'version': '1.0'
        }
        
        self.process_docs[process_name] = process_doc
        
        self.logger.info(f"Documented process: {process_name}")
        return process_doc
    
    def add_edge_case(self,
                      scenario: str,
                      process_affected: str,
                      description: str,
                      recommended_handling: str,
                      severity: str = 'medium') -> Dict[str, Any]:
        """
        Add an edge case scenario for documentation.
        
        Args:
            scenario: Short name for the edge case
            process_affected: Which process this affects
            description: Detailed description
            recommended_handling: How to handle this case
            severity: 'low', 'medium', or 'high'
            
        Returns:
            The edge case record
        """
        edge_case = {
            'id': len(self.edge_cases) + 1,
            'scenario': scenario,
            'process_affected': process_affected,
            'description': description,
            'recommended_handling': recommended_handling,
            'severity': severity,
            'documented_at': datetime.now().isoformat(),
            'status': 'documented'
        }
        
        self.edge_cases.append(edge_case)
        self.logger.info(f"Added edge case: {scenario}")
        
        return edge_case
    
    def create_compliance_checklist(self,
                                     building_id: Optional[str] = None,
                                     year: Optional[int] = None) -> Dict[str, Any]:
        """
        Create a compliance checklist for LL84/33 submission.
        
        Args:
            building_id: Optional building identifier
            year: Compliance year (defaults to current regulation year)
            
        Returns:
            Checklist dictionary
        """
        year = year or self.regulation_year
        
        checklist = {
            'title': f'LL84/33 Compliance Checklist - {year}',
            'building_id': building_id,
            'created_at': datetime.now().isoformat(),
            'deadline': f'{year}-05-01',
            'items': [
                {
                    'id': 1,
                    'task': 'Gather 12 months of utility data',
                    'category': 'data_collection',
                    'required': True,
                    'status': 'pending',
                    'notes': 'Jan-Dec of previous year'
                },
                {
                    'id': 2,
                    'task': 'Validate utility data for completeness',
                    'category': 'validation',
                    'required': True,
                    'status': 'pending',
                    'notes': 'Use Validator Agent'
                },
                {
                    'id': 3,
                    'task': 'Check for negative or irrational values',
                    'category': 'validation',
                    'required': True,
                    'status': 'pending',
                    'notes': 'Flag any anomalies'
                },
                {
                    'id': 4,
                    'task': 'Verify all months are present',
                    'category': 'validation',
                    'required': True,
                    'status': 'pending',
                    'notes': 'No gaps in data'
                },
                {
                    'id': 5,
                    'task': 'Log into ENERGY STAR Portfolio Manager',
                    'category': 'submission',
                    'required': True,
                    'status': 'pending',
                    'notes': 'Use authorized account'
                },
                {
                    'id': 6,
                    'task': 'Enter/update utility data in Portfolio Manager',
                    'category': 'submission',
                    'required': True,
                    'status': 'pending',
                    'notes': 'Match validated data exactly'
                },
                {
                    'id': 7,
                    'task': 'Generate benchmark report',
                    'category': 'submission',
                    'required': True,
                    'status': 'pending',
                    'notes': 'Download for records'
                },
                {
                    'id': 8,
                    'task': 'Submit to NYC DOB',
                    'category': 'submission',
                    'required': True,
                    'status': 'pending',
                    'notes': f'Before May 1, {year}'
                },
                {
                    'id': 9,
                    'task': 'Save confirmation number',
                    'category': 'compliance_check',
                    'required': True,
                    'status': 'pending',
                    'notes': 'Critical for audit trail'
                },
                {
                    'id': 10,
                    'task': 'Archive all documentation',
                    'category': 'reporting',
                    'required': True,
                    'status': 'pending',
                    'notes': 'Keep for 3 years minimum'
                }
            ]
        }
        
        self.logger.info(f"Created compliance checklist for {year}")
        return checklist
    
    def handoff_to_validator(self, 
                             process_doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send process documentation to Validator for compliance check.
        
        Args:
            process_doc: Process documentation to validate
            
        Returns:
            Handoff record
        """
        return self.handoff(
            target_agent='validator',
            data=process_doc,
            message='Process documentation for compliance validation'
        )
    
    def handoff_to_scriptsmith(self,
                               edge_cases: Optional[List[Dict[str, Any]]] = None,
                               error_logs: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Send edge cases and error logs to Scriptsmith for automation.
        
        Args:
            edge_cases: Edge cases to address
            error_logs: Error logs for debugging
            
        Returns:
            Handoff record
        """
        data = {
            'edge_cases': edge_cases or self.edge_cases,
            'error_logs': error_logs or self.error_logs,
            'automation_requests': self._generate_automation_requests()
        }
        
        return self.handoff(
            target_agent='scriptsmith',
            data=data,
            message='Edge cases and error logs for automation development'
        )
    
    def receive_from_pilot_hunter(self, 
                                   handoff: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receive customer data from Pilot Hunter.
        
        Args:
            handoff: Handoff record from Pilot Hunter
            
        Returns:
            Processed customer data
        """
        customer_data = self.receive_handoff(handoff)
        
        # Create a checklist for this customer
        if customer_data.get('building_id'):
            checklist = self.create_compliance_checklist(
                building_id=customer_data['building_id']
            )
            customer_data['compliance_checklist'] = checklist
        
        self.logger.info("Received customer data from Pilot Hunter")
        return customer_data
    
    def _get_data_requirements(self) -> Dict[str, Any]:
        """Get standard data requirements for LL84/33."""
        return {
            'utility_data': {
                'required_columns': ['Date', 'kWh', 'Therms', 'Demand'],
                'date_format': 'YYYY-MM-DD recommended',
                'coverage': '12 consecutive months',
                'acceptable_formats': ['CSV', 'Excel']
            },
            'building_info': {
                'required_fields': [
                    'BIN (Building Identification Number)',
                    'Address',
                    'Gross Floor Area',
                    'Building Type',
                    'Year Built'
                ]
            },
            'energy_star': {
                'required': 'Portfolio Manager Property ID',
                'account_type': 'Full access for submission'
            }
        }
    
    def _get_validation_rules(self) -> List[Dict[str, Any]]:
        """Get validation rules for LL84/33 data."""
        return [
            {
                'rule': 'Date Coverage',
                'description': 'Data must cover 12 consecutive months',
                'severity': 'error'
            },
            {
                'rule': 'No Negative Values',
                'description': 'Utility values cannot be negative',
                'severity': 'error'
            },
            {
                'rule': 'No Duplicates',
                'description': 'Each month should appear only once',
                'severity': 'error'
            },
            {
                'rule': 'Numeric Columns',
                'description': 'kWh, Therms, Demand must be numeric',
                'severity': 'error'
            },
            {
                'rule': 'Unit Consistency',
                'description': 'Values should be consistent (watch for unit mismatches)',
                'severity': 'warning'
            },
            {
                'rule': 'Reasonable Range',
                'description': 'Values should be within expected ranges for building size',
                'severity': 'warning'
            }
        ]
    
    def _get_common_errors(self) -> List[Dict[str, Any]]:
        """Get common errors encountered in LL84/33 submissions."""
        return [
            {
                'error': 'Missing Months',
                'cause': "Utility provider didn't provide all 12 months",
                'solution': 'Contact utility provider for missing data'
            },
            {
                'error': 'Unit Mismatch',
                'cause': 'Data exported in wrong units (e.g., MWh vs kWh)',
                'solution': 'Verify units with utility provider, convert if needed'
            },
            {
                'error': 'BIN Mismatch',
                'cause': "Building ID in Portfolio Manager doesn't match DOB records",
                'solution': 'Verify BIN at NYC DOB BIS website'
            },
            {
                'error': 'Late Submission',
                'cause': 'Submitted after May 1st deadline',
                'solution': 'Submit ASAP, may incur late filing penalty'
            },
            {
                'error': 'Duplicate Entry',
                'cause': 'Same building submitted twice',
                'solution': 'Contact DOB to resolve duplicate submissions'
            }
        ]
    
    def _get_automation_status(self) -> Dict[str, Any]:
        """Get current automation status for each process."""
        return {
            'data_collection': {
                'status': 'manual',
                'automated_by': None,
                'notes': 'Requires utility provider integration'
            },
            'validation': {
                'status': 'automated',
                'automated_by': 'Validator Agent (check_utility_data.py)',
                'notes': 'Fully functional'
            },
            'submission': {
                'status': 'manual',
                'automated_by': None,
                'notes': 'Requires ENERGY STAR API integration'
            },
            'compliance_check': {
                'status': 'partial',
                'automated_by': 'Validator Agent',
                'notes': 'Pre-submission checks automated'
            },
            'reporting': {
                'status': 'partial',
                'automated_by': 'Validator Agent (JSON reports)',
                'notes': 'PDF generation pending'
            }
        }
    
    def _generate_automation_requests(self) -> List[Dict[str, Any]]:
        """Generate automation requests for Scriptsmith."""
        requests = []
        
        # Check what's not yet automated
        status = self._get_automation_status()
        
        for process, info in status.items():
            if info['status'] in ['manual', 'partial']:
                requests.append({
                    'process': process,
                    'current_status': info['status'],
                    'priority': 'high' if process == 'submission' else 'medium',
                    'notes': info['notes']
                })
        
        return requests
