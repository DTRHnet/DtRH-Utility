import json
import sys
from jsonschema import validate, ValidationError
from dtrhLogger import DevLogger

class pJSON:
    def __init__(self):
        self.data = None
        self.logger = DevLogger()

    def read_from_file(self, file_path):
        """Read JSON data from a file."""
        try:
            with open(file_path, 'r') as file:
                self.data = json.load(file)
            self.logger.log("INFO", f"Successfully read JSON from file: {file_path}")
            return self.data
        except FileNotFoundError:
            self.logger.log("ERROR", "File not found.")
        except json.JSONDecodeError as e:
            self.logger.log("ERROR", f"Error decoding JSON: {e}")
        except Exception as e:
            self.logger.log("ERROR", f"An error occurred: {e}")

    def read_from_stdin(self):
        """Read JSON data from standard input."""
        try:
            input_data = self.to_json_string(sys.stdin.read())
            self.data = json.loads(input_data)
            self.logger.log("INFO", "Successfully read JSON from stdin")
            return self.data
        except json.JSONDecodeError as e:
            self.logger.log("ERROR", f"Error decoding JSON: {e}")
        except Exception as e:
            self.logger.log("ERROR", f"An error occurred: {e}")

    def to_json_string(self):
        """Convert the data to a JSON string."""
        if self.data is not None:
            try:
                return json.dumps(self.data, indent=4)
            except Exception as e:
                self.logger.log("ERROR", f"An error occurred: {e}")
        else:
            self.logger.log("WARNING", "No data to convert.")

    def to_dict(self):
        """Return the data as a dictionary."""
        if self.data is not None:
            return self.data
        else:
            self.logger.log("WARNING", "No data available.")

    def to_pretty_string(self):
        """Return a pretty-printed JSON string."""
        if self.data is not None:
            try:
                return json.dumps(self.data, indent=4, sort_keys=True)
            except Exception as e:
                self.logger.log("ERROR", f"An error occurred: {e}")
        else:
            self.logger.log("WARNING", "No data to print.")

    def validate_json(self, schema):
        """Validate JSON data against a provided schema."""
        if self.data is not None:
            try:
                validate(instance=self.data, schema=schema)
                self.logger.log("INFO", "JSON is valid.")
            except ValidationError as e:
                self.logger.log("ERROR", f"JSON validation error: {e}")
            except Exception as e:
                self.logger.log("ERROR", f"An error occurred: {e}")
        else:
            self.logger.log("WARNING", "No data to validate.")
