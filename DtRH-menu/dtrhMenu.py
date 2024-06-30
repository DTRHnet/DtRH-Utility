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


# ======================
#  External Dependencies
# ======================================================================================================
import sys           # System-specific parameters and functions
import threading     # Multi-threading
import json          # JSON parsing and manipulation
from queue import Queue             # Thread-safe queue implementation
from dtrhStyle import ThemeManager  # Custom theme management for the menu
from dtrhLogger import DtrhLogger   # Custom logging for the application
from dtrhParser import pJSON        # Custom JSON parsing
from schemap import * # JSON schemas for STDIN


# ======================
#  CLASS - Menu
#  
#  Class for managing menu display and interactions
# ======================================================================================================
class Menu:
    #
    def __init__(self, config):
        self.logger = DtrhLogger()     # Logger instance for debugging and info
        self.logger.log("DEBUG", f"Entering __init__ - Arguments passed: config={config}")
        self.config = config           # Configuration data for the menu
        self.current_menu = 'main'     
        self.menus = {'main': config} 
        self.theme = None              # Theme manager (initialized later)
        self.language = config.get('language', 'en')  # Language setting
        self.selected_index = 0        # Index of the currently selected menu item
        self.history = []              # History of menu navigation for back functionality
        self.data_changed = True       # Flag to indicate if data has changed and needs refreshing

        # Setup submenus if provided in configuration
        if 'submenus' in config:
            for submenu_key, submenu_config in config['submenus'].items():
                self.menus[submenu_key] = submenu_config

        self.logger.log("DEBUG", "Exiting __init__")

# ======================
#  Menu.get_menu_title()
#  
#  Retrieve the title of the current menu
# ======================================================================================================
    def get_menu_title(self):
        self.logger.log("DEBUG", "Entering get_menu_title")
        menu = self.menus[self.current_menu]           # Access current menu data
        title = self.config.get('menu_title', 'Menu')  # Default to 'Menu' if no title provided
        self.logger.log("DEBUG", f"Exiting get_menu_title - Return: {title}")
        return title

# ======================
#  Menu.get_menu_items()
#  
#  Retrieve the items of the current menu
# ======================================================================================================
    def get_menu_items(self):
        self.logger.log("DEBUG", "Entering get_menu_items")
        menu = self.menus[self.current_menu]  # Access current menu data
        items = menu['menu_items']            # Retrieve menu items
        self.logger.log("DEBUG", f"Exiting get_menu_items - Return: {items}")
        return items

# ======================
#  Menu.display()
#  
#  Render the menu interface in the terminal
# ======================================================================================================
    def display(self, stdscr):
        self.logger.log("DEBUG", "Entering display")
        if not self.theme:
            # Initialize theme if not already set
            default_theme = {
                "highlight_color": "cyan",
                "normal_color": "white"
            }
            self.theme = ThemeManager(self.config.get('theme', default_theme))
        curses.curs_set(0)  # Hide the cursor in the terminal

        if self.data_changed:
            stdscr.clear()                  # Clear the screen for fresh rendering
            h, w = stdscr.getmaxyx()        # Get terminal dimensions
            title = self.get_menu_title()   # Get the menu title
            x = w // 2 - len(title) // 2    # Calculate center position for title
            y = h // 2 - len(self.get_menu_items()) // 2 - 1  # Calculate start position for items
            stdscr.addstr(y, x, title, curses.A_BOLD)         # Display title

            # Iterate through menu items and display them
            for idx, item in enumerate(self.get_menu_items()):
                label = item['label']         # Menu item label
                x = w // 2 - len(label) // 2  # Center align label
                y = h // 2 - len(self.get_menu_items()) // 2 + idx + 1  # Position items vertically
                if idx == self.selected_index:
                    # Highlight the selected item
                    stdscr.attron(self.theme.get_color('highlight_color'))
                    stdscr.addstr(y, x, label)
                    stdscr.attroff(self.theme.get_color('highlight_color'))
                else:
                    stdscr.addstr(y, x, label)

            stdscr.refresh()           # Refresh the screen to display changes
            self.data_changed = False  # Reset change flag
        self.logger.log("DEBUG", "Exiting display")

