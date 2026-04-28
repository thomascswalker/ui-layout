"""
Wrapper around the Windows API. Provides human-readable names for functions,
parameters, attributes, enums, and constants.

Some functions require pointers to structures, so these are wrapped in
`ctypes.byref()` to simplify the Python API.
"""

from __future__ import annotations

import ctypes
from contextlib import contextmanager
from ctypes import wintypes
from functools import lru_cache
from typing import Any, Generator

from ui.platform.win32 import types
from ui.types import RGB

_DLL_CACHE: dict[str, ctypes.WinDLL] = {}


@lru_cache(maxsize=4)
def _dll(name: str) -> ctypes.WinDLL:
    return ctypes.WinDLL(name, use_last_error=True)


class PaintStruct(ctypes.Structure):
    """
    Contains information for an application. This information can be used to
    paint the client area of a window owned by that application.

    https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-paintstruct
    """

    _fields_ = [
        ("hdc", wintypes.HDC),
        ("f_erase", wintypes.BOOL),
        ("rc_paint", wintypes.RECT),
        ("f_restore", wintypes.BOOL),
        ("f_inc_update", wintypes.BOOL),
        ("rgb_reserved", ctypes.c_byte * 32),
    ]

    @property
    def device_context(self) -> int:
        """
        A handle to the display device context (DC) to be used for painting.
        Alias of `hdc`.
        """
        return self.hdc  # type: ignore

    @device_context.setter
    def device_context(self, value: int) -> None:
        self.hdc = ctypes.cast(value, ctypes.c_void_p)  # type: ignore

    @property
    def erase_background(self) -> bool:
        """
        Indicates whether the background must be erased. This value is
        nonzero if the application should erase the background. The application
        is responsible for erasing the background if a window class is created
        without a background brush. For more information, see the description
        of the hbrBackground member of the WNDCLASS structure.

        Alias of `fErase`.
        """
        return self.f_erase

    @erase_background.setter
    def erase_background(self, value: bool) -> None:
        self.f_erase = ctypes.cast(value, ctypes.c_bool)  # type: ignore

    @property
    def rect(self) -> wintypes.RECT:
        """
        A RECT structure that specifies the upper left and lower right
        corners of the rectangle in which the painting is requested, in device
        units relative to the upper-left corner of the client area.

        Alias of `rcPaint`.
        """
        return self.rc_paint

    @rect.setter
    def rect(self, value: wintypes.RECT) -> None:
        self.rc_paint = value


class WndClassExW(ctypes.Structure):
    _fields_ = [
        ("cb_size", wintypes.UINT),
        ("style", wintypes.UINT),
        ("lpfn_wnd_proc", ctypes.c_void_p),
        ("cb_cls_extra", wintypes.INT),
        ("cb_wnd_extra", wintypes.INT),
        ("h_instance", wintypes.HINSTANCE),
        ("h_icon", wintypes.HICON),
        ("h_cursor", wintypes.HCURSOR),
        ("hbr_background", wintypes.HBRUSH),
        ("lpsz_menu_name", wintypes.LPCWSTR),
        ("lpsz_class_name", wintypes.LPCWSTR),
        ("h_icon_sm", wintypes.HICON),
    ]


ShowWindow = _dll("user32").ShowWindow
ShowWindow.argtypes = (wintypes.HWND, wintypes.INT)
ShowWindow.restype = wintypes.BOOL


def show_window(hwnd: int, flags: int) -> bool:
    return ShowWindow(hwnd, flags)


GetModuleHandleW = _dll("kernel32").GetModuleHandleW
GetModuleHandleW.argtypes = (wintypes.LPCWSTR,)
GetModuleHandleW.restype = wintypes.HMODULE


def get_module_handle(module_name: str | None) -> int:
    return GetModuleHandleW(module_name)


MessageBoxW = _dll("user32").MessageBoxW
MessageBoxW.argtypes = (
    wintypes.HWND,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.UINT,
)
MessageBoxW.restype = wintypes.INT


def message_box(hwnd: int, text: str | None, caption: str | None, type: int) -> int:
    return MessageBoxW(hwnd, text, caption, type)


Beep = _dll("kernel32").Beep
Beep.argtypes = (wintypes.DWORD, wintypes.DWORD)
Beep.restype = wintypes.BOOL


def beep(frequency: int, duration: int) -> bool:
    return Beep(frequency, duration)


SetWindowTextW = _dll("user32").SetWindowTextW
SetWindowTextW.argtypes = (wintypes.HWND, wintypes.LPCWSTR)
SetWindowTextW.restype = wintypes.BOOL


def set_window_text(hwnd: int, text: str | None) -> bool:
    return SetWindowTextW(hwnd, text)


BeginPaint = _dll("user32").BeginPaint
BeginPaint.argtypes = (wintypes.HWND, ctypes.POINTER(PaintStruct))
BeginPaint.restype = wintypes.HDC


def begin_paint(hwnd: int, paint_struct: PaintStruct) -> int:
    return BeginPaint(hwnd, ctypes.byref(paint_struct))


