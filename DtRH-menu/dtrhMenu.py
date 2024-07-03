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
#   DtRH-Menu - 0.0.2                                                                         |  $$$$$$/
#   June 29, 2024                                                                              \______/ 
#                                                                                                       
#                                                                                < admin [at] dtrh.net >
# ======================================================================================================


import sys           # System-specific parameters and functions
import threading     # Multi-threading
import json          # JSON parsing and manipulation
import curses
from queue import Queue             # Thread-safe queue implementation
from dtrhStyle import ThemeManager  # Custom theme management for the menu
from dtrhLogger import BasicLogger  # Custom logging for the application
from dtrhParser import pJSON        # Custom JSON parsing
from schemap import *  # JSON schemas for STDIN
import os
import datetime

def setup_logger():
    #calling_file = os.path.basename(sys.argv[0])
    base_name = 'dtrhMenu' #os.path.splitext(calling_file)[0]
    log_filename = f"{base_name}-{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
    log_directory = datetime.datetime.now().strftime('%Y-%m-%d')
    os.makedirs(log_directory, exist_ok=True)
    log_filepath = os.path.join(log_directory, log_filename)
    logger = BasicLogger('MainLogger', output_file=log_filepath, rich_output=False)
    return logger

logger = setup_logger()

class Menu:
    def __init__(self, config):
        self.logger = logger
        self.logger.debug(f"Entering __init__ - Arguments passed: config={config}")
        self.config = config  # Configuration data for the menu
        self.current_menu = 'main'
        self.menus = {'main': config}
        self.theme = None  # Theme manager (initialized later)
        self.language = config.get('language', 'en')  # Language setting
        self.selected_index = 0  # Index of the currently selected menu item
        self.history = []  # History of menu navigation for back functionality
        self.data_changed = True  # Flag to indicate if data has changed and needs refreshing

        # Setup submenus if provided in configuration
        if 'submenus' in config:
            for submenu_key, submenu_config in config['submenus'].items():
                self.menus[submenu_key] = submenu_config

        self.logger.debug("Exiting __init__")

    def get_menu_title(self):
        self.logger.debug("Entering get_menu_title")
        menu = self.menus[self.current_menu]  # Access current menu data
        title = self.config.get('menu_title', 'Menu')  # Default to 'Menu' if no title provided
        self.logger.debug(f"Exiting get_menu_title - Return: {title}")
        return title

    def get_menu_items(self):
        self.logger.debug("Entering get_menu_items")
        menu = self.menus[self.current_menu]  # Access current menu data
        items = menu['menu_items']  # Retrieve menu items
        self.logger.debug(f"Exiting get_menu_items - Return: {items}")
        return items

    def display(self, stdscr):
        self.logger.debug("Entering display")
        if not self.theme:
            # Initialize theme if not already set
            default_theme = {
                "highlight_color": "cyan",
                "normal_color": "white"
            }
            self.theme = ThemeManager(self.config.get('theme', default_theme))
        curses.curs_set(0)  # Hide the cursor in the terminal

        if self.data_changed:
            stdscr.clear()  # Clear the screen for fresh rendering
            h, w = stdscr.getmaxyx()  # Get terminal dimensions
            title = self.get_menu_title()  # Get the menu title
            x = w // 2 - len(title) // 2  # Calculate center position for title
            y = h // 2 - len(self.get_menu_items()) // 2 - 1  # Calculate start position for items
            stdscr.addstr(y, x, title, curses.A_BOLD)  # Display title

            # Iterate through menu items and display them
            for idx, item in enumerate(self.get_menu_items()):
                label = item['label']  # Menu item label
                x = w // 2 - len(label) // 2  # Center align label
                y = h // 2 - len(self.get_menu_items()) // 2 + idx + 1  # Position items vertically
                if idx == self.selected_index:
                    # Highlight the selected item
                    stdscr.attron(self.theme.get_color('highlight_color'))
                    stdscr.addstr(y, x, label)
                    stdscr.attroff(self.theme.get_color('highlight_color'))
                else:
                    stdscr.addstr(y, x, label)

            stdscr.refresh()  # Refresh the screen to display changes
            self.data_changed = False  # Reset change flag
        self.logger.debug("Exiting display")

    def run(self, stdscr):
        self.logger.debug("Entering run")
        while True:
            self.display(stdscr)  # Display the menu
            key = stdscr.getch()  # Wait for user input

            # Handle navigation and interactions
            if key == curses.KEY_UP and self.selected_index > 0:
                self.selected_index -= 1  # Move selection up
                self.data_changed = True  # Mark data as changed
            elif key == curses.KEY_DOWN and self.selected_index < len(self.get_menu_items()) - 1:
                self.selected_index += 1  # Move selection down
                self.data_changed = True  # Mark data as changed
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.execute_action(self.get_menu_items()[self.selected_index]['action'], stdscr)  # Execute action
        self.logger.debug("Exiting run")

    def execute_action(self, action, stdscr):
        self.logger.debug(f"Entering execute_action - Arguments passed: action={action}")
        item = self.get_menu_items()[self.selected_index]  # Get the selected item
        if action == "start_game":
            self.logger.info("Starting game...")
        elif action == "exit":
            self.logger.info("Exiting...")
            sys.exit(0)
        elif action == "submenu":
            submenu_id = item['submenu']  # Navigate to submenu
            self.history.append(self.current_menu)  # Save current menu to history
            self.current_menu = submenu_id  # Update current menu
            self.data_changed = True  # Mark data as changed
        elif action == "back":
            self.current_menu = self.history.pop()  # Go back to previous menu
            self.data_changed = True  # Mark data as changed
        elif action == "input":
            self.handle_input(item, stdscr)  # Handle user input
        elif action == "multiple_select":
            self.handle_multiple_select(item, stdscr)  # Handle multiple selections
        elif action == "checkbox":
            self.handle_checkbox(item, stdscr)  # Handle checkboxes
        elif action == "radio":
            self.handle_radio(item, stdscr)  # Handle radio buttons
        self.logger.debug("Exiting execute_action")

    def handle_input(self, item, stdscr):
        self.logger.debug(f"Entering handle_input - Arguments passed: item={item}")
        curses.echo()  # Enable echoing of typed characters
        stdscr.clear()  # Clear the screen
        h, w = stdscr.getmaxyx()  # Get terminal dimensions
        prompt = item['label'] + ": "  # Prompt user with label
        stdscr.addstr(h // 2, w // 2 - len(prompt) // 2, prompt)  # Display prompt
        stdscr.refresh()  # Refresh screen
        input_value = stdscr.getstr(h // 2, w // 2 + len(prompt) // 2).decode('utf-8')  # Capture input
        curses.noecho()  # Disable echoing
        self.logger.debug(f"Input received: {input_value}")
        self.logger.debug("Exiting handle_input")

    def handle_multiple_select(self, item, stdscr):
        self.logger.debug(f"Entering handle_multiple_select - Arguments passed: item={item}")
        options = item['options']  # Get available options
        selected_options = []  # Store selected options
        idx = 0  # Index of the current selection
        while True:
            stdscr.clear()  # Clear screen
            h, w = stdscr.getmaxyx()  # Get terminal dimensions
            for i, option in enumerate(options):
                x = w // 2 - len(option) // 2  # Center align option
                y = h // 2 - len(options) // 2 + i  # Position option
                if i == idx:
                    # Highlight current option
                    stdscr.attron(self.theme.get_color('highlight_color'))
                    stdscr.addstr(y, x, option)
                    stdscr.attroff(self.theme.get_color('highlight_color'))
                else:
                    stdscr.addstr(y, x, option)
            stdscr.refresh()  # Refresh screen
            key = stdscr.getch()  # Wait for user input
            if key == curses.KEY_UP and idx > 0:
                idx -= 1  # Move selection up
            elif key == curses.KEY_DOWN and idx < len(options) - 1:
                idx += 1  # Move selection down
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_options.append(options[idx])  # Add selected option
                break
        self.logger.debug(f"Selected options: {selected_options}")
        self.logger.debug("Exiting handle_multiple_select")

    def handle_checkbox(self, item, stdscr):
        self.logger.debug(f"Entering handle_checkbox - Arguments passed: item={item}")
        options = item['options']  # Get checkbox options
        selected_options = [False] * len(options)  # Initialize selection states
        idx = 0  # Index of the current selection
        while True:
            stdscr.clear()  # Clear screen
            h, w = stdscr.getmaxyx()  # Get terminal dimensions
            for i, option in enumerate(options):
                x = w // 2 - len(option) // 2  # Center align option
                y = h // 2 - len(options) // 2 + i  # Position option
                checkbox = '[X]' if selected_options[i] else '[ ]'  # Checkbox state
                display_text = f"{checkbox} {option}"  # Display text with checkbox
                if i == idx:
                    # Highlight current option
                    stdscr.attron(self.theme.get_color('highlight_color'))
                    stdscr.addstr(y, x, display_text)
                    stdscr.attroff(self.theme.get_color('highlight_color'))
                else:
                    stdscr.addstr(y, x, display_text)
            stdscr.refresh()  # Refresh screen
            key = stdscr.getch()  # Wait for user input
            if key == curses.KEY_UP and idx > 0:
                idx -= 1  # Move selection up
            elif key == curses.KEY_DOWN and idx < len(options) - 1:
                idx += 1  # Move selection down
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_options[idx] = not selected_options[idx]  # Toggle selection state
        self.logger.debug(f"Checkbox selections: {selected_options}")
        self.logger.debug("Exiting handle_checkbox")

    def handle_radio(self, item, stdscr):
        self.logger.debug(f"Entering handle_radio - Arguments passed: item={item}")
        options = item['options']  # Get radio button options
        selected_option = 0  # Index of the selected option
        idx = 0  # Index of the current selection
        while True:
            stdscr.clear()  # Clear screen
            h, w = stdscr.getmaxyx()  # Get terminal dimensions
            for i, option in enumerate(options):
                x = w // 2 - len(option) // 2  # Center align option
                y = h // 2 - len(options) // 2 + i  # Position option
                radio = '(O)' if i == selected_option else '( )'  # Radio button state
                display_text = f"{radio} {option}"  # Display text with radio button
                if i == idx:
                    # Highlight current option
                    stdscr.attron(self.theme.get_color('highlight_color'))
                    stdscr.addstr(y, x, display_text)
                    stdscr.attroff(self.theme.get_color('highlight_color'))
                else:
                    stdscr.addstr(y, x, display_text)
            stdscr.refresh()  # Refresh screen
            key = stdscr.getch()  # Wait for user input
            if key == curses.KEY_UP and idx > 0:
                idx -= 1  # Move selection up
            elif key == curses.KEY_DOWN and idx < len(options) - 1:
                idx += 1  # Move selection down
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_option = idx  # Select the current option
        self.logger.debug(f"Radio selection: {selected_option}")
        self.logger.debug("Exiting handle_radio")

def read_and_convert_input(queue):
    parser = pJSON()  # JSON parser instance
    parser.logger.debug("Entering read_and_convert_input")
    input_data = sys.stdin.read()  # Read input from STDIN
    sys.stdin.close()  # Close STDIN to signal end of input
    try:
        data = json.loads(input_data)  # Attempt to parse input as JSON
    except json.JSONDecodeError:
        # Convert non-JSON input to JSON format
        lines = input_data.strip().split("\n")
        data = {
            "menu_title": "Dynamic Menu",
            "menu_items": [{"label": line, "action": "none"} for line in lines]
        }

    parser.data = data  # Store parsed data
    queue.put(parser)  # Enqueue the parser instance
    parser.logger.debug("Exiting read_and_convert_input")

def main():
    global logger  # Ensure we use the global logger
    logger.debug("Entering main")
    input_queue = Queue()  # Queue for threading communication
    if len(sys.argv) > 1:
        # If configuration file is provided as an argument
        parser = pJSON()
        config = parser.read_from_file(sys.argv[1])  # Read configuration file
        parser.validate_json(menu_schema)  # Validate against schema
    else:
        # Otherwise, read from STDIN
        input_thread = threading.Thread(target=read_and_convert_input, args=(input_queue,))
        input_thread.start()
        input_thread.join()
        parser = input_queue.get()  # Get parsed data from queue
        parser.validate_json(stdin_schema)  # Validate against schema

    if parser.data:
        menu = Menu(parser.data)  # Initialize menu with parsed data
        curses.wrapper(menu.run)  # Run the menu system in a curses wrapper
    logger.debug("Exiting main")

if __name__ == "__main__":
    main()
