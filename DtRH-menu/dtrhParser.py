import json
import sys
import logging
from jsonschema import validate, ValidationError

# Assuming dtrhMenu.py sets up the logger and we can import it here
logger = logging.getLogger('MainLogger')

class pJSON:
    def __init__(self):
        self.data = None

    def read_from_file(self, file_path):
        """Read JSON data from a file."""
        try:
            with open(file_path, 'r') as file:
                self.data = json.load(file)
            logger.info(f"Successfully read JSON from file: {file_path}")
            return self.data
        except FileNotFoundError:
            logger.error("File not found.")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    def read_from_stdin(self):
        """Read JSON data from standard input."""
        try:
            input_data = sys.stdin.read()
            self.data = json.loads(input_data)
            logger.info("Successfully read JSON from stdin")
            return self.data
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    def to_json_string(self):
        """Convert the data to a JSON string."""
        if self.data is not None:
            try:
                return json.dumps(self.data, indent=4)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
        else:
            logger.warning("No data to convert.")

    def to_dict(self):
        """Return the data as a dictionary."""
        if self.data is not None:
            return self.data
        else:
            logger.warning("No data available.")

    def to_pretty_string(self):
        """Return a pretty-printed JSON string."""
        if self.data is not None:
            try:
                return json.dumps(self.data, indent=4, sort_keys=True)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
        else:
            logger.warning("No data to print.")

    def validate_json(self, schema):
        """Validate JSON data against a provided schema."""
        if self.data is not None:
            try:
                validate(instance=self.data, schema=schema)
                logger.info("JSON is valid.")
            except ValidationError as e:
                logger.error(f"JSON validation error: {e}")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
        else:
            logger.warning("No data to validate.")