EndPaint = _dll("user32").EndPaint
EndPaint.argtypes = (wintypes.HWND, ctypes.POINTER(PaintStruct))
EndPaint.restype = wintypes.BOOL


def end_paint(hwnd: int, paint_struct: PaintStruct) -> bool:
    return EndPaint(hwnd, ctypes.byref(paint_struct))


PostQuitMessage = _dll("user32").PostQuitMessage
PostQuitMessage.argtypes = (wintypes.INT,)
PostQuitMessage.restype = None


def post_quit_message(exit_code: int) -> Any:
    return PostQuitMessage(exit_code)


GetClientRect = _dll("user32").GetClientRect
GetClientRect.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.RECT))
GetClientRect.restype = wintypes.BOOL


def get_client_rect(hwnd: int, rect: Any) -> bool:
    return GetClientRect(hwnd, rect)


DrawTextW = _dll("user32").DrawTextW
DrawTextW.argtypes = (
    wintypes.HDC,
    wintypes.LPCWSTR,
    wintypes.INT,
    ctypes.POINTER(wintypes.RECT),
    wintypes.UINT,
)
DrawTextW.restype = wintypes.INT


def draw_text(
    hdc: int, text: str | None, count: int, rect: wintypes.RECT, format: int
) -> int:
    return DrawTextW(hdc, text, count, ctypes.byref(rect), format)


DefWindowProcW = _dll("user32").DefWindowProcW
DefWindowProcW.argtypes = (
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)
DefWindowProcW.restype = ctypes.c_uint64


def def_window_proc(hwnd: int, msg: int, w_param: int, l_param: int) -> Any:
    return DefWindowProcW(hwnd, msg, w_param, l_param)


GetMessageW = _dll("user32").GetMessageW
GetMessageW.argtypes = (
    ctypes.POINTER(wintypes.MSG),
    wintypes.HWND,
    wintypes.UINT,
    wintypes.UINT,
)
GetMessageW.restype = wintypes.INT


def get_message(msg: Any, hwnd: int, msg_filter_min: int, msg_filter_max: int) -> int:
    return GetMessageW(msg, hwnd, msg_filter_min, msg_filter_max)


TranslateMessage = _dll("user32").TranslateMessage
TranslateMessage.argtypes = (ctypes.POINTER(wintypes.MSG),)
TranslateMessage.restype = wintypes.BOOL


def translate_message(msg: Any) -> bool:
    return TranslateMessage(msg)


DispatchMessageW = _dll("user32").DispatchMessageW
DispatchMessageW.argtypes = (ctypes.POINTER(wintypes.MSG),)
DispatchMessageW.restype = ctypes.c_uint64


def dispatch_message(msg: Any) -> Any:
    return DispatchMessageW(msg)


LoadIconW = _dll("user32").LoadIconW
LoadIconW.argtypes = (wintypes.HINSTANCE, wintypes.LPCWSTR)
LoadIconW.restype = wintypes.HICON


def load_icon(instance: int, icon_name: str | None) -> int:
    return LoadIconW(instance, icon_name)


LoadCursorW = _dll("user32").LoadCursorW
LoadCursorW.argtypes = (wintypes.HINSTANCE, wintypes.LPCWSTR)
LoadCursorW.restype = wintypes.HCURSOR


def load_cursor(instance: int, cursor_name: str | None) -> int:
    return LoadCursorW(instance, cursor_name)


GetStockObject = _dll("gdi32").GetStockObject
GetStockObject.argtypes = (wintypes.INT,)
GetStockObject.restype = wintypes.HBRUSH


def get_stock_object(object: int) -> int:
    return GetStockObject(object)


RegisterClassExW = _dll("user32").RegisterClassExW
RegisterClassExW.argtypes = (ctypes.POINTER(WndClassExW),)
RegisterClassExW.restype = wintypes.ATOM


def register_class_ex(wnd_class: Any) -> int:
    return RegisterClassExW(wnd_class)


CreateWindowExW = _dll("user32").CreateWindowExW
CreateWindowExW.argtypes = (
    wintypes.DWORD,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.INT,
    wintypes.INT,
    wintypes.INT,
    wintypes.INT,
    wintypes.HWND,
    wintypes.HMENU,
    wintypes.HINSTANCE,
    wintypes.LPVOID,
)
CreateWindowExW.restype = wintypes.HWND


def create_window_ex(
    ex_style: int,
    class_name: str | None,
    window_name: str | None,
    style: int,
    x: int,
    y: int,
    width: int,
    height: int,
    parent: int,
    menu: int,
    instance: int,
    param: int | None,
) -> int:
    return CreateWindowExW(
        ex_style,
        class_name,
        window_name,
        style,
        x,
        y,
        width,
        height,
        parent,
        menu,
        instance,
        param,
    )


UpdateWindow = _dll("user32").UpdateWindow
UpdateWindow.argtypes = (wintypes.HWND,)
UpdateWindow.restype = wintypes.BOOL


def update_window(hwnd: int) -> bool:
    return UpdateWindow(hwnd)


