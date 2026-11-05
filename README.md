# Log Analyzer CLI

A Python CLI tool for analyzing log files and generating structured reports.

## Features

- Parse log entries and timestamps
- Detect log levels automatically
- Support DEBUG, INFO, WARN, ERROR, and CRITICAL levels
- Normalize WARNING and FATAL log levels
- Count and summarize log entries
- Identify the most frequent errors
- Generate human-readable reports
- Export reports in JSON format
- Save reports to output files
- Handle missing files and invalid input
- Automated tests with pytest

## Project Structure

log-analyzer-cli/
│
├── src/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── parser.py
│   └── cli.py
│
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_parser.py
│   └── test_cli.py
│
├── examples/
│   └── sample.log
│
├── .gitignore
├── LICENSE
└── README.md

## Requirements

- Python 3.10 or newer

No external dependencies are required to run the application.

## Usage

Clone the repository:

    git clone https://github.com/zekolardev/log-analyzer-cli.git

Navigate to the project directory:

    cd log-analyzer-cli

### Basic Analysis

    python -m src.cli examples/sample.log

### JSON Output

    python -m src.cli examples/sample.log --json

### Save Report to a File

    python -m src.cli examples/sample.log --output report.txt

### Save JSON Report

    python -m src.cli examples/sample.log --json --output report.json

### Display Help

    python -m src.cli --help

## Example Output

    =============================================
    LOG ANALYZER REPORT
    =============================================
    Total entries : 10
    Errors        : 2
    Critical      : 1
    Warnings      : 2

    LOG LEVELS
    ---------------------------------------------
    CRITICAL        1
    ERROR           2
    INFO            5
    WARN            2

    TOP ERRORS
    ---------------------------------------------
    [2] Database connection failed
    [1] Payment service unavailable
    =============================================

## Running Tests

Install pytest:

    python -m pip install pytest

Run the test suite:

    python -m pytest -v

## License

This project is licensed under the MIT License.

## Author

**zekolardev**

GitHub: https://github.com/zekolardev