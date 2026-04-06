import argparse

from ui.render import render_file


def main() -> None:
    """Command-line entry point for rendering UI layout files."""
    parser = argparse.ArgumentParser(description="Render a UI layout from an XML file")
    parser.add_argument(
        "file",
        help="Path to the XML file to render",
    )
    args = parser.parse_args()
    render_file(args.file)
