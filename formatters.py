"""
Log Formatters Module

This module provides output formatting functions for different types of log analysis.
Each formatter takes a list of log entries and returns formatted strings for display.

Formatters:
- format_summary: Provides count statistics by log level
- format_errors: Extracts and displays ERROR-level logs with timestamps

Author: Log Analyser Team
Date: 2026
"""

from collections import Counter


def format_summary(logs):
    """
    Generate a summary of log statistics by severity level.
    
    Creates a count of log entries grouped by their severity level (DEBUG, INFO, WARNING, ERROR).
    Uses the Counter class for efficient frequency counting.
    
    Args:
        logs (list or generator): Iterable of log dictionaries containing 'level' key
    
    Returns:
        str: Formatted summary with count of entries per log level
             Example output:
             INFO: 45 entries
             WARNING: 12 entries
             ERROR: 3 entries
    """
    # Count occurrences of each log level
    counts = Counter(log['level'] for log in logs)
    # Format as human-readable summary
    return "\n".join(f"{level}: {count} entries" for level, count in counts.items())

def format_errors(logs):
    """
    Extract and format ERROR-level log entries with timestamps.
    
    Filters logs to show only ERROR severity and displays them in a readable format
    with timestamp and message details.
    
    Args:
        logs (list or generator): Iterable of log dictionaries containing 'level', 'date', and 'message' keys
    
    Returns:
        str: Formatted error report showing total count and individual error details
             Example output:
             Total ERROR entries: 5
             2024-01-15 14:30:45 Database connection failed
             2024-01-15 14:35:22 Transaction timeout
    """
    # Filter logs to include only ERROR level entries
    error_logs = [log for log in logs if log['level'] == 'ERROR']
    
    # Format output: total count + individual errors with timestamps
    return f"Total ERROR entries: {len(error_logs)}\n" + "\n".join(f"{log['date']} {log['message']}" for log in error_logs)