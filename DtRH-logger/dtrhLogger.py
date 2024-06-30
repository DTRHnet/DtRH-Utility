#
#    /$$$$$$$    /$$     /$$$$$$$  /$$   /$$         /$$   /$$   /$$     /$$ /$$ /$$   /$$              
#   | $$__  $$  | $$    | $$__  $$| $$  | $$        | $$  | $$  | $$    |__/| $$|__/  | $$              
#   | $$  \ $$ /$$$$$$  | $$  \ $$| $$  | $$        | $$  | $$ /$$$$$$   /$$| $$ /$$ /$$$$$$   /$$   /$$
#   | $$  | $$|_  $$_/  | $$$$$$$/| $$$$$$$$ /$$$$$$| $$  | $$|_  $$_/  | $$| $$| $$|_  $$_/  | $$  | $$
#   | $$  | $$  | $$    | $$__  $$| $$__  $$|______/| $$  | $$  | $$    | $$| $$| $$  | $$    | $$  | $$
#   | $$  | $$  | $$ /$$| $$  \ $$| $$  | $$        | $$  | $$  | $$ /$$| $$| $$| $$  | $$ /$$| $$  | $$
#   | $$$$$$$/  |  $$$$/| $$  | $$| $$  | $$        |  $$$$$$/  |  $$$$/| $$| $$| $$  |  $$$$/|  $$$$$$$
#   |_______/    \___/  |__/  |__/|__/  |__/         \______/    \___/  |__/|__/|__/   \___/   \____  $$
#                                                                                              /$$  | $$
#   DtRH-Logger - v0.0.1                                                                         |  $$$$$$/
#   July 1, 2024                                                                              \______/ 
#                                                                                                       
#                                                                                < admin [at] dtrh.net >
# ======================================================================================================

import logging
import logging.handlers
from rich.logging import RichHandler
import sys
import time
import threading
import json
import os

# ======================
# BaseLogger.__init__()
# Initializes the base logger with configuration options
# ==============================================
class BaseLogger:
    def __init__(self, name, log_file='app.log', log_level=logging.DEBUG, rotation='size', interval=1, when='midnight', max_bytes=10*1024*1024, backup_count=5):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Console Handler with Rich
        self.console_handler = RichHandler()
        self.console_handler.setLevel(log_level)

        # File handler based on rotation type
        if rotation == 'size':
            self.file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
        elif rotation == 'time':
            self.file_handler = logging.handlers.TimedRotatingFileHandler(
                log_file, when=when, interval=interval, backupCount=backup_count
            )

        # Formatter for log messages
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.file_handler.setFormatter(formatter)

        # Adding handlers to logger
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)

    # ======================
    # BaseLogger.log()
    # Logs a message with a specified log level
    # ==============================================
    def log(self, level, message, **kwargs):
        self.logger.log(level, message, extra=kwargs)

# ======================
# SystemLogger.__init__()
# Initializes the system logger with specific settings
# ==============================================
class SystemLogger(BaseLogger):
    def __init__(self, name, log_file='system.log', log_level=logging.DEBUG, **kwargs):
        super().__init__(name, log_file, log_level, **kwargs)

    # ======================
    # SystemLogger.add_syslog_handler()
    # Adds a syslog handler for system logging
    # ==============================================
    def add_syslog_handler(self, address='/dev/log', level=logging.WARNING):
        syslog_handler = logging.handlers.SysLogHandler(address=address)
        syslog_handler.setLevel(level)
        self.logger.addHandler(syslog_handler)

# ======================
# WebLogger.__init__()
# Initializes the web logger with JSON logging capabilities
# ==============================================
class WebLogger(BaseLogger):
    def __init__(self, name, log_file='web.log', log_level=logging.DEBUG, **kwargs):
        super().__init__(name, log_file, log_level, **kwargs)

    # ======================
    # WebLogger.set_json_logging()
    # Enables or disables JSON formatted logging
    # ==============================================
    def set_json_logging(self, enabled=True):
        if enabled:
            json_handler = logging.StreamHandler()
            json_handler.setLevel(logging.DEBUG)
            json_formatter = logging.Formatter(
                '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
            )
            json_handler.setFormatter(json_formatter)
            self.logger.addHandler(json_handler)

