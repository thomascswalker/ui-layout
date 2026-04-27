import argparse
from ctypes import byref
from ctypes.wintypes import MSG, RECT

from ui.platform import win32
from ui.render import render_file
from ui.logger import init_logging

NULL = 0
WM_PAINT = 15
WM_DESTROY = 2
DT_SINGLELINE = 32
DT_CENTER = 1
DT_VCENTER = 4


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

    if False:
        render_file(args.file)
        return 0
    else:

        def wnd_proc(hwnd: int, msg: int, wparam: int, lparam: int):
            ps = win32.PaintStruct()
            rect = RECT()

            match msg:
                case win32.WindowsMessage.DESTROY:
                    win32.post_quit_message(0)
                    return 0
                case win32.WindowsMessage.PAINT:
                    hdc = win32.begin_paint(hwnd, ps)
                    win32.get_client_rect(hwnd, rect)
                    win32.draw_text(
                        hdc,
                        "A window",
                        -1,
                        rect,
                        DT_SINGLELINE | DT_CENTER | DT_VCENTER,
                    )
                    win32.end_paint(hwnd, ps)
                    return 0

            return win32.def_window_proc(hwnd, msg, wparam, lparam)

        window = win32.Window("Python win32", wnd_proc)
        window.show()

        msg = MSG()
        while win32.get_message(msg, 0, 0, 0) != 0:
            win32.translate_message(msg)
            win32.dispatch_message(msg)

        return msg.wParam
