from __future__ import annotations

import ctypes
from ctypes import wintypes
from typing import Any

_DLL_CACHE: dict[str, ctypes.WinDLL] = {}
LRESULT = c_uint64

def _get_dll(name: str) -> ctypes.WinDLL:
    key = name.lower()
    dll = _DLL_CACHE.get(key)
    if dll is None:
        dll = ctypes.WinDLL(name, use_last_error=True)
        _DLL_CACHE[key] = dll
    return dll

class Point(ctypes.Structure):
    """ctypes.Structure for POINT."""
    _fields_ = [
        ("x", wintypes.LONG),
        ("y", wintypes.LONG),
    ]

class Msg(ctypes.Structure):
    """ctypes.Structure for MSG."""
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("w_param", wintypes.WPARAM),
        ("l_param", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", Point),
    ]

class PaintStruct(ctypes.Structure):
    """ctypes.Structure for PAINTSTRUCT."""
    _fields_ = [
        ("hdc", wintypes.HDC),
        ("f_erase", wintypes.BOOL),
        ("rc_paint", wintypes.RECT),
        ("f_restore", wintypes.BOOL),
        ("f_inc_update", wintypes.BOOL),
        ("rgb_reserved", ctypes.c_byte * 32),
    ]

class WndClassExW(ctypes.Structure):
    """ctypes.Structure for WNDCLASSEXW."""
    _fields_ = [
        ("cb_size", wintypes.UINT),
        ("style", wintypes.UINT),
        ("lpfn_wnd_proc", ctypes.c_void_p),
        ("cb_cls_extra", ctypes.c_int),
        ("cb_wnd_extra", ctypes.c_int),
        ("h_instance", wintypes.HINSTANCE),
        ("h_icon", wintypes.HICON),
        ("h_cursor", wintypes.HCURSOR),
        ("hbr_background", wintypes.HBRUSH),
        ("lpsz_menu_name", wintypes.LPCWSTR),
        ("lpsz_class_name", wintypes.LPCWSTR),
        ("h_icon_sm", wintypes.HICON),
    ]

ShowWindow = _get_dll('user32').ShowWindow
ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)
ShowWindow.restype = wintypes.BOOL

def show_window(hwnd: int, flags: int) -> bool:
    return ShowWindow(hwnd, flags)

GetModuleHandleW = _get_dll('kernel32').GetModuleHandleW
GetModuleHandleW.argtypes = (wintypes.LPCWSTR,)
GetModuleHandleW.restype = wintypes.HMODULE

def get_module_handle(module_name: str | None) -> int:
    return GetModuleHandleW(module_name)

MessageBoxW = _get_dll('user32').MessageBoxW
MessageBoxW.argtypes = (wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT)
MessageBoxW.restype = ctypes.c_int

def message_box(hwnd: int, text: str | None, caption: str | None, type: int) -> int:
    return MessageBoxW(hwnd, text, caption, type)

Beep = _get_dll('kernel32').Beep
Beep.argtypes = (wintypes.DWORD, wintypes.DWORD)
Beep.restype = wintypes.BOOL

def beep(frequency: int, duration: int) -> bool:
    return Beep(frequency, duration)

SetWindowTextW = _get_dll('user32').SetWindowTextW
SetWindowTextW.argtypes = (wintypes.HWND, wintypes.LPCWSTR)
SetWindowTextW.restype = wintypes.BOOL

def set_window_text(hwnd: int, text: str | None) -> bool:
    return SetWindowTextW(hwnd, text)

BeginPaint = _get_dll('user32').BeginPaint
BeginPaint.argtypes = (wintypes.HWND, ctypes.POINTER(PaintStruct))
BeginPaint.restype = wintypes.HDC

def begin_paint(hwnd: int, paint_struct: Any) -> int:
    return BeginPaint(hwnd, paint_struct)

EndPaint = _get_dll('user32').EndPaint
EndPaint.argtypes = (wintypes.HWND, ctypes.POINTER(PaintStruct))
EndPaint.restype = wintypes.BOOL

def end_paint(hwnd: int, paint_struct: Any) -> bool:
    return EndPaint(hwnd, paint_struct)

PostQuitMessage = _get_dll('user32').PostQuitMessage
PostQuitMessage.argtypes = (ctypes.c_int,)
PostQuitMessage.restype = None

def post_quit_message(exit_code: int) -> Any:
    return PostQuitMessage(exit_code)

