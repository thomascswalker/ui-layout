import argparse
import sys

from ui.logger import init_logging

match sys.platform:
    case "win32":
        from ui.platform.win32.window import Win32Window as Window
    case "linux" | "linux2":
        from ui.platform.linux.window import LinuxWindow as Window
    case _:
        raise OSError(f"No window implementation for platform {sys.platform!r}.")


def main() -> int:
    """Command-line entry point for rendering UI layout files."""
    init_logging()
    parser = argparse.ArgumentParser(
        description="Render a UI layout from an HTML file",
    )
    parser.add_argument(
        "file",
        help="Path to the HTML file to render",
    )
    args = parser.parse_args()
    window = Window(args.file)
    window.show()
    return window.run()
