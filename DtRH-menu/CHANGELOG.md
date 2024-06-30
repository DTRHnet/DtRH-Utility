### CHANGELOG.md
```markdown
# Changelog

### CHANGELOG.md

## v0.0.2 - 2024-06-29
### Added
- Modularized schema definitions into `schemas.py` for easier expansion and modification.
- Detailed logging within the menu system for better debugging and traceability.
- Dynamic STDIN handling with JSON conversion, improving flexibility for menu inputs.

### Improved
- Enhanced user interface with customizable themes through the DtRH-Style module.
- Improved threading and input handling in the menu system to prevent blocking and enhance responsiveness.

### Fixed
- Addressed issues with navigation in the menu system when using STDIN inputs.
- Resolved flickering and redraw issues by implementing efficient screen refresh logic.

### Removed
- Hard-coded schemas from the main `dtrhMenu.py` file, moving them to a separate module for better modularity.
All notable changes to this project will be documented in this file.


## [0.0.1] - 2024-06-27
### Added
- Initial release with support for:
  - Dynamic JSON configuration
  - Themed menus with customizable colors
  - Nested submenus
  - Various menu entry controls (static select, multiple select, input fields, checkboxes, radio buttons)
  - Multi-language support
  - Advanced logging with five log levels
