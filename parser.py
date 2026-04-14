"""
Log Parser Module

This module provides the LogParser class for parsing and filtering log files.
It uses regular expressions to extract structured data from unstructured log lines
and supports filtering by log level and date range.

Key Concepts:
- Regex Pattern Matching: Extracts date, level, and message from each line
- Log Level Hierarchy: DEBUG < INFO < WARNING < ERROR
- Generator Pattern: Uses yield for memory-efficient processing of large files
- Date-based Filtering: Supports filtering logs by start date

Author: Log Analyser Team
Date: 2026
"""

from datetime import datetime
import re


# Regular expression pattern for log lines
# Expected format: YYYY-MM-DD HH:MM:SS LEVEL message
# Example: 2024-01-15 14:30:45 ERROR Database connection failed
LOG_PATTERN = r"(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<level>[A-Z]+) (?P<message>.*)"

class LogParser:
    """
    Parser for structured log files with filtering capabilities.
    
    Filters logs by:
    - Minimum log level (DEBUG, INFO, WARNING, ERROR)
    - Date range (logs since a specific date)
    """
    
    # Severity hierarchy - higher numbers = higher severity
    # Used to filter logs by minimum level
    # Note: WARN and WARNING are both supported for compatibility
    LEVEL_WEIGHTS = {
        'DEBUG': 1,
        'INFO': 2,
        'WARN': 3,
        'WARNING': 3,
        'ERROR': 4
    }

    def __init__(self, log_file):
        """
        Initialize the LogParser with a log file path.
        
        Args:
            log_file (str): Path to the log file to parse
        """
        self.log_file = log_file

    def parse_logs(self, minLevel='INFO', since=None):
        """
        Parse and filter logs from the log file using regex pattern matching.
        
        Uses a generator pattern to yield logs one at a time, allowing memory-efficient
        processing of large log files without loading entire file into memory.
        
        Args:
            minLevel (str): Minimum log severity level to include. Defaults to 'INFO'.
                           Valid values: 'DEBUG', 'INFO', 'WARNING', 'ERROR'
            since (datetime): Filter logs to only include entries from this date onward.
                             If None, no date filtering is applied.
        
        Yields:
            dict: Dictionary containing:
                - 'date' (datetime): Parsed log timestamp
                - 'level' (str): Log severity level
                - 'message' (str): Log message content
        
        Raises:
            SystemExit: If log file not found (error code 1)
        
        Note:
            - Skips malformed lines that don't match LOG_PATTERN
            - Uses regex groups for safe extraction
            - Implements two-tier filtering: date range, then severity level
        """
        log_entries = []
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    # Attempt to parse the log line using regex pattern
                    match = re.match(LOG_PATTERN, line)
                    if not match:
                        # Skip lines that don't match expected format
                        continue
                    
                    # Extract and parse the date component
                    log_date = datetime.strptime(match.group('date'), '%Y-%m-%d %H:%M:%S')
                    
                    # Apply date filtering - skip logs before 'since' date if specified
                    if since and log_date < since:
                        continue
                    
                    # Extract log level and normalize to uppercase
                    log_level = match.group('level').upper()
                    
                    # Extract log message
                    log_message = match.group('message')
                    
                    # Apply severity level filtering
                    # Compare weights: skip if log level is below minimum threshold
                    if self.LEVEL_WEIGHTS.get(log_level, 0) < self.LEVEL_WEIGHTS.get(minLevel, 0):
                        continue
                    
                    log_entries.append((log_date, log_level, log_message))

                    # Yield filtered log as dictionary for processing
                    yield {
                        'date': log_date,
                        'level': log_level,
                        'message': log_message
                    }
        except FileNotFoundError:
            print(f"Error: Log file '{self.log_file}' not found.")
            exit(1)
        

        
    