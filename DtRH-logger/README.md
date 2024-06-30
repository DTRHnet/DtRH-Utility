# DtRH-Logger 

## Overview

`dtrhLogger` is a Python logging utility that enhances application observability through advanced logging features, thread safety, and configurable options. It integrates with the `rich` library for pretty console output and supports various logging mechanisms including a separate module for trace.

## Features

- Rich console output with `rich` library
- File-based logging with rotation options
- JSON-formatted logging for web applications
- Thread-safe logging of function calls and execution times
- Configurable logging levels and formats via JSON file
- Summary of log data with function call count and execution time

## Classes and Functionality

### `BaseLogger`
- **Purpose**: Serves as the foundational logging class, providing core functionality.
- **Features**:
  - Supports both console and file logging.
  - Configurable log rotation (size or time-based).
  - Uses `rich` for enhanced console output.

### `SystemLogger`
- **Purpose**: Extends `BaseLogger` for system-specific logging needs.
- **Features**:
  - Inherits all features from `BaseLogger`.
  - Adds the capability to log to system syslog.

### `WebLogger`
- **Purpose**: Specialized for logging in web applications.
- **Features**:
  - Inherits from `BaseLogger`.
  - Offers JSON-formatted logging for structured data output.

### `DevLogger`
- **Purpose**: Tailored for development environments.
- **Features**:
  - Inherits from `BaseLogger`.
  - Provides easy-to-use methods for debug and info-level logging.

### `TraceInfo`
- **Purpose**: Maintains trace data for function calls.
- **Features**:
  - Tracks current function, last executed command, runtime, call count, and execution times.

### `Tracer`
- **Purpose**: Implements tracing of function calls and execution times.
- **Features**:
  - Uses `TraceInfo` to collect and log trace data.
  - Thread-safe implementation to handle concurrent environments.
  - Provides detailed summaries of function calls and execution metrics.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set up logging configuration in `logging_config.json` or via environment variables.
2. Use the logging functions provided in `dtrhLogger.py`.
3. Run your Python script:
   ```bash
   python dtrhLogger.py
   ```

4. View logs in real-time:
   ```bash
   tail -f trace.log
   ```

## Configuration

- `log_level`: The logging level (e.g., DEBUG, INFO)
- `log_file`: File path for logging output
- `rotation`: Type of log rotation ('size' or 'time')
- `interval`: Interval for time-based rotation
- `when`: Time specification for rotation (e.g., 'midnight')
- `max_bytes`: Maximum file size for size-based rotation
- `backup_count`: Number of backup files to keep

## Example

```python
dev_logger.debug("Debugging information")
dev_logger.info("Development log entry")
```
