# DtRH Utility Suite

The DtRH Utility Suite is a comprehensive collection of modular tools designed to enhance terminal-based applications. It includes customizable menu systems, advanced logging capabilities, a flexible styling framework, robust communication classes, and a simplified tmux wrapper. All modules are built to integrate seamlessly and provide a robust user experience.

## Modules

### 1. DtRH-Menu

The DtRH-Menu is a dynamic and modular system that enables the creation of interactive terminal menus. It supports features such as:

- **Dynamic Configuration**: Build menus from JSON configurations or standard input.
- **Theming**: Customize the look and feel with the integrated ThemeManager.
- **Multi-language Support**: Easily switch languages for menu items and labels.

### 2. DtRH-Logger

The DtRH-Logger is a versatile logging system tailored for terminal applications, providing:

- **Comprehensive Logging**: Supports multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- **File and Console Outputs**: Logs can be written to both a file and the console for easy monitoring.
- **Flexible Configuration**: Customize log formats and destinations.

### 3. DtRH-Style

The DtRH-Style module offers a powerful CLI styling system that includes:

- **Color Customization**: Define and apply color schemes using the ThemeManager.
- **Curses Integration**: Leverage `curses` for advanced terminal display options.
- **Ease of Use**: Apply styles and themes across your application with minimal setup.

### 4. DtRH-Comm

The DtRH-Comm module provides robust communication classes with support for tools like tmux and reptyr, offering:

- **Session Management**: Easily manage tmux sessions and windows.
- **Process Control**: Seamless integration with reptyr for controlling processes.
- **Advanced Functionality**: Scriptable interfaces for automating complex workflows.

### 5. DtRH-tmux

DtRH-tmux is a simplified tmux wrapper built with ease of use in mind. It does not require libtmux and its implementation is not as strict in comparison, however, the caveate less overall control. Features include

- **Ease of Use**: Straightforward interface for tmux commands.
- **Session and Window Management**: Simplified methods to create and control tmux sessions and windows.
- **Scriptability**: Ideal for users looking for a lightweight and intuitive tmux experience.

## Installation

To install the DtRH Utility Suite, clone the repository and install the necessary dependencies:

``` bash
git clone https://github.com/DTRHnet/DtRH-Utility.git
cd DtRH-Utility
pip install -r requirements.txt
```

## Getting Started

Each module is designed to be used independently or in combination. Refer to the specific module documentation for detailed instructions on usage and configuration.

## License

This project is licensed under the MIT License. See the LICENSE.md file for details.
