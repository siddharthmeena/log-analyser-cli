"""
Log Analyser CLI - Main Entry Point

This module serves as the command-line interface for the Log Analyser application.
It handles argument parsing, orchestrates the log parsing and formatting workflow,
and manages output presentation to the user.

Author: Log Analyser Team
Date: 2026
"""

import argparse
from datetime import datetime
import sys
from collections import Counter

from formatters import format_errors, format_summary
from parser import LogParser

def parse_arguments():
    """
    Parse and return command-line arguments.
    
    Configures the ArgumentParser with the following options:
    - --file: Path to the log file to be analysed (required)
    - --format: Types of analysis to perform (summary, errors, timeline)
    - --level: Minimum log level filter (DEBUG, INFO, WARNING, ERROR)
    - --since: Start date for analysis (YYYY-MM-DD format)
    - --output/-o: Output file path for results
    
    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description='Log Analyser')
    # Positional argument for log file path
    parser.add_argument('--file', help='Path to the log file to be analysed')
    # Multiple format options: summary, errors, timeline
    parser.add_argument('--format', nargs='+', choices=['summary', 'errors', 'timeline'], help='Types of analysis to perform', default=['summary'])
    # Log level filter - only includes logs at or above this level
    parser.add_argument('--level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Minimum log level to include in the analysis', default='INFO')
    # Date range filter - start date for analysis
    parser.add_argument('--since', help='Start date for log analysis (YYYY-MM-DD)')
    # Output file path for results
    parser.add_argument('--output', '-o', help='Path to save the analysis results', default='analysis_results.txt')
    return parser.parse_args()




def main():
    """
    Main function that orchestrates the log analysis workflow.
    
    Workflow:
    1. Parse command-line arguments
    2. Parse date filter (if provided)
    3. Initialize LogParser and retrieve filtered logs
    4. Apply requested analysis format(s)
    5. Display or save results
    """
    args = parse_arguments()
    
    # Debug output: confirm file being analyzed
    print(f"Analyzing log file: {args.file}")

    # Parse the --since parameter and convert to datetime object
    since_dt = None
    if args.since:
        try:
            since_dt = datetime.strptime(args.since, '%Y-%m-%d')
        except ValueError:
            print("Error: Invalid date format for --since. Use YYYY-MM-DD.")
            exit(1)
    
    # Initialize the log parser and retrieve logs matching criteria
    parser = LogParser(args.file)
    logs = parser.parse_logs(minLevel=args.level, since=since_dt)
    
    # Handle case where no logs match the filter criteria
    if not logs:
        print("No logs found matching the criteria.")
        sys.exit(2)
    
    # Apply summary analysis if requested
    if 'summary' in args.format:
        print("Summary analysis:")
        # Generate formatted summary statistics (count by level)
        formatted_summary = format_summary(logs)
        print(formatted_summary)

    # Apply error analysis if requested
    if 'errors' in args.format:
        print("\nError analysis:")
        # Extract and display ERROR level logs with timestamps
        formatted_errors = format_errors(logs)
        print(formatted_errors)
    # Future enhancement: timeline analysis
    # for log in logs:
    #     print(f"{log['date']} {log['level']} {log['message']}")


if __name__ == "__main__":
    main()