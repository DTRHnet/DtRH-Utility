import curses

class ThemeManager:
    def __init__(self, theme_config):
        self.theme_config = theme_config
        self.color_pairs = {}
        self.init_colors()

    def init_colors(self):
        curses.start_color()
        # Assign color pair numbers starting from 1 (0 is reserved)
        self.color_pairs = {
            "highlight_color": self.init_color_pair(self.theme_config.get('highlight_color', 'cyan'), 'black', 1),
            "text_color": self.init_color_pair(self.theme_config.get('text_color', 'white'), 'black', 2),
            "background_color": self.init_color_pair(self.theme_config.get('background_color', 'black'), 'black', 3)
        }

    def init_color_pair(self, fg, bg, pair_number):
        color_map = {
            "black": curses.COLOR_BLACK,
            "red": curses.COLOR_RED,
            "green": curses.COLOR_GREEN,
            "yellow": curses.COLOR_YELLOW,
            "blue": curses.COLOR_BLUE,
            "magenta": curses.COLOR_MAGENTA,
            "cyan": curses.COLOR_CYAN,
            "white": curses.COLOR_WHITE
        }
        fg_color = color_map.get(fg, curses.COLOR_WHITE)
        bg_color = color_map.get(bg, curses.COLOR_BLACK)
        curses.init_pair(pair_number, fg_color, bg_color)
        return curses.color_pair(pair_number)

    def get_color(self, color_name):
        return self.color_pairs.get(color_name, curses.color_pair(0))  # Default to pair 0 if not found

