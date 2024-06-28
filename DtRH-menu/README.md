# dtrhMenu

dtrhMenu is one of many versatile components which collectively create the dtrhUtility suite. It provides a comprehensive set of functions to create and manage both static and dynamic menu systems. Written in Python and utilizing the ncurses library, it ensures broad compatibility across various operating systems while maintaining very little library external library dependances. The system primarily renders menus via custom JSON formatted input, either through configuration files or on the fly via STDIN. Error checking, advanced logging capabilities, and design with modularity in mind make for seamless integration into diverse projects with little hassle.

## Features
- Dynamic configuration via JSON files
- Themed menus with customizable colors
- Support for nested submenus
- Multiple menu entry controls:
  - Static select
  - Multiple select
  - Input fields
  - Checkboxes
  - Radio buttons
- Multi-language support
- Advanced logging with five log levels

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/dtrhMenu-v0.0.1.git
    ```

2. Navigate to the project directory:
    ```bash
    cd dtrhMenu-v0.0.1
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the menu system with a JSON configuration file:
```bash
python3 dtrhMenu.py path/to/config.json
