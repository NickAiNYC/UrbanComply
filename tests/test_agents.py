"""
Tests for the UrbanComply Agent Framework

Tests the base agent functionality and the ProcessEngineerAgent.
"""

import unittest
import tempfile
import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from agents.process_engineer_agent import ProcessEngineerAgent
from agents.validator_agent import ValidatorAgent


class ConcreteTestAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing."""
    
    def run(self, **kwargs):
        return {'status': 'success', 'message': 'Test agent ran'}
    
    def get_capabilities(self):
        return ['test_capability_1', 'test_capability_2']


class TestBaseAgent(unittest.TestCase):
    """Test cases for BaseAgent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = ConcreteTestAgent(name='test_agent')
    
    def test_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.name, 'test_agent')
        self.assertEqual(self.agent.status, 'initialized')
        self.assertEqual(len(self.agent.activity_log), 0)
    
    def test_log_activity(self):
        """Test activity logging."""
        activity = self.agent.log_activity(
            activity_type='test_activity',
            status='completed',
            details={'test_key': 'test_value'}
        )
        
        self.assertEqual(activity['agent_name'], 'test_agent')
        self.assertEqual(activity['activity_type'], 'test_activity')
        self.assertEqual(activity['status'], 'completed')
        self.assertIn('timestamp', activity)
        self.assertEqual(len(self.agent.activity_log), 1)
    
    def test_log_failed_activity(self):
        """Test logging a failed activity."""
        activity = self.agent.log_activity(
            activity_type='failing_activity',
            status='failed',
            error_message='Test error'
        )
        
        self.assertEqual(activity['status'], 'failed')
        self.assertEqual(activity['error_message'], 'Test error')
    
    def test_get_activity_log_filtering(self):
        """Test activity log filtering."""
        self.agent.log_activity('type_a', 'completed')
        self.agent.log_activity('type_b', 'completed')
        self.agent.log_activity('type_a', 'failed')
        
        # Filter by type
        type_a_logs = self.agent.get_activity_log(activity_type='type_a')
        self.assertEqual(len(type_a_logs), 2)
        
        # Filter by status
        completed_logs = self.agent.get_activity_log(status='completed')
        self.assertEqual(len(completed_logs), 2)
        
        # Filter by both
        type_a_failed = self.agent.get_activity_log(activity_type='type_a', status='failed')
        self.assertEqual(len(type_a_failed), 1)
    
    def test_handoff(self):
        """Test handoff preparation."""
        handoff = self.agent.handoff(
            target_agent='other_agent',
            data={'key': 'value'},
            message='Test handoff'
        )
        
        self.assertEqual(handoff['from_agent'], 'test_agent')
        self.assertEqual(handoff['to_agent'], 'other_agent')
        self.assertEqual(handoff['data'], {'key': 'value'})
        self.assertEqual(handoff['message'], 'Test handoff')
    
    def test_receive_handoff(self):
        """Test receiving a handoff."""
        handoff = {
            'from_agent': 'sender_agent',
            'to_agent': 'test_agent',
            'data': {'received_key': 'received_value'},
            'message': 'Incoming handoff'
        }
        
        data = self.agent.receive_handoff(handoff)
        self.assertEqual(data, {'received_key': 'received_value'})
    
    def test_get_status(self):
        """Test getting agent status."""
        self.agent.log_activity('test', 'completed')
        self.agent.log_activity('test', 'failed')
        
        status = self.agent.get_status()
        
        self.assertEqual(status['agent_name'], 'test_agent')
        self.assertEqual(status['total_activities'], 2)
        self.assertEqual(status['completed_activities'], 1)
        self.assertEqual(status['failed_activities'], 1)
        self.assertIn('capabilities', status)
    
    def test_get_capabilities(self):
        """Test getting capabilities."""
        capabilities = self.agent.get_capabilities()
        self.assertIn('test_capability_1', capabilities)
        self.assertIn('test_capability_2', capabilities)
    
    def test_run(self):
        """Test run method."""
        result = self.agent.run()
        self.assertEqual(result['status'], 'success')


