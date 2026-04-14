# Log Analyser CLI

A command-line application for parsing, filtering, and analyzing log files with support for multiple analysis formats and flexible filtering criteria.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Architecture & Design Patterns](#architecture--design-patterns)
- [Key Concepts & Technologies](#key-concepts--technologies)
- [Current Limitations](#current-limitations)
- [Potential Enhancements](#potential-enhancements)
- [Best Practices & Code Quality](#best-practices--code-quality)

---

## Overview

Log Analyser CLI is a Python utility designed to help developers and system administrators quickly analyze log files. It provides filtering capabilities by severity level and date range, and offers multiple analysis formats for different use cases.

**Use Cases:**
- Identify and analyze error patterns in application logs
- Generate statistical summaries of log entries
- Filter logs by severity level for focused debugging
- Extract logs from specific time periods
- Quick analysis without loading entire files into memory

---

## Features

- ✅ **Multiple Log Levels**: Support for DEBUG, INFO, WARNING, and ERROR levels
- ✅ **Severity-based Filtering**: Show only logs at or above a minimum severity threshold
- ✅ **Date Range Filtering**: Analyze logs from a specific start date onward
- ✅ **Multiple Analysis Formats**: 
  - Summary: Log count statistics by level
  - Errors: Detailed ERROR-level log extraction
  - Timeline: Foundation for chronological analysis (planned)
- ✅ **Memory Efficient**: Uses generator pattern for processing large log files
- ✅ **Flexible Command-Line Interface**: argparse-based with sensible defaults

---

## Installation

### Requirements
- Python 3.6+
- Standard library only (no external dependencies)

### Setup

1. Clone or download the project:
```bash
cd LOG_ANALYSER_CLI
```

2. Verify Python installation:
```bash
python --version
```

3. Run the application:
```bash
python log_analyser.py --help
```

---

## Usage

### Basic Command Structure

```bash
python log_analyser.py --file <log_file> [options]
```

### Command-Line Arguments

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `--file` | - | string | *required* | Path to the log file to analyze |
| `--format` | - | choice | `summary` | Analysis format(s): `summary`, `errors`, `timeline` |
| `--level` | - | choice | `INFO` | Minimum log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `--since` | - | date | none | Start date for filtering (YYYY-MM-DD format) |
| `--output` | `-o` | string | `analysis_results.txt` | Output file path for results |

### Usage Examples

#### Example 1: Basic Summary Analysis
```bash
python log_analyser.py --file application.log
```
Shows count of log entries by severity level (defaults to INFO level and above).

**Output:**
```
Analyzing log file: application.log
Summary analysis:
INFO: 150 entries
WARNING: 23 entries
ERROR: 5 entries
```

#### Example 2: Extract All Error Logs
```bash
python log_analyser.py --file application.log --format errors --level ERROR
```
Displays all ERROR-level logs with timestamps and messages.

**Output:**
```
Analyzing log file: application.log
Error analysis:
Total ERROR entries: 5
2024-01-15 14:30:45 Database connection failed
2024-01-15 14:35:22 Transaction timeout
2024-01-15 15:02:10 Memory allocation error
```

#### Example 3: Analyze Logs Since a Specific Date
```bash
python log_analyser.py --file application.log --since 2024-01-15 --format summary errors
```
Analyzes only logs from January 15, 2024 onward with both summary and error formats.

#### Example 4: DEBUG Level Analysis
```bash
python log_analyser.py --file application.log --level DEBUG --format summary
```
Includes DEBUG level and all higher severity logs in the analysis.

#### Example 5: Save Results to File
```bash
python log_analyser.py --file application.log --format errors --output error_report.txt
```
Analysis results are saved to the specified output file.

### Log File Format

The application expects log files in the following format:

```
YYYY-MM-DD HH:MM:SS LEVEL message
```

**Example:**
```
2024-01-15 08:30:15 DEBUG Service initialization started
2024-01-15 08:30:20 INFO Database connection established
2024-01-15 08:30:45 WARNING Cache miss rate exceeds threshold
2024-01-15 09:15:32 ERROR Failed to process request ID 12345
```

---

## Project Structure

```
LOG_ANALYSER_CLI/
├── log_analyser.py      # Main entry point - CLI orchestration
├── parser.py            # Log parsing and filtering logic
├── formatters.py        # Output formatting functions
├── README.md            # This file - documentation
└── tests/
    └── sample.txt       # Sample log file for testing
```

### Module Responsibilities

| Module | Purpose | Key Classes/Functions |
|--------|---------|----------------------|
| `log_analyser.py` | CLI interface and workflow orchestration | `parse_arguments()`, `main()` |
| `parser.py` | Log file parsing and filtering | `LogParser` class, regex patterns |
| `formatters.py` | Output formatting for different analysis types | `format_summary()`, `format_errors()` |

---

## Architecture & Design Patterns

### 1. **Generator Pattern (Memory Efficiency)**

The `parse_logs()` method uses Python generators with `yield`:

```python
def parse_logs(self, minLevel='INFO', since=None):
    # Yields one log at a time instead of returning a complete list
    yield {
        'date': log_date,
        'level': log_level,
        'message': log_message
    }
```

**Benefits:**
- Processes large files without loading entire file into RAM
- Enables filtering before storing in memory
- Supports streaming analysis

### 2. **Regular Expression Pattern Matching**

Uses compiled regex patterns for robust log line parsing:

```python
LOG_PATTERN = r"(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<level>[A-Z]+) (?P<message>.*)"
```

**Benefits:**
- Named groups for clear extraction
- Handles variations in log formats
- Skips malformed lines gracefully

### 3. **Log Level Hierarchy**

Implements severity-based filtering using a weight dictionary:

```python
LEVEL_WEIGHTS = {
    'DEBUG': 1,
    'INFO': 2,
    'WARN': 3,
    'WARNING': 3,
    'ERROR': 4
}
```

**Benefits:**
- Supports filtering by minimum severity
- Semantically clear hierarchy
- Easy to extend with new levels

### 4. **Command-Line Argument Parsing (argparse)**

Uses Python's standard `argparse` module for robust CLI:

```python
parser = argparse.ArgumentParser(description='Log Analyser')
parser.add_argument('--file', help='Path to the log file')
```

**Benefits:**
- Automatic --help generation
- Type validation
- Clear error messages for invalid arguments

### 5. **Separation of Concerns**

- **Parser**: Handles IO and regex extraction
- **Formatters**: Handles output presentation
- **CLI**: Handles argument orchestration

---

## Key Concepts & Technologies

### Core Concepts

1. **Log Levels (Severity Hierarchy)**
   - Represents message importance and urgency
   - Used for filtering and prioritization
   - Standard levels: DEBUG → INFO → WARNING → ERROR

2. **Regular Expressions (Regex)**
   - Pattern matching for structured data extraction
   - Enables parsing of unstructured log lines
   - Supporting format: `YYYY-MM-DD HH:MM:SS LEVEL message`

3. **Generator Functions**
   - Memory-efficient processing pattern
   - Yields values one at a time
   - Enables lazy evaluation

4. **Date Filtering**
   - `datetime.strptime()` for parsing date strings
   - Comparison operators for range filtering
   - YYYY-MM-DD format requirement

### Technologies Used

- **Python 3.6+**: Core language
- **argparse**: Command-line interface framework
- **re (regex)**: Pattern matching and extraction
- **datetime**: Date/time parsing and comparison
- **collections.Counter**: Efficient frequency counting
- **sys**: System exit codes and standard streams

### Design Principles Applied

1. **DRY (Don't Repeat Yourself)**: Reusable parsing logic
2. **Single Responsibility**: Each module has one clear purpose
3. **Open/Closed Principle**: Easy to add new formatters
4. **KISS (Keep It Simple)**: No unnecessary complexity
5. **Fail Fast**: Early error detection with clear messages

---

## Current Limitations

1. **Single Log Format**
   - Only supports one regex pattern
   - Not configurable for custom formats

2. **In-Memory Log Storage**
   - Current implementation stores parsed logs in memory (line 37 in parser.py)
   - `log_entries` list isn't used but could impact large files
   - Generator approach partially mitigates this

3. **No Wildcard Log Levels**
   - Cannot analyze across multiple non-continuous levels
   - Must specify a minimum level

4. **Limited Output Formats**
   - Only summary and errors implemented
   - Timeline format is declared but not implemented

5. **No Regex Validation**
   - Malformed log lines are silently skipped
   - No logging of parsing failures

6. **Single Output Stream**
   - Results printed to stdout only (--output not yet implemented)
   - No option to redirect to file

7. **No Sorting**
   - Logs returned in file order, no sorting by level or date

8. **Limited Error Recovery**
   - File not found exits with code 1
   - No retry or fallback mechanisms

---

## Potential Enhancements

### High Priority

1. **Implement File Output**
   ```python
   # Write results to --output file instead of stdout
   with open(args.output, 'w') as f:
       f.write(formatted_summary)
   ```

2. **Timeline Analysis Format**
   - Implement chronological visualization
   - Support for aggregation by hour/day
   - Error rate trending

3. **Configurable Log Format**
   - Accept custom regex patterns
   - Support different timestamp formats
   - Handle multi-line log entries

4. **Log Statistics**
   - Average response times
   - Error frequency analysis
   - Peak load analysis

### Medium Priority

5. **Search/Pattern Matching**
   - Filter logs by message content
   - Regex search in log messages
   - Keyword highlighting

6. **Export Formats**
   - JSON export for programmatic processing
   - CSV export for spreadsheet analysis
   - HTML report generation

7. **Performance Optimization**
   - Index frequently searched fields
   - Parallel processing for large files
   - Caching for repeated analyses

8. **Advanced Filtering**
   - Message pattern matching
   - Combined filters (AND/OR logic)
   - Exclude specific patterns

### Low Priority

9. **Interactive CLI Mode**
   - REPL for multiple analyses
   - Live log tailing
   - Autocomplete for arguments

10. **Integration Features**
    - Web API for remote log analysis
    - Webhook notifications for errors
    - Dashboard integration

11. **Database Support**
    - Store parsed logs in SQLite
    - Query via SQL
    - Historical trend analysis

12. **Unit Testing Framework**
    - Test suite for parser functions
    - Mock log files for testing
    - Regression test coverage

---

## Best Practices & Code Quality

### Current Implementation Quality

| Aspect | Status | Notes |
|--------|--------|-------|
| Code Documentation | ✅ Complete | All functions have docstrings |
| Error Handling | ⚠️ Partial | Basic file not found handling |
| Type Hints | ❌ Missing | No type annotations (Python 3.5+ feature) |
| Unit Tests | ❌ Missing | No automated test suite |
| Code Comments | ✅ Complete | Inline comments explain logic |
| Separation of Concerns | ✅ Good | Clear module responsibilities |

### Recommended Best Practices

#### 1. **Add Type Hints** (Python 3.5+)
```python
from typing import Generator, Dict, Optional
from datetime import datetime

def parse_logs(self, minLevel: str = 'INFO', 
               since: Optional[datetime] = None) -> Generator[Dict, None, None]:
    """Parse and filter logs from file."""
    ...
```

#### 2. **Implement Unit Testing**
```python
# tests/test_parser.py
import unittest
from parser import LogParser

class TestLogParser(unittest.TestCase):
    def test_parse_valid_log_line(self):
        """Test parsing of correctly formatted log line."""
        # Arrange
        parser = LogParser('tests/sample.txt')
        # Act
        logs = list(parser.parse_logs(minLevel='DEBUG'))
        # Assert
        self.assertGreater(len(logs), 0)
```

#### 3. **Enhanced Error Handling**
```python
# Better error messages and logging
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    with open(self.log_file, 'r') as f:
        ...
except FileNotFoundError:
    logger.error(f"Log file not found: {self.log_file}")
    sys.exit(1)
except IOError as e:
    logger.error(f"Failed to read log file: {e}")
    sys.exit(2)
```

#### 4. **Remove Dead Code**
```python
# Line 37 in parser.py stores logs but never uses them
# Remove: log_entries.append((log_date, log_level, log_message))
```

#### 5. **Implement Logging Module**
```python
# Replace print() calls with logging
import logging
logging.info(f"Analyzing log file: {args.file}")
logging.error("Invalid date format in --since argument")
```

#### 6. **Add Validation Layer**
```python
def validate_log_level(level: str) -> bool:
    """Validate log level is supported."""
    return level.upper() in LogParser.LEVEL_WEIGHTS

def validate_date_format(date_str: str) -> bool:
    """Validate date string format."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
```

#### 7. **Create Configuration File**
```python
# config.py
LOG_CONFIG = {
    'allowed_levels': ['DEBUG', 'INFO', 'WARNING', 'ERROR'],
    'default_level': 'INFO',
    'date_format': '%Y-%m-%d',
    'timestamp_format': '%Y-%m-%d %H:%M:%S',
    'max_file_size': 1024 * 1024 * 100,  # 100MB
}
```

#### 8. **Performance Considerations**
- Current regex compilation happens on every line
- Optimize by compiling regex once at module level:
```python
LOG_PATTERN_COMPILED = re.compile(LOG_PATTERN)
# Then use in loop: match = LOG_PATTERN_COMPILED.match(line)
```

#### 9. **Document Edge Cases**
- What happens with timestamps in different timezones?
- How are extremely long log messages handled?
- What are limits on file size?

#### 10. **Version Control & Documentation**
- Add version number to module docstring
- Include changelog for tracked improvements
- Document breaking changes in future versions

---

## Example Workflow

### Scenario: Debug Production Error

1. **Identify the problem window:**
   ```bash
   python log_analyser.py --file production.log --since 2024-01-15 \
       --level ERROR --format errors
   ```

2. **Get context with summary:**
   ```bash
   python log_analyser.py --file production.log --since 2024-01-15 \
       --level DEBUG --format summary
   ```

3. **Analyze patterns:**
   - Are errors concentrated in time?
   - What's the ratio of errors to warnings?
   - What was happening before the first error?

---

## Contributing

To extend this project:

1. Add custom formatters in `formatters.py`
2. Enhance regex patterns in `parser.py` for new log formats
3. Add new CLI arguments in `parse_arguments()` function
4. Create comprehensive tests before merging changes

---

## License

This project is provided as-is for educational and professional use.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-14 | Initial release with basic filtering and analysis |

---

## Support & Troubleshooting

### Common Issues

**"Error: Log file not found"**
- Verify the file path is correct
- Check file permissions (read access required)
- Use absolute path if relative path fails

**"No logs found matching the criteria"**
- Check your --level filter isn't too restrictive
- Verify --since date is before log entries
- Inspect a sample of the log file format

**"Invalid date format for --since"**
- Use YYYY-MM-DD format only
- Example: `--since 2024-01-15`

**Analysis seems incomplete**
- Verify log file format matches expected pattern
- Check for multi-line log entries (not currently supported)

---

## Roadmap

- [ ] Implement timeline analysis format
- [ ] Add JSON/CSV export options
- [ ] Create interactive CLI mode
- [ ] Add comprehensive unit test suite
- [ ] Implement custom regex pattern support
- [ ] Create web API wrapper
- [ ] Add performance metrics (processing time, memory usage)
- [ ] Support for multiple simultaneous files
