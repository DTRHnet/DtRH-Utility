import logging
import json
import yaml
import os
import datetime
import xml.etree.ElementTree as ET
from rich.console import Console

class BasicLogger:
    handlers_registry = {}
    default_config_file = 'dtrhLogger.yaml'
    default_config = {
        "level": "INFO",
        "output_file": None,
        "rich_output": False,
        "enable_logger": True,
        "terminal_output": True,  # Default to true if not specified
        "handlers": []
    }

    def __init__(self, name, config_file=None, output_file=None, rich_output=False):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.config_file = config_file or self.default_config_file
        self.config = self.load_config(self.config_file)
        
        # Override config with explicit parameters if provided
        if output_file:
            self.config['output_file'] = output_file
        self.config['rich_output'] = rich_output

        self.console = Console() if self.config.get('rich_output', False) else None
        if self.config.get('enable_logger', True):
            self.setup_handlers()

    def load_config(self, config_file):
        if not os.path.exists(config_file):
            self.create_default_config(config_file)
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

    def create_default_config(self, config_file):
        with open(config_file, 'w') as file:
            yaml.dump(self.default_config, file)
        print(f"Default configuration file created at {config_file}")

    def setup_handlers(self):
        if self.config.get('output_file'):
            log_directory = self.create_log_directory()
            output_file = self.config['output_file']
            if not os.path.isabs(output_file):
                output_file = os.path.join(log_directory, output_file)
            self.ensure_log_file(output_file)
            file_handler = logging.FileHandler(output_file, mode='a')
            file_handler.setFormatter(CustomFormatter())
            self.logger.addHandler(file_handler)

        if self.config.get('terminal_output', True):
            if self.console:
                from rich.logging import RichHandler
                rich_handler = RichHandler(console=self.console)
                self.logger.addHandler(rich_handler)
            else:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(CustomFormatter())
                self.logger.addHandler(console_handler)

        for handler_class in self.config.get('handlers', []):
            handler = self.handlers_registry.get(handler_class)
            if handler:
                self.logger.addHandler(handler())

    def create_log_directory(self):
        sub_directory = 'log'
        date_directory = datetime.datetime.now().strftime('%Y-%m-%d')
        os.makedirs(sub_directory, exist_ok=True)
        if not os.path.exists(f"{sub_directory}/{date_directory}"):
            os.makedirs(f"{sub_directory}/{date_directory}")
        #log_directory = f"{sub_directory}/{date_directory}"
        return sub_directory

    def ensure_log_file(self, file_path):
        # Ensure the log file exists by creating it if it does not exist
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write('')

    @classmethod
    def register_handler(cls, handler_class):
        def wrapper(handler):
            cls.handlers_registry[handler_class] = handler
            return handler
        return wrapper

    def log(self, level, msg):
        if not self.config.get('enable_logger', True):
            return
        if self.console and self.config.get('terminal_output', True):
            self.console.log(f"[{logging.getLevelName(level)}] {msg}")
        else:
            self.logger.log(level, msg)

    def debug(self, msg):
        self.log(logging.DEBUG, msg)

    def info(self, msg):
        self.log(logging.INFO, msg)

    def warn(self, msg):
        self.log(logging.WARNING, msg)

    def error(self, msg):
        self.log(logging.ERROR, msg)

    def critical(self, msg):
        self.log(logging.CRITICAL, msg)


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Add 4 line breaks and timestamp at the beginning of each log entry
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record.msg = f"\n\n\n\n[{timestamp}] {record.msg}"
        return super().format(record)


@BasicLogger.register_handler('xml')
class XMLLogger(BasicLogger):
    def log(self, level, msg):
        if not self.config.get('enable_logger', True):
            return
        log_entry = ET.Element("Log")
        ET.SubElement(log_entry, "Level").text = logging.getLevelName(level)
        ET.SubElement(log_entry, "Message").text = msg
        xml_string = ET.tostring(log_entry, encoding='unicode')
        super().log(level, xml_string)

@BasicLogger.register_handler('json')
class JSONLogger(BasicLogger):
    def log(self, level, msg):
        if not self.config.get('enable_logger', True):
            return
        log_entry = json.dumps({"level": logging.getLevelName(level), "message": msg})
        super().log(level, log_entry)

# Usage Example
if __name__ == "__main__":
    logger = BasicLogger('example_logger', output_file='example.log', rich_output=True)
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    logger.debug("This is a debug message.")