class TestProcessEngineerAgent(unittest.TestCase):
    """Test cases for ProcessEngineerAgent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.agent = ProcessEngineerAgent(config={
            'output_dir': self.temp_dir,
            'regulation_year': 2025
        })
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.name, 'process_engineer')
        self.assertEqual(self.agent.regulation_year, 2025)
    
    def test_get_capabilities(self):
        """Test capabilities list."""
        capabilities = self.agent.get_capabilities()
        self.assertIn('document_process', capabilities)
        self.assertIn('track_edge_cases', capabilities)
        self.assertIn('create_checklist', capabilities)
    
    def test_generate_full_documentation(self):
        """Test generating full documentation."""
        result = self.agent.run(action='generate_documentation')
        
        self.assertIn('title', result)
        self.assertIn('workflow', result)
        self.assertIn('data_requirements', result)
        self.assertIn('validation_rules', result)
        self.assertEqual(result['regulation_year'], 2025)
    
    def test_document_process(self):
        """Test documenting a process."""
        result = self.agent.run(
            action='document_process',
            process_name='Test Process',
            category='validation',
            description='A test process',
            steps=[
                {'step': 1, 'action': 'Do something'},
                {'step': 2, 'action': 'Do something else'}
            ]
        )
        
        self.assertEqual(result['process_name'], 'Test Process')
        self.assertEqual(result['category'], 'validation')
        self.assertEqual(len(result['steps']), 2)
    
    def test_document_process_invalid_category(self):
        """Test that invalid category raises error."""
        with self.assertRaises(ValueError):
            self.agent.run(
                action='document_process',
                process_name='Test',
                category='invalid_category',
                description='Test',
                steps=[]
            )
    
    def test_add_edge_case(self):
        """Test adding an edge case."""
        result = self.agent.run(
            action='add_edge_case',
            scenario='Missing utility bill',
            process_affected='data_collection',
            description='Utility company failed to provide bill for one month',
            recommended_handling='Contact utility company for historical data',
            severity='high'
        )
        
        self.assertEqual(result['scenario'], 'Missing utility bill')
        self.assertEqual(result['severity'], 'high')
        self.assertEqual(len(self.agent.edge_cases), 1)
    
    def test_create_compliance_checklist(self):
        """Test creating a compliance checklist."""
        result = self.agent.run(
            action='create_checklist',
            building_id='TEST123',
            year=2025
        )
        
        self.assertEqual(result['building_id'], 'TEST123')
        self.assertIn('items', result)
        self.assertGreater(len(result['items']), 0)
        
        # Check that items have required fields
        for item in result['items']:
            self.assertIn('task', item)
            self.assertIn('status', item)
            self.assertIn('required', item)
    
    def test_handoff_to_validator(self):
        """Test handoff to Validator."""
        process_doc = {'name': 'test', 'steps': []}
        handoff = self.agent.handoff_to_validator(process_doc)
        
        self.assertEqual(handoff['to_agent'], 'validator')
        self.assertEqual(handoff['from_agent'], 'process_engineer')
    
    def test_handoff_to_scriptsmith(self):
        """Test handoff to Scriptsmith."""
        # Add an edge case first
        self.agent.add_edge_case(
            scenario='Test case',
            process_affected='validation',
            description='Test',
            recommended_handling='Test'
        )
        
        handoff = self.agent.handoff_to_scriptsmith()
        
        self.assertEqual(handoff['to_agent'], 'scriptsmith')
        self.assertIn('edge_cases', handoff['data'])
        self.assertIn('automation_requests', handoff['data'])
    
    def test_receive_from_pilot_hunter(self):
        """Test receiving data from Pilot Hunter."""
        handoff = {
            'from_agent': 'pilot_hunter',
            'to_agent': 'process_engineer',
            'data': {
                'building_id': 'BLD001',
                'customer_name': 'Test Customer'
            },
            'message': 'New pilot customer'
        }
        
        result = self.agent.receive_from_pilot_hunter(handoff)
        
        self.assertEqual(result['building_id'], 'BLD001')
        self.assertIn('compliance_checklist', result)
    
    def test_save_documentation(self):
        """Test saving documentation to file."""
        output_file = os.path.join(self.temp_dir, 'test_doc.json')
        
        result = self.agent.run(
            action='generate_documentation',
            output_file=output_file
        )
        
        self.assertTrue(os.path.exists(output_file))
        
        with open(output_file, 'r') as f:
            saved_doc = json.load(f)
        
        self.assertEqual(saved_doc['regulation_year'], 2025)


class TestValidatorAgent(unittest.TestCase):
    """Test cases for ValidatorAgent."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.agent = ValidatorAgent(config={
            'output_dir': self.temp_dir
        })
        
        # Create a test CSV
        self.test_csv = os.path.join(self.temp_dir, 'test_data.csv')
        with open(self.test_csv, 'w') as f:
            f.write("Date,kWh,Therms,Demand\n")
            f.write("2024-01-01,1000,50,100\n")
            f.write("2024-02-01,1100,55,110\n")
            f.write("2024-03-01,1050,52,105\n")
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.name, 'validator')
    
    def test_get_capabilities(self):
        """Test capabilities list."""
        capabilities = self.agent.get_capabilities()
        self.assertIn('validate_utility_data', capabilities)
        self.assertIn('generate_validation_report', capabilities)
    
    def test_run_validation(self):
        """Test running validation."""
        result = self.agent.run(input_file=self.test_csv)
        
        self.assertTrue(result['passed'])
        self.assertEqual(result['validation_status'], 'PASS')
    
    def test_validation_summary(self):
        """Test validation summary."""
        self.agent.run(input_file=self.test_csv)
        summary = self.agent.get_validation_summary()
        
        self.assertEqual(summary['total_validations'], 1)
        self.assertEqual(summary['passed'], 1)
        self.assertIn(self.test_csv, summary['files_validated'])
    
    def test_handoff_to_process_engineer(self):
        """Test handoff to Process Engineer."""
        report = self.agent.run(input_file=self.test_csv)
        handoff = self.agent.handoff_to_process_engineer(report)
        
        self.assertEqual(handoff['to_agent'], 'process_engineer')
        self.assertIn('validation_status', handoff['data'])


if __name__ == '__main__':
    unittest.main()
