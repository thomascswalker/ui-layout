def parse_style(style: str) -> dict[str, str]:
    """Parse a CSS style string into a dictionary."""

    if not style:
        return {}

    styles = {}

    # Split by semicolon and strip whitespace
    for decl in style.split(";"):
        decl = decl.strip()
        if ":" in decl:
            prop, value = decl.split(":", 1)
            styles[prop.strip()] = value.strip()

    return styles
