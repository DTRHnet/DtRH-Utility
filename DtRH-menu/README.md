# dtrhMenu

dtrhMenu is a versatile component within the dtrhUtility suite, providing a comprehensive set of functions to create and manage both static and dynamic menu systems. Written in Python and utilizing the ncurses library, it ensures broad compatibility across various operating systems with minimal external dependencies. 

The system primarily renders menus via custom JSON formatted input, either from configuration files or dynamically through STDIN. Its design emphasizes robust error checking, advanced logging capabilities, and modularity, allowing for seamless integration into diverse projects with minimal hassle.

## Features
- Dynamic configuration via JSON files
- Modular design
- Themed menus with customizable colors
- Support for nested submenus 
- Multiple menu entry controls:
  - Static select
  - Multiple select
  - Input fields
  - Checkboxes
  - Radio buttons
- Multi-language support
- Advanced logging 

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
