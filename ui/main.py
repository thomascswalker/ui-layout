import argparse
from ctypes import byref, windll
from ctypes.wintypes import MSG, RECT

from ui.platform.win32 import PAINTSTRUCT
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
        from ui.platform.win32 import create_window

        def callback(hwnd: int, msg: int, wparam: int, lparam: int) -> int:
            print(f"Message: {msg}")

            ps = PAINTSTRUCT()
            rect = RECT()

            if msg == WM_DESTROY:  # WM_DESTROY
                print("Destroying window...")
                windll.user32.PostQuitMessage(0)
                return 0
            if msg == WM_PAINT:  # WM_PAINT
                print("Painting...")
                hdc = windll.user32.BeginPaint(hwnd, byref(ps))
                windll.user32.GetClientRect(hwnd, byref(rect))
                windll.user32.DrawTextW(
                    hdc,
                    "Python Powered Windows 你好吗？",
                    -1,
                    byref(rect),
                    DT_SINGLELINE | DT_CENTER | DT_VCENTER,
                )
                windll.user32.EndPaint(hwnd, byref(ps))
                return 0

            return windll.user32.DefWindowProcW(hwnd, msg, wparam, lparam)

        create_window("My Window", callback)
        msg = MSG()
        pmsg = byref(msg)

        while windll.user32.GetMessageW(pmsg, None, 0, 0):
            windll.user32.TranslateMessage(pmsg)
            windll.user32.DispatchMessageW(pmsg)

        ret_code = msg.wParam
        print(f"Return code: {ret_code}")
        return ret_code