CreateSolidBrush = _dll("gdi32").CreateSolidBrush
CreateSolidBrush.argtypes = (wintypes.COLORREF,)
CreateSolidBrush.restype = wintypes.HBRUSH


def create_solid_brush(color: int) -> int:
    return CreateSolidBrush(color)


CreatePen = _dll("gdi32").CreatePen
CreatePen.argtypes = (wintypes.INT, wintypes.INT, wintypes.COLORREF)
CreatePen.restype = wintypes.HPEN


def create_pen(style: int, width: int, color: int) -> int:
    return CreatePen(style, width, color)


SelectObject = _dll("gdi32").SelectObject
SelectObject.argtypes = (wintypes.HDC, wintypes.HGDIOBJ)
SelectObject.restype = wintypes.HGDIOBJ


def select_object(hdc: int, obj: int) -> int:
    return SelectObject(hdc, obj)


DeleteObject = _dll("gdi32").DeleteObject
DeleteObject.argtypes = (wintypes.HGDIOBJ,)
DeleteObject.restype = wintypes.BOOL


def delete_object(obj: int) -> bool:
    return DeleteObject(obj)


Rectangle = _dll("gdi32").Rectangle
Rectangle.argtypes = (
    wintypes.HDC,
    wintypes.INT,
    wintypes.INT,
    wintypes.INT,
    wintypes.INT,
)
Rectangle.restype = wintypes.BOOL


def rectangle(
    hdc: int,
    left: int,
    top: int,
    right: int,
    bottom: int,
) -> bool:
    return Rectangle(hdc, left, top, right, bottom)


SetTextColor = _dll("gdi32").SetTextColor
SetTextColor.argtypes = (wintypes.HDC, wintypes.COLORREF)
SetTextColor.restype = wintypes.COLORREF


def set_text_color(hdc: int, color: int) -> int:
    return SetTextColor(hdc, color)


SetBkMode = _dll("gdi32").SetBkMode
SetBkMode.argtypes = (wintypes.HDC, wintypes.INT)
SetBkMode.restype = wintypes.INT


def set_bk_mode(hdc: int, mode: int) -> int:
    return SetBkMode(hdc, mode)


InvalidateRect = _dll("user32").InvalidateRect
InvalidateRect.argtypes = (
    wintypes.HWND,
    ctypes.POINTER(wintypes.RECT),
    wintypes.BOOL,
)
InvalidateRect.restype = wintypes.BOOL


def invalidate_rect(hwnd: int, rect: wintypes.RECT | None, erase: bool) -> bool:
    return InvalidateRect(hwnd, ctypes.byref(rect) if rect else None, erase)


FillRect = _dll("user32").FillRect
FillRect.argtypes = (wintypes.HDC, ctypes.POINTER(wintypes.RECT), wintypes.HBRUSH)
FillRect.restype = wintypes.INT


def fill_rect(hdc: int, rect: wintypes.RECT, brush: int) -> int:
    return FillRect(hdc, ctypes.byref(rect), brush)


@contextmanager
def paint(hwnd: int) -> Generator[PaintStruct, None, None]:
    """
    Context manager for painting a window's client area.

    BeginPaint returns an HDC and fills ``ps``; EndPaint must receive the same
    window handle as BeginPaint, not the device context.

    Args:
        hwnd: Window handle passed to BeginPaint / EndPaint.
    """
    ps = PaintStruct()
    begin_paint(hwnd, ps)
    try:
        yield ps
    finally:
        end_paint(hwnd, ps)


@contextmanager
def draw(
    hdc: int,
    fill: RGB,
    stroke: RGB,
    width: int = 1,
) -> Generator[None, None, None]:
    """
    Context manager for drawing with GDI objects.

    Args:
        hdc: The device context to draw on.
        fill: The fill color.
        stroke: The stroke color.
        width: The width of the stroke.
    """
    brush_obj = create_solid_brush(fill.r | (fill.g << 8) | (fill.b << 16))
    pen_obj = create_pen(
        types.PenStyle.SOLID,
        width,
        stroke.r | (stroke.g << 8) | (stroke.b << 16),
    )
    old_br = select_object(hdc, brush_obj)
    old_pen = select_object(hdc, pen_obj)
    try:
        yield
    finally:
        select_object(hdc, old_br)
        select_object(hdc, old_pen)
        delete_object(brush_obj)
        delete_object(pen_obj)


__all__ = [
    "beep",
    "begin_paint",
    "create_pen",
    "create_solid_brush",
    "create_window_ex",
    "def_window_proc",
    "delete_object",
    "dispatch_message",
    "draw_text",
    "draw",
    "end_paint",
    "fill_rect",
    "get_client_rect",
    "get_message",
    "get_module_handle",
    "get_stock_object",
    "invalidate_rect",
    "load_cursor",
    "load_icon",
    "message_box",
    "paint",
    "PaintStruct",
    "post_quit_message",
    "rectangle",
    "register_class_ex",
    "select_object",
    "set_bk_mode",
    "set_text_color",
    "set_window_text",
    "show_window",
    "translate_message",
    "update_window",
    "WndClassExW",
]
