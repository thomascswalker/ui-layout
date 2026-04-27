from enum import IntEnum
from ctypes import (
    POINTER,
    WINFUNCTYPE,
    Structure,
    WinDLL,
    WinError,
    byref,
    c_int,
    c_int64,
    c_void_p,
)
from ctypes.wintypes import (
    ATOM,
    BOOL,
    BYTE,
    DWORD,
    HBRUSH,
    HDC,
    HGDIOBJ,
    HICON,
    HINSTANCE,
    HMENU,
    HMODULE,
    HWND,
    LPARAM,
    LPCWSTR,
    LPVOID,
    MSG,
    RECT,
    UINT,
    WPARAM,
)
from typing import Callable


def errcheck(result, *_):
    if result is None or result == 0:
        raise WinError()
    return result


def minusonecheck(result, *_):
    if result == -1:
        raise WinError()
    return result


LRESULT = c_int64
HCURSOR = c_void_p
WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)


def MAKEINTRESOURCE(x):
    return LPCWSTR(x)


class WNDCLASSEX(Structure):
    _fields_ = (
        ("style", UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", c_int),
        ("cbWndExtra", c_int),
        ("hInstance", HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", LPCWSTR),
        ("lpszClassName", LPCWSTR),
    )


class PAINTSTRUCT(Structure):
    _fields_ = (
        ("hdc", HDC),
        ("fErase", BOOL),
        ("rcPaint", RECT),
        ("fRestore", BOOL),
        ("fIncUpdate", BOOL),
        ("rgbReserved", BYTE * 32),
    )


KERNEL32 = WinDLL("kernel32", use_last_error=True)
USER32 = WinDLL("user32", use_last_error=True)

CreateWindow = USER32.CreateWindowExW
CreateWindow.argtypes = (
    DWORD,
    LPCWSTR,
    LPCWSTR,
    DWORD,
    c_int,
    c_int,
    c_int,
    c_int,
    HWND,
    HMENU,
    HINSTANCE,
    LPVOID,
)
CreateWindow.restype = HWND
CreateWindow.errcheck = errcheck

GetModuleHandle = KERNEL32.GetModuleHandleW
GetModuleHandle.argtypes = (LPCWSTR,)
GetModuleHandle.restype = HMODULE
GetModuleHandle.errcheck = errcheck


def get_module_handle(name: str) -> int:
    return GetModuleHandle(name)


LoadIcon = USER32.LoadIconW
LoadIcon.argtypes = HINSTANCE, LPCWSTR
LoadIcon.restype = HICON
LoadIcon.errcheck = errcheck

LoadCursor = USER32.LoadCursorW
LoadCursor.argtypes = HINSTANCE, LPCWSTR
LoadCursor.restype = HCURSOR
LoadCursor.errcheck = errcheck

RegisterClass = USER32.RegisterClassW
RegisterClass.argtypes = (POINTER(WNDCLASSEX),)
RegisterClass.restype = ATOM
RegisterClass.errcheck = errcheck

ShowWindow = USER32.ShowWindow
ShowWindow.argtypes = HWND, c_int
ShowWindow.restype = BOOL


def show_window(hwnd: int, flags: int) -> bool:
    return ShowWindow(hwnd, flags)


UpdateWindow = USER32.UpdateWindow
UpdateWindow.argtypes = (HWND,)
UpdateWindow.restype = BOOL
UpdateWindow.errcheck = errcheck

GetMessage = USER32.GetMessageW
GetMessage.argtypes = POINTER(MSG), HWND, UINT, UINT
GetMessage.restype = BOOL
GetMessage.errcheck = minusonecheck

TranslateMessage = USER32.TranslateMessage
TranslateMessage.argtypes = (POINTER(MSG),)
TranslateMessage.restype = BOOL

DispatchMessageW = USER32.DispatchMessageW
DispatchMessageW.argtypes = (POINTER(MSG),)
DispatchMessageW.restype = LRESULT

BeginPaint = USER32.BeginPaint
BeginPaint.argtypes = HWND, POINTER(PAINTSTRUCT)
BeginPaint.restype = HDC

GetClientRect = USER32.GetClientRect
GetClientRect.argtypes = HWND, POINTER(RECT)
GetClientRect.restype = BOOL
GetClientRect.errcheck = errcheck

DrawText = USER32.DrawTextW
DrawText.argtypes = HDC, LPCWSTR, c_int, POINTER(RECT), UINT
DrawText.restype = c_int

EndPaint = USER32.EndPaint
EndPaint.argtypes = HWND, POINTER(PAINTSTRUCT)
EndPaint.restype = BOOL


PostQuitMessage: Callable[[int], None] = USER32.PostQuitMessage
PostQuitMessage.argtypes = (c_int,)
PostQuitMessage.restype = None


def post_quit_message(code: int) -> None:
    return PostQuitMessage(code)


DefWindowProcW = USER32.DefWindowProcW
DefWindowProcW.argtypes = HWND, UINT, WPARAM, LPARAM
DefWindowProcW.restype = LRESULT

GDI32 = WinDLL("gdi32", use_last_error=True)
GetStockObject = GDI32.GetStockObject
GetStockObject.argtypes = (c_int,)
GetStockObject.restype = HGDIOBJ

CW_USEDEFAULT = c_int(0x80000000).value
IDI_APPLICATION = MAKEINTRESOURCE(32512)

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

IDC_ARROW = MAKEINTRESOURCE(32512)
WHITE_BRUSH = 0

SW_SHOWNORMAL = 1

WM_PAINT = 15
WM_DESTROY = 2
DT_SINGLELINE = 32
DT_CENTER = 1
DT_VCENTER = 4


class WindowsMessage(IntEnum):
    DESTROY = 2
    PAINT = 15


class Window:
    def __init__(self, name: str, wnd_proc):
        # Define Window Class
        self.cls = WNDCLASSEX()
        self.cls.style = CS_HREDRAW | CS_VREDRAW
        self.cls.lpfnWndProc = WNDPROC(wnd_proc)
        self.cls.cbClsExtra = 0
        self.cls.cbWndExtra = 0
        self.cls.hInstance = GetModuleHandle(None)
        self.cls.hIcon = LoadIcon(None, IDI_APPLICATION)
        self.cls.hCursor = LoadCursor(None, IDC_ARROW)
        self.cls.hbrBackground = GetStockObject(WHITE_BRUSH)
        self.cls.lpszMenuName = None
        self.cls.lpszClassName = "WindowClassName"

        # Register Window Class
        RegisterClass(byref(self.cls))

        # Create Window
        self.hwnd = CreateWindow(
            0,
            self.cls.lpszClassName,
            name,
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            None,
            None,
            self.cls.hInstance,
            None,
        )

    def show(self):
        ShowWindow(self.hwnd, SW_SHOWNORMAL)
        UpdateWindow(self.hwnd)
