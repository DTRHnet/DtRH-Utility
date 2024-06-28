# dtrhMenu

dtrhMenu is a modular, advanced, themed menu system in Python. It supports dynamic configuration through JSON files and allows for various types of menu controls including static select, multiple select, input fields, checkboxes, and radio buttons. The menu system is designed to be flexible and easily customizable.

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