GetClientRect = _get_dll('user32').GetClientRect
GetClientRect.argtypes = (wintypes.HWND, ctypes.POINTER(RECT))
GetClientRect.restype = wintypes.BOOL

def get_client_rect(hwnd: int, rect: Any) -> bool:
    return GetClientRect(hwnd, rect)

DrawTextW = _get_dll('user32').DrawTextW
DrawTextW.argtypes = (wintypes.HDC, wintypes.LPCWSTR, ctypes.c_int, ctypes.POINTER(RECT), wintypes.UINT)
DrawTextW.restype = ctypes.c_int

def draw_text(hdc: int, text: str | None, count: int, rect: Any, format: int) -> int:
    return DrawTextW(hdc, text, count, rect, format)

DefWindowProcW = _get_dll('user32').DefWindowProcW
DefWindowProcW.argtypes = (wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
DefWindowProcW.restype = wintypes.LRESULT

def def_window_proc(hwnd: int, msg: int, w_param: int, l_param: int) -> Any:
    return DefWindowProcW(hwnd, msg, w_param, l_param)

GetMessageW = _get_dll('user32').GetMessageW
GetMessageW.argtypes = (ctypes.POINTER(MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT)
GetMessageW.restype = wintypes.BOOL

def get_message(msg: Any, hwnd: int, msg_filter_min: int, msg_filter_max: int) -> bool:
    return GetMessageW(msg, hwnd, msg_filter_min, msg_filter_max)

TranslateMessage = _get_dll('user32').TranslateMessage
TranslateMessage.argtypes = (ctypes.POINTER(MSG),)
TranslateMessage.restype = wintypes.BOOL

def translate_message(msg: Any) -> bool:
    return TranslateMessage(msg)

DispatchMessageW = _get_dll('user32').DispatchMessageW
DispatchMessageW.argtypes = (ctypes.POINTER(MSG),)
DispatchMessageW.restype = wintypes.LRESULT

def dispatch_message(msg: Any) -> Any:
    return DispatchMessageW(msg)

LoadIconW = _get_dll('user32').LoadIconW
LoadIconW.argtypes = (wintypes.HINSTANCE, wintypes.LPCWSTR)
LoadIconW.restype = wintypes.HICON

def load_icon(instance: int, icon_name: str | None) -> int:
    return LoadIconW(instance, icon_name)

LoadCursorW = _get_dll('user32').LoadCursorW
LoadCursorW.argtypes = (wintypes.HINSTANCE, wintypes.LPCWSTR)
LoadCursorW.restype = wintypes.HCURSOR

def load_cursor(instance: int, cursor_name: str | None) -> int:
    return LoadCursorW(instance, cursor_name)

GetStockObject = _get_dll('gdi32').GetStockObject
GetStockObject.argtypes = (ctypes.c_int,)
GetStockObject.restype = wintypes.HBRUSH

def get_stock_object(object: int) -> int:
    return GetStockObject(object)

RegisterClassExW = _get_dll('user32').RegisterClassExW
RegisterClassExW.argtypes = (ctypes.POINTER(WndClassExW),)
RegisterClassExW.restype = wintypes.ATOM

def register_class_ex(wnd_class: Any) -> int:
    return RegisterClassExW(wnd_class)

CreateWindowExW = _get_dll('user32').CreateWindowExW
CreateWindowExW.argtypes = (wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID)
CreateWindowExW.restype = wintypes.HWND

def create_window_ex(ex_style: int, class_name: str | None, window_name: str | None, style: int, x: int, y: int, width: int, height: int, parent: int, menu: int, instance: int, param: int | None) -> int:
    return CreateWindowExW(ex_style, class_name, window_name, style, x, y, width, height, parent, menu, instance, param)

UpdateWindow = _get_dll('user32').UpdateWindow
UpdateWindow.argtypes = (wintypes.HWND,)
UpdateWindow.restype = wintypes.BOOL

def update_window(hwnd: int) -> bool:
    return UpdateWindow(hwnd)

__all__ = [

	"show_window",
	"get_module_handle",
	"message_box",
	"beep",
	"set_window_text",
	"begin_paint",
	"end_paint",
	"post_quit_message",
	"get_client_rect",
	"draw_text",
	"def_window_proc",
	"get_message",
	"translate_message",
	"dispatch_message",
	"load_icon",
	"load_cursor",
	"get_stock_object",
	"register_class_ex",
	"create_window_ex",
	"update_window",
	"Point",
	"Msg",
	"PaintStruct",
	"WndClassExW",
]