# ======================
# DevLogger.__init__()
# Initializes the development logger with enhanced logging settings
# ==============================================
class DevLogger(BaseLogger):
    def __init__(self, name, log_file='dev.log', log_level=logging.DEBUG, **kwargs):
        super().__init__(name, log_file, log_level, **kwargs)

    # ======================
    # DevLogger.debug()
    # Logs a debug-level message
    # ==============================================
    def debug(self, message, **kwargs):
        self.log(logging.DEBUG, message, **kwargs)

    # ======================
    # DevLogger.info()
    # Logs an info-level message
    # ==============================================
    def info(self, message, **kwargs):
        self.log(logging.INFO, message, **kwargs)

# ======================
# TraceInfo.__init__()
# Initializes trace information for function calls
# ==============================================
class TraceInfo:
    def __init__(self):
        self.current_function = None
        self.last_command = None
        self.runtime = 0
        self.call_count = 0
        self.execution_times = []

# ======================
# Tracer.__init__()
# Initializes the tracer with logging and threading capabilities
# ==============================================
class Tracer:
    def __init__(self):
        self.trace_info = TraceInfo()
        self.logger = DevLogger('Tracer', log_file='trace.log')
        self.start_time = None
        self.lock = threading.Lock()

    # ======================
    # Tracer.trace_calls()
    # Traces function calls and logs them
    # ==============================================
    def trace_calls(self, frame, event, arg):
        if event == 'call':
            with self.lock:
                self.trace_info.current_function = frame.f_code.co_name
                self.trace_info.call_count += 1
                self.start_time = time.time()
                self.logger.debug(f"Function {frame.f_code.co_name} called.")
        return self.trace_lines

    # ======================
    # Tracer.trace_lines()
    # Traces line executions and returns from functions
    # ==============================================
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

    # ======================
    # Tracer.start_tracing()
    # Starts the tracing process
    # ==============================================
    def start_tracing(self):
        sys.settrace(self.trace_calls)

    # ======================
    # Tracer.stop_tracing()
    # Stops the tracing process
    # ==============================================
    def stop_tracing(self):
        sys.settrace(None)

    # ======================
    # Tracer.get_trace_info()
    # Retrieves the current trace information
    # ==============================================
    def get_trace_info(self):
        with self.lock:
            return self.trace_info

    # ======================
    # Tracer.log_summary()
    # Logs a summary of the trace information
    # ==============================================
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

    # ======================
    # Tracer.reset_tracing()
    # Resets the trace information
    # ==============================================
    def reset_tracing(self):
        with self.lock:
            self.trace_info = TraceInfo()

# ======================
# trace_process()
# Decorator to trace a target function
# ==============================================
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

# ======================
# load_config()
# Loads logging configuration from a file or environment variables
# ==============================================
def load_config():
    config_file = os.getenv('LOGGING_CONFIG_FILE', 'logging_config.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

# ======================
# main()
# Main function to set up logging and run examples
# ==============================================
def main():
    config = load_config()

    log_level = config.get('log_level', logging.DEBUG)
    log_file = config.get('log_file', 'app.log')
    rotation = config.get('rotation', 'size')
    interval = config.get('interval', 1)
    when = config.get('when', 'midnight')
    max_bytes = config.get('max_bytes', 10*1024*1024)
    backup_count = config.get('backup_count', 5)

    dev_logger = DevLogger(
        'Dev', log_file=log_file, log_level=log_level, rotation=rotation,
        interval=interval, when=when, max_bytes=max_bytes, backup_count=backup_count
    )

    # Example usage with additional logging capabilities
    dev_logger.debug("Debugging information")
    dev_logger.info("Development log entry")

    # Running the example function
    example_function()

if __name__ == "__main__":
    main()

# Instructions:
# To watch the output from a separate terminal, run:
# tail -f trace.log
