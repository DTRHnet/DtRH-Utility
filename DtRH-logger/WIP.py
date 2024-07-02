import logging
import logging.handlers
from rich.logging import RichHandler
import sys
import time
import threading
import json
import os
import yaml
import xml.etree.ElementTree as ET

# Formatter to handle multiple log formats: JSON, YAML, XML
class MultiFormatFormatter(logging.Formatter):
    def __init__(self, log_format='json'):
        super().__init__()
        self.log_format = log_format

    def format(self, record):
        if self.log_format == 'json':
            return self.format_json(record)
        elif self.log_format == 'yaml':
            return self.format_yaml(record)
        elif self.log_format == 'xml':
            return self.format_xml(record)
        else:
            return super().format(record)

    def format_json(self, record):
        log_record = record.__dict__.copy()
        return json.dumps(log_record)

    def format_yaml(self, record):
        log_record = record.__dict__.copy()
        return yaml.dump(log_record)

    def format_xml(self, record):
        log_record = record.__dict__.copy()
        log_element = ET.Element('log')
        for key, value in log_record.items():
            child = ET.SubElement(log_element, key)
            child.text = str(value)
        return ET.tostring(log_element, encoding='unicode')

# Custom filter to filter logs based on level or message content
class LogFilter(logging.Filter):
    def __init__(self, level=None, contains=None):
        self.level = level
        self.contains = contains

    def filter(self, record):
        if self.level and record.levelno != self.level:
            return False
        if self.contains and self.contains not in record.msg:
            return False
        return True

# Custom handler for additional log handling logic
class CustomHandler(logging.Handler):
    def emit(self, record):
        try:
            log_entry = self.format(record)
            # Custom logic to handle log entries, e.g., send to a remote server
            print(f"CustomHandler: {log_entry}")
        except Exception as e:
            self.handleError(record)

# Base Logger class with configuration options and multiple format support
class BaseLogger:
    def __init__(self, name, log_file='app.log', log_level=logging.DEBUG, rotation='size', interval=1, when='midnight', max_bytes=10*1024*1024, backup_count=5, log_format='json'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Console Handler with Rich
        self.console_handler = RichHandler()
        self.console_handler.setLevel(log_level)
        self.console_handler.setFormatter(MultiFormatFormatter(log_format=log_format))

        # File handler based on rotation type
        if rotation == 'size':
            self.file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
        elif rotation == 'time':
            self.file_handler = logging.handlers.TimedRotatingFileHandler(
                log_file, when=when, interval=interval, backupCount=backup_count
            )
        self.file_handler.setFormatter(MultiFormatFormatter(log_format=log_format))

        # Adding handlers to logger
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)

    def log(self, level, message, **kwargs):
        self.logger.log(level, message, extra=kwargs)

# System Logger class with Syslog handler support
class SystemLogger(BaseLogger):
    def __init__(self, name, log_file='system.log', log_level=logging.DEBUG, **kwargs):
        super().__init__(name, log_file, log_level, **kwargs)

    def add_syslog_handler(self, address='/dev/log', level=logging.WARNING):
        syslog_handler = logging.handlers.SysLogHandler(address=address)
        syslog_handler.setLevel(level)
        self.logger.addHandler(syslog_handler)

# Web Logger class with JSON logging capability
class WebLogger(BaseLogger):
    def __init__(self, name, log_file='web.log', log_level=logging.DEBUG, **kwargs):
        super().__init__(name, log_file, log_level, **kwargs)

    def set_json_logging(self, enabled=True):
        if enabled:
            json_handler = logging.StreamHandler()
            json_handler.setLevel(logging.DEBUG)
            json_formatter = logging.Formatter(
                '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
            )
            json_handler.setFormatter(json_formatter)
            self.logger.addHandler(json_handler)

# Development Logger class with convenience methods for debugging
class DevLogger(BaseLogger):
    def __init__(self, name, log_file='dev.log', log_level=logging.DEBUG, **kwargs):
        super().__init__(name, log_file, log_level, **kwargs)

    def debug(self, message, **kwargs):
        self.log(logging.DEBUG, message, **kwargs)

    def info(self, message, **kwargs):
        self.log(logging.INFO, message, **kwargs)

# Class to store trace information for function calls
class TraceInfo:
    def __init__(self):
        self.current_function = None
        self.last_command = None
        self.runtime = 0
        self.call_count = 0
        self.execution_times = []

# Tracer class for tracing function calls and logging them
class Tracer:
    def __init__(self):
        self.trace_info = TraceInfo()
        self.logger = DevLogger('Tracer', log_file='trace.log')
        self.start_time = None
        self.lock = threading.Lock()

    def trace_calls(self, frame, event, arg):
        if event == 'call':
            with self.lock:
                self.trace_info.current_function = frame.f_code.co_name
                self.trace_info.call_count += 1
                self.start_time = time.time()
                self.logger.debug(f"Function {frame.f_code.co_name} called.")
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        with self.lock:
            if event == 'line':
                self.trace_info.last_command = frame.f_lineno
                self.trace_info.runtime = time.time() - self.start_time
            elif event == 'return':
                exec_time = time.time() - self.start_time
                self.trace_info.execution_times.append(exec_time)
                self.logger.info(f"Function {frame.f_code.co_name} returned, execution time: {exec_time:.4f} seconds.")
        return self.trace_lines

    def start_tracing(self):
        sys.settrace(self.trace_calls)

    def stop_tracing(self):
        sys.settrace(None)

    def get_trace_info(self):
        with self.lock:
            return self.trace_info

    def log_summary(self):
        with self.lock:
            summary = {
                "current_function": self.trace_info.current_function,
                "last_command": self.trace_info.last_command,
                "runtime": self.trace_info.runtime,
                "call_count": self.trace_info.call_count,
                "average_execution_time": sum(self.trace_info.execution_times) / len(self.trace_info.execution_times) if self.trace_info.execution_times else 0,
                "total_execution_time": sum(self.trace_info.execution_times)
            }
            for key, value in summary.items():
                self.logger.info(f"{key}: {value}")

    def reset_tracing(self):
        with self.lock:
            self.trace_info = TraceInfo()

# Decorator to trace a target function
def trace_process(target_function):
    tracer = Tracer()

    def wrapper(*args, **kwargs):
        tracer.start_tracing()
        result = target_function(*args, **kwargs)
        tracer.stop_tracing()
        tracer.log_summary()
        return result

    return wrapper

@trace_process
def example_function():
    print("Example function started")
    time.sleep(1)
    print("Example function ended")

# Loads logging configuration from a file or environment variables
def load_config():
    config_file = os.getenv('LOGGING_CONFIG_FILE', 'logging_config.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

# Main function to set up logging and run examples
def main():
    config = load_config()

    log_level = config.get('log_level', logging.DEBUG)
    log_file = config.get('log_file', 'app.log')
    rotation = config.get('rotation', 'size')
    interval = config.get('interval', 1)
    when = config.get('when', 'midnight')
    max_bytes = config.get('max_bytes', 10*1024*1024)
    backup_count = config.get('backup_count', 5)
    log_format = config.get('log_format', 'json')

    dev_logger = DevLogger(
        'Dev', log_file=log_file, log_level=log_level, rotation=rotation,
        interval=interval, when=when, max_bytes=max_bytes, backup_count=backup_count, log_format=log_format
    )

    # Example usage with additional logging capabilities
    dev_logger.debug("Debugging information")
    dev_logger.info("Development log entry")

    # Running the example function
    example_function()

if __name__ == "__main__":
    main()
