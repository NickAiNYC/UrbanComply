"""
Base Agent Module for UrbanComply

Provides the abstract base class for all agents in the UrbanComply framework.
All agents must inherit from BaseAgent and implement required methods.
"""

import logging
import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class BaseAgent(ABC):
    """
    Abstract base class for all UrbanComply agents.
    
    Provides common functionality for:
    - Activity logging
    - Error handling
    - Status tracking
    - Inter-agent communication
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the base agent.
        
        Args:
            name: Agent identifier (e.g., 'validator', 'process_engineer')
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.status = 'initialized'
        self.activity_log: List[Dict[str, Any]] = []
        
        # Configure logging
        self.logger = logging.getLogger(f'urbancomply.{name}')
        self.logger.setLevel(logging.INFO)
        
        # Add handler if not already present
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(handler)
        
        self.logger.info(f"Agent '{name}' initialized")
    
    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the agent's primary function.
        
        Must be implemented by all subclasses.
        
        Returns:
            Dictionary containing execution results
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Return a list of capabilities this agent provides.
        
        Must be implemented by all subclasses.
        
        Returns:
            List of capability strings
        """
        pass
    
    def log_activity(self, 
                     activity_type: str, 
                     status: str, 
                     details: Optional[Dict[str, Any]] = None,
                     error_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Log an activity performed by this agent.
        
        Args:
            activity_type: Type of activity (e.g., 'validation', 'documentation')
            status: Status of the activity ('started', 'completed', 'failed')
            details: Optional dictionary with additional details
            error_message: Optional error message if status is 'failed'
            
        Returns:
            The logged activity record
        """
        activity = {
            'agent_name': self.name,
            'activity_type': activity_type,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'details': details or {},
            'error_message': error_message
        }
        
        self.activity_log.append(activity)
        
        if status == 'failed':
            self.logger.error(f"Activity '{activity_type}' failed: {error_message}")
        else:
            self.logger.info(f"Activity '{activity_type}' - Status: {status}")
        
        return activity
    
    def get_activity_log(self, 
                         activity_type: Optional[str] = None,
                         status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve activity log entries with optional filtering.
        
        Args:
            activity_type: Filter by activity type
            status: Filter by status
            
        Returns:
            List of matching activity records
        """
        results = self.activity_log
        
        if activity_type:
            results = [a for a in results if a['activity_type'] == activity_type]
        
        if status:
            results = [a for a in results if a['status'] == status]
        
        return results
    
    def handoff(self, 
                target_agent: str, 
                data: Dict[str, Any],
                message: str = '') -> Dict[str, Any]:
        """
        Prepare a handoff to another agent.
        
        Args:
            target_agent: Name of the receiving agent
            data: Data to pass to the target agent
            message: Optional message/context for the handoff
            
        Returns:
            Handoff record that can be processed by the target agent
        """
        handoff_record = {
            'from_agent': self.name,
            'to_agent': target_agent,
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'data': data
        }
        
        self.log_activity(
            activity_type='handoff',
            status='completed',
            details={'target_agent': target_agent, 'message': message}
        )
        
        self.logger.info(f"Handoff prepared for agent '{target_agent}'")
        return handoff_record
    
    def receive_handoff(self, handoff: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a handoff from another agent.
        
        Args:
            handoff: Handoff record from another agent
            
        Returns:
            Extracted data from the handoff
        """
        self.log_activity(
            activity_type='receive_handoff',
            status='completed',
            details={
                'from_agent': handoff.get('from_agent'),
                'message': handoff.get('message', '')
            }
        )
        
        self.logger.info(f"Received handoff from agent '{handoff.get('from_agent')}'")
        return handoff.get('data', {})
    
    def save_report(self, 
                    report_data: Dict[str, Any], 
                    output_path: str,
                    format: str = 'json') -> str:
        """
        Save a report to file.
        
        Args:
            report_data: Report data to save
            output_path: Path to save the report
            format: Output format ('json' only for now)
            
        Returns:
            Path to the saved report
        """
        output_file = Path(output_path)
        
        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        self.logger.info(f"Report saved to {output_file}")
        return str(output_file)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent.
        
        Returns:
            Dictionary with agent status information
        """
        completed_count = len([a for a in self.activity_log if a['status'] == 'completed'])
        failed_count = len([a for a in self.activity_log if a['status'] == 'failed'])
        
        return {
            'agent_name': self.name,
            'status': self.status,
            'total_activities': len(self.activity_log),
            'completed_activities': completed_count,
            'failed_activities': failed_count,
            'capabilities': self.get_capabilities()
        }
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', status='{self.status}')>"
