from enum import IntEnum

import ctypes
from ctypes import wintypes
from winapi_gen import *  # noqa
import winapi_gen

WNDPROC = ctypes.WINFUNCTYPE(
    winapi_gen.LRESULT,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)


class WindowsMessage(IntEnum):
    DESTROY = 2
    PAINT = 15


CW_USEDEFAULT = ctypes.c_int(0x80000000).value
IDI_APPLICATION = wintypes.LPCWSTR(32512)

WS_OVERLAPPED = 0x00000000
WS_CAPTION = 0x00C00000
WS_SYSMENU = 0x00080000
WS_THICKFRAME = 0x00040000
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000

WS_OVERLAPPEDWINDOW = (
    WS_OVERLAPPED
    | WS_CAPTION
    | WS_SYSMENU
    | WS_THICKFRAME
    | WS_MINIMIZEBOX
    | WS_MAXIMIZEBOX
)
assert WS_OVERLAPPEDWINDOW == 0x00CF0000

CS_HREDRAW = 2
CS_VREDRAW = 1

IDC_ARROW = wintypes.LPCWSTR(32512)
WHITE_BRUSH = 0

SW_SHOWNORMAL = 1

WM_PAINT = 15
WM_DESTROY = 2
DT_SINGLELINE = 32
DT_CENTER = 1
DT_VCENTER = 4


class Window:
    def __init__(self, name: str, wnd_proc):
        # Define Window Class
        self.cls = winapi_gen.WndClassExW()
        self.cls.style = CS_HREDRAW | CS_VREDRAW
        self.cls.lpfnWndProc = WNDPROC(wnd_proc)
        self.cls.cbClsExtra = 0
        self.cls.cbWndExtra = 0
        self.cls.hInstance = winapi_gen.get_module_handle(None)
        self.cls.hIcon = winapi_gen.load_icon(0, IDI_APPLICATION)
        self.cls.hCursor = winapi_gen.load_cursor(0, IDC_ARROW)
        self.cls.hbrBackground = winapi_gen.get_stock_object(WHITE_BRUSH)
        self.cls.lpszMenuName = None
        self.cls.lpszClassName = "WindowClassName"

        # Register Window Class
        winapi_gen.register_class_ex(self.cls)

        # Create Window
        self.hwnd = winapi_gen.create_window_ex(
            0,
            self.cls.lpszClassName,
            name,
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            0,
            0,
            self.cls.hInstance,
            None,
        )

    def show(self):
        winapi_gen.show_window(self.hwnd, SW_SHOWNORMAL)
        winapi_gen.update_window(self.hwnd)
