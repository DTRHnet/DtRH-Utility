import json
import sys
import curses
from dtrhStyle import ThemeManager
from dtrhLogger import DtrhLogger

class Menu:
    def __init__(self, config):
        self.logger = DtrhLogger()
        self.config = config
        self.current_menu = 'main'
        self.menus = {'main': config}
        self.theme = None  # Initialize theme to None here
        self.language = config['language']
        self.selected_index = 0
        self.history = []

        # Load all submenus
        if 'submenus' in config:
            for submenu_key, submenu_config in config['submenus'].items():
                self.menus[submenu_key] = submenu_config

    def get_menu_title(self):
        menu = self.menus[self.current_menu]
        return self.config['languages'][self.language].get(menu['menu_title'], menu['menu_title'])

    def get_menu_items(self):
        menu = self.menus[self.current_menu]
        return menu['menu_items']

    def display(self, stdscr):
        if not self.theme:
            self.theme = ThemeManager(self.config['theme'])  # Initialize theme after curses initscr
        curses.curs_set(0)  # Hide the cursor
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = self.get_menu_title()
        x = w // 2 - len(title) // 2
        y = h // 2 - len(self.get_menu_items()) // 2 - 1
        stdscr.addstr(y, x, title, curses.A_BOLD)
        
        for idx, item in enumerate(self.get_menu_items()):
            label = self.config['languages'][self.language].get(item['label'], item['label'])
            x = w // 2 - len(label) // 2
            y = h // 2 - len(self.get_menu_items()) // 2 + idx + 1
            if idx == self.selected_index:
                stdscr.attron(self.theme.get_color('highlight_color'))
                stdscr.addstr(y, x, label)
                stdscr.attroff(self.theme.get_color('highlight_color'))
            else:
                stdscr.addstr(y, x, label)

        stdscr.refresh()

    def run(self, stdscr):
        while True:
            self.display(stdscr)
            key = stdscr.getch()

            if key == curses.KEY_UP and self.selected_index > 0:
                self.selected_index -= 1
            elif key == curses.KEY_DOWN and self.selected_index < len(self.get_menu_items()) - 1:
                self.selected_index += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.execute_action(self.get_menu_items()[self.selected_index]['action'], stdscr)

    def execute_action(self, action, stdscr):
        item = self.get_menu_items()[self.selected_index]
        if action == "start_game":
            self.logger.log("INFO", "Starting game...")
        elif action == "exit":
            self.logger.log("INFO", "Exiting...")
            sys.exit(0)
        elif action == "submenu":
            submenu_id = item['submenu']
            self.history.append(self.current_menu)
            self.current_menu = submenu_id
        elif action == "back":
            self.current_menu = self.history.pop()
        elif action == "input":
            self.handle_input(item, stdscr)
        elif action == "multiple_select":
            self.handle_multiple_select(item, stdscr)
        elif action == "checkbox":
            self.handle_checkbox(item, stdscr)
        elif action == "radio":
            self.handle_radio(item, stdscr)

    def handle_input(self, item, stdscr):
        curses.echo()
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        prompt = item['label'] + ": "
        stdscr.addstr(h // 2, w // 2 - len(prompt) // 2, prompt)
        stdscr.refresh()
        input_value = stdscr.getstr(h // 2, w // 2 + len(prompt) // 2).decode('utf-8')
        curses.noecho()
        self.logger.log("DEBUG", f"Input received: {input_value}")

    def handle_multiple_select(self, item, stdscr):
        options = item['options']
        selected_options = []
        idx = 0
        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            for i, option in enumerate(options):
                x = w // 2 - len(option) // 2
                y = h // 2 - len(options) // 2 + i
                if i == idx:
                    stdscr.attron(self.theme.get_color('highlight_color'))
                    stdscr.addstr(y, x, option)
                    stdscr.attroff(self.theme.get_color('highlight_color'))
                else:
                    stdscr.addstr(y, x, option)
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_UP and idx > 0:
                idx -= 1
            elif key == curses.KEY_DOWN and idx < len(options) - 1:
                idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_options.append(options[idx])
                break
        self.logger.log("DEBUG", f"Selected options: {selected_options}")

    def handle_checkbox(self, item, stdscr):
        options = item['options']
        selected_options = [False] * len(options)
        idx = 0
        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            for i, option in enumerate(options):
                x = w // 2 - len(option) // 2
                y = h // 2 - len(options) // 2 + i
                checkbox = '[X]' if selected_options[i] else '[ ]'
                display_text = f"{checkbox} {option}"
                if i == idx:
                    stdscr.attron(self.theme.get_color('highlight_color'))
                    stdscr.addstr(y, x, display_text)
                    stdscr.attroff(self.theme.get_color('highlight_color'))
                else:
                    stdscr.addstr(y, x, display_text)
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_UP and idx > 0:
                idx -= 1
            elif key == curses.KEY_DOWN and idx < len(options) - 1:
                idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_options[idx] = not selected_options[idx]
        self.logger.log("DEBUG", f"Checkbox selections: {selected_options}")

    def handle_radio(self, item, stdscr):
        options = item['options']
        selected_option = 0
        idx = 0
        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            for i, option in enumerate(options):
                x = w // 2 - len(option) // 2
                y = h // 2 - len(options) // 2 + i
                radio = '(O)' if i == selected_option else '( )'
                display_text = f"{radio} {option}"
                if i == idx:
                    stdscr.attron(self.theme.get_color('highlight_color'))
                    stdscr.addstr(y, x, display_text)
                    stdscr.attroff(self.theme.get_color('highlight_color'))
                else:
                    stdscr.addstr(y, x, display_text)
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_UP and idx > 0:
                idx -= 1
            elif key == curses.KEY_DOWN and idx < len(options) - 1:
                idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_option = idx
        self.logger.log("DEBUG", f"Radio selection: {selected_option}")

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            config = json.load(f)
    else:
        config = json.load(sys.stdin)

    menu = Menu(config)
    curses.wrapper(menu.run)

if __name__ == "__main__":
    main()
