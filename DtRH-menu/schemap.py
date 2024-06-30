# schemap.py
# The schema mapper..

menu_schema = {
    "type": "object",
    "properties": {
        "menu_title": {"type": "string"},
        "language": {"type": "string"},
        "theme": {"type": "object"},
        "menu_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "action": {"type": "string"}
                },
                "required": ["label", "action"]
            }
        },
        "submenus": {"type": "object"},
        "languages": {"type": "object"}
    },
    "required": ["menu_title", "language", "menu_items"]
}

stdin_schema = {
    "type": "object",
    "properties": {
        "menu_title": {"type": "string"},
        "menu_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "action": {"type": "string"}
                },
                "required": ["label", "action"]
            }
        }
    },
    "required": ["menu_title", "menu_items"]
}
