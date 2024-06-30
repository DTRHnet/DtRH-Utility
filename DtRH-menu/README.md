# DtRH-Menu

DtRH-Menu is a versatile component within the DtRH-Utility suite, with the aim of providing a comprehensive set of functions to create and manage both static and dynamic menu systems. It is written in Python and utilizes the ncurses library to ensure broad compatibility across various operating systems with minimal external dependencies. 

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
    git clone https://github.com/DTRHnet/DtRH-Utility.git
    ```

2. Navigate to the project directory:
    ```bash
    cd dtrhMenu
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The menu system expects input in one of two ways - either a json formatted configuration file or unformatted data via stdin. Sample configuration files can be found in the 'conf' and 'conf/tests' folders:

```bash
python3 dtrhMenu.py conf/tests/menu_controls.json
```

Please note that menu creation via stdin is still a work in progress due to how ncurses processes getch(). However, you can still display a menu, albeit with no navigation via piping:

```bash
# Discover lan devices with nmap and list them as a menu
nmap -sn 10.0.0.1/24 | grep -v Host | grep 10 | awk -F' ' '{print $5}' | python3 dtrhMenu.py
```

