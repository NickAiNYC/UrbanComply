#!/usr/bin/env python3
"""
UrbanComply CLI - Agent-Based Compliance Automation

A command-line interface for the UrbanComply agent framework.
Provides access to the Validator and Process Engineer agents.
"""

import argparse
import json
import sys
from pathlib import Path


def cmd_validate(args):
    """Run validation on utility data."""
    from agents.validator_agent import ValidatorAgent
    
    agent = ValidatorAgent(config={
        'min_value_threshold': args.min_value,
        'max_value_threshold': args.max_value,
        'output_dir': str(Path(args.output).parent) if args.output else '.'
    })
    
    try:
        report = agent.run(
            input_file=args.input_file,
            output_file=args.output
        )
        
        print(f"\n{'='*60}")
        print("VALIDATION RESULTS")
        print(f"{'='*60}")
        print(f"Status: {report['validation_status']}")
        print(f"Rows Processed: {report['summary']['rows_processed']}")
        print(f"Errors: {report['summary']['total_errors']}")
        print(f"Warnings: {report['summary']['total_warnings']}")
        
        if report['errors']:
            print(f"\nErrors Found:")
            for error in report['errors'][:5]:  # Show first 5
                print(f"  - [{error['type']}] {error['message']}")
        
        if report['warnings']:
            print(f"\nWarnings:")
            for warning in report['warnings'][:5]:  # Show first 5
                print(f"  - [{warning['type']}] {warning['message']}")
        
        print(f"{'='*60}")
        
        return 0 if report['passed'] else 1
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_checklist(args):
    """Generate a compliance checklist."""
    from agents.process_engineer_agent import ProcessEngineerAgent
    
    agent = ProcessEngineerAgent(config={
        'output_dir': str(Path(args.output).parent) if args.output else '.',
        'regulation_year': args.year
    })
    
    try:
        checklist = agent.run(
            action='create_checklist',
            building_id=args.building_id,
            year=args.year
        )
        
        print(f"\n{'='*60}")
        print(f"COMPLIANCE CHECKLIST - {args.year}")
        print(f"{'='*60}")
        
        if args.building_id:
            print(f"Building ID: {args.building_id}")
        
        print(f"Deadline: {checklist['deadline']}")
        print(f"\nTasks:")
        
        for item in checklist['items']:
            status_icon = '[ ]' if item['status'] == 'pending' else '[✓]'
            required = '*' if item['required'] else ' '
            print(f"  {status_icon}{required} {item['id']}. {item['task']}")
            if item.get('notes'):
                print(f"        Note: {item['notes']}")
        
        print(f"\n* = Required")
        print(f"{'='*60}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(checklist, f, indent=2)
            print(f"\nSaved to: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_docs(args):
    """Generate process documentation."""
    from agents.process_engineer_agent import ProcessEngineerAgent
    
    agent = ProcessEngineerAgent(config={
        'output_dir': str(Path(args.output).parent) if args.output else '.',
        'regulation_year': args.year
    })
    
    try:
        docs = agent.run(
            action='generate_documentation',
            output_file=args.output
        )
        
        print(f"\n{'='*60}")
        print("PROCESS DOCUMENTATION GENERATED")
        print(f"{'='*60}")
        print(f"Title: {docs['title']}")
        print(f"Regulation Year: {docs['regulation_year']}")
        print(f"Workflow Steps: {len(docs['workflow'])}")
        print(f"Validation Rules: {len(docs['validation_rules'])}")
        print(f"Common Errors Documented: {len(docs['common_errors'])}")
        
        if args.output:
            print(f"\nSaved to: {args.output}")
        
        print(f"{'='*60}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_status(args):
    """Show agent status."""
    from agents.validator_agent import ValidatorAgent
    from agents.process_engineer_agent import ProcessEngineerAgent
    
    print(f"\n{'='*60}")
    print("URBANCOMPLY AGENT STATUS")
    print(f"{'='*60}")
    
    agents = [
        ValidatorAgent(),
        ProcessEngineerAgent()
    ]
    
    for agent in agents:
        status = agent.get_status()
        print(f"\n{status['agent_name'].upper()}")
        print(f"  Status: {status['status']}")
        print(f"  Capabilities: {len(status['capabilities'])}")
        for cap in status['capabilities'][:5]:
            print(f"    - {cap}")
        if len(status['capabilities']) > 5:
            print(f"    ... and {len(status['capabilities']) - 5} more")
    
    print(f"\n{'='*60}")
    print("Available Agents: validator, process_engineer")
    print("Coming Soon: pilot_hunter, scriptsmith, scale_scout")
    print(f"{'='*60}")
    
    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='UrbanComply - NYC LL84/33 Compliance Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s validate utility_data.csv
  %(prog)s checklist --building-id BLD123 --year 2025
  %(prog)s docs -o process_docs.json
  %(prog)s status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate utility data')
    validate_parser.add_argument('input_file', help='Path to utility data CSV')
    validate_parser.add_argument('-o', '--output', help='Output report path')
    validate_parser.add_argument('--min-value', type=float, default=0.0,
                                help='Minimum acceptable utility value for validation (default: 0.0)')
    validate_parser.add_argument('--max-value', type=float, default=1e9,
                                help='Maximum acceptable utility value for validation (default: 1e9)')
    
    # Checklist command
    checklist_parser = subparsers.add_parser('checklist', help='Generate compliance checklist')
    checklist_parser.add_argument('-b', '--building-id', help='Building identifier')
    checklist_parser.add_argument('-y', '--year', type=int, default=2025,
                                 help='Compliance year')
    checklist_parser.add_argument('-o', '--output', help='Output file path')
    
    # Documentation command
    docs_parser = subparsers.add_parser('docs', help='Generate process documentation')
    docs_parser.add_argument('-y', '--year', type=int, default=2025,
                            help='Regulation year')
    docs_parser.add_argument('-o', '--output', help='Output file path')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show agent status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    if args.command == 'validate':
        return cmd_validate(args)
    elif args.command == 'checklist':
        return cmd_checklist(args)
    elif args.command == 'docs':
        return cmd_docs(args)
    elif args.command == 'status':
        return cmd_status(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