# ======================
#  Menu.run()
#  
#  Main loop to capture user input and update the menu
# ======================================================================================================
    def run(self, stdscr):
        self.logger.log("DEBUG", "Entering run")
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
        self.logger.log("DEBUG", "Exiting run")

# ======================
#  Menu.execute_action()
#  
#  Execute the specified action for the selected menu item
# ======================================================================================================
    def execute_action(self, action, stdscr):
        self.logger.log("DEBUG", f"Entering execute_action - Arguments passed: action={action}")
        item = self.get_menu_items()[self.selected_index]  # Get the selected item
        if action == "start_game":
            self.logger.log("INFO", "Starting game...")
        elif action == "exit":
            self.logger.log("INFO", "Exiting...")
            sys.exit(0)
        elif action == "submenu":
            submenu_id = item['submenu']            # Navigate to submenu
            self.history.append(self.current_menu)  # Save current menu to history
            self.current_menu = submenu_id          # Update current menu
            self.data_changed = True                # Mark data as changed
        elif action == "back":
            self.current_menu = self.history.pop()  # Go back to previous menu
            self.data_changed = True                # Mark data as changed
        elif action == "input":
            self.handle_input(item, stdscr)         # Handle user input
        elif action == "multiple_select":
            self.handle_multiple_select(item, stdscr)  # Handle multiple selections
        elif action == "checkbox":
            self.handle_checkbox(item, stdscr)      # Handle checkboxes
        elif action == "radio":
            self.handle_radio(item, stdscr)         # Handle radio buttons
        self.logger.log("DEBUG", "Exiting execute_action")

# ======================
#  Menu.handle_input()
#  
#  Capture and handle user text input
# ======================================================================================================
    def handle_input(self, item, stdscr):
        self.logger.log("DEBUG", f"Entering handle_input - Arguments passed: item={item}")
        curses.echo()   # Enable echoing of typed characters
        stdscr.clear()  # Clear the screen
        h, w = stdscr.getmaxyx()       # Get terminal dimensions
        prompt = item['label'] + ": "  # Prompt user with label
        stdscr.addstr(h // 2, w // 2 - len(prompt) // 2, prompt)  # Display prompt
        stdscr.refresh()  # Refresh screen
        input_value = stdscr.getstr(h // 2, w // 2 + len(prompt) // 2).decode('utf-8')  # Capture input
        curses.noecho()   # Disable echoing
        self.logger.log("DEBUG", f"Input received: {input_value}")
        self.logger.log("DEBUG", "Exiting handle_input")

# ======================
#  Menu.handle_multiple_select()
#  
#  Handle user selections from multiple options
# ======================================================================================================
    def handle_multiple_select(self, item, stdscr):
        self.logger.log("DEBUG", f"Entering handle_multiple_select - Arguments passed: item={item}")
        options = item['options']  # Get available options
        selected_options = []      # Store selected options
        idx = 0                    # Index of the current selection
        while True:
            stdscr.clear()         # Clear screen
            h, w = stdscr.getmaxyx()  # Get terminal dimensions
            for i, option in enumerate(options):
                x = w // 2 - len(option) // 2       # Center align option
                y = h // 2 - len(options) // 2 + i  # Position option
                if i == idx:
                    # Highlight current option
                    stdscr.attron(self.theme.get_color('highlight_color'))
                    stdscr.addstr(y, x, option)
                    stdscr.attroff(self.theme.get_color('highlight_color'))
                else:
                    stdscr.addstr(y, x, option)
            stdscr.refresh()      # Refresh screen
            key = stdscr.getch()  # Wait for user input
            if key == curses.KEY_UP and idx > 0:
                idx -= 1  # Move selection up
            elif key == curses.KEY_DOWN and idx < len(options) - 1:
                idx += 1  # Move selection down
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_options.append(options[idx])  # Add selected option
                break
        self.logger.log("DEBUG", f"Selected options: {selected_options}")
        self.logger.log("DEBUG", "Exiting handle_multiple_select")

# ======================
#  Menu.handle_checkbox()
#  
#  Handle checkbox selections
# ======================================================================================================
    def handle_checkbox(self, item, stdscr):
        self.logger.log("DEBUG", f"Entering handle_checkbox - Arguments passed: item={item}")
        options = item['options']  # Get checkbox options
        selected_options = [False] * len(options)  # Initialize selection states
        idx = 0                    # Index of the current selection
        while True:
            stdscr.clear()            # Clear screen
            h, w = stdscr.getmaxyx()  # Get terminal dimensions
            for i, option in enumerate(options):
                x = w // 2 - len(option) // 2       # Center align option
                y = h // 2 - len(options) // 2 + i  # Position option
                checkbox = '[X]' if selected_options[i] else '[ ]'  # Checkbox state
                display_text = f"{checkbox} {option}"               # Display text with checkbox
                if i == idx:
                    # Highlight current option
                    stdscr.attron(self.theme.get_color('highlight_color'))
                    stdscr.addstr(y, x, display_text)
                    stdscr.attroff(self.theme.get_color('highlight_color'))
                else:
                    stdscr.addstr(y, x, display_text)
            stdscr.refresh()      # Refresh screen
            key = stdscr.getch()  # Wait for user input
            if key == curses.KEY_UP and idx > 0:
                idx -= 1  # Move selection up
            elif key == curses.KEY_DOWN and idx < len(options) - 1:
                idx += 1  # Move selection down
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_options[idx] = not selected_options[idx]  # Toggle selection state
        self.logger.log("DEBUG", f"Checkbox selections: {selected_options}")
        self.logger.log("DEBUG", "Exiting handle_checkbox")

# ======================
#  Menu.handle_radio()
#  
#  Handle radio button selections
# ======================================================================================================
    def handle_radio(self, item, stdscr):
        self.logger.log("DEBUG", f"Entering handle_radio - Arguments passed: item={item}")
        options = item['options']  # Get radio button options
        selected_option = 0        # Index of the selected option
        idx = 0  # Index of the current selection
        while True:
            stdscr.clear()  # Clear screen
            h, w = stdscr.getmaxyx()           # Get terminal dimensions
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
            stdscr.refresh()      # Refresh screen
            key = stdscr.getch()  # Wait for user input
            if key == curses.KEY_UP and idx > 0:
                idx -= 1  # Move selection up
            elif key == curses.KEY_DOWN and idx < len(options) - 1:
                idx += 1  # Move selection down
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_option = idx  # Select the current option
        self.logger.log("DEBUG", f"Radio selection: {selected_option}")
        self.logger.log("DEBUG", "Exiting handle_radio")

# ======================
#  read_and_convert_input
#  
#  Read from STDIN, convert non-JSON input to JSON, and enqueue the result
# ======================================================================================================
def read_and_convert_input(queue):
    parser = pJSON()  # JSON parser instance
    parser.logger.log("DEBUG", "Entering read_and_convert_input")
    input_data = sys.stdin.read()  # Read input from STDIN
    sys.stdin.close()              # Close STDIN to signal end of input
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
    queue.put(parser)   # Enqueue the parser instance
    parser.logger.log("DEBUG", "Exiting read_and_convert_input")

# ======================
#  main
#  
#  Main function to initialize and run the menu system
# ======================================================================================================
def main():
    logger = DtrhLogger()  # Logger instance for debugging and info
    logger.log("DEBUG", "Entering main")
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
    logger.log("DEBUG", "Exiting main")

if __name__ == "__main__":
    main()

