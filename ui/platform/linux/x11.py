from __future__ import annotations

import ctypes
import ctypes.util
from typing import Any

_X11: ctypes.CDLL | None = None


def _lib() -> ctypes.CDLL:
    global _X11
    if _X11 is None:
        name = ctypes.util.find_library("X11")
        if not name:
            raise OSError(
                "Could not locate libX11 (set DISPLAY and install libX11).",
            )
        _X11 = ctypes.CDLL(name)
    return _X11


class XColor(ctypes.Structure):
    _fields_ = [
        ("pixel", ctypes.c_ulong),
        ("red", ctypes.c_ushort),
        ("green", ctypes.c_ushort),
        ("blue", ctypes.c_ushort),
        ("flags", ctypes.c_byte),
        ("pad", ctypes.c_byte),
    ]


class XCharStruct(ctypes.Structure):
    _fields_ = [
        ("lbearing", ctypes.c_short),
        ("rbearing", ctypes.c_short),
        ("width", ctypes.c_short),
        ("ascent", ctypes.c_short),
        ("descent", ctypes.c_short),
        ("attributes", ctypes.c_short),
    ]


class XFontStruct(ctypes.Structure):
    """Minimal XFontStruct layout through `descent`; sufficient for ctypes pointer access."""

    _fields_ = [
        ("ext_data", ctypes.c_void_p),
        ("fid", ctypes.c_ulong),
        ("direction", ctypes.c_uint),
        ("min_char_or_byte2", ctypes.c_uint),
        ("max_char_or_byte2", ctypes.c_uint),
        ("min_byte1", ctypes.c_uint),
        ("max_byte1", ctypes.c_uint),
        ("all_chars_exist", ctypes.c_int),
        ("default_char", ctypes.c_uint),
        ("n_properties", ctypes.c_int),
        ("properties", ctypes.c_void_p),
        ("min_bounds", XCharStruct),
        ("max_bounds", XCharStruct),
        ("per_char", ctypes.c_void_p),
        ("ascent", ctypes.c_int),
        ("descent", ctypes.c_int),
    ]


class XClientMessageEvent(ctypes.Structure):
    """Layout matches 64-bit Xlib: `format` is followed by padding before the `data` union."""

    _fields_ = [
        ("type", ctypes.c_int),
        ("serial", ctypes.c_ulong),
        ("send_event", ctypes.c_int),
        ("display", ctypes.c_void_p),
        ("window", ctypes.c_ulong),
        ("message_type", ctypes.c_ulong),
        ("format", ctypes.c_int),
        ("_pad_before_data", ctypes.c_int),
        ("data_l", ctypes.c_long * 5),
    ]


def open_display(name: bytes | None = None) -> ctypes.c_void_p:
    XOpenDisplay = _lib().XOpenDisplay
    XOpenDisplay.argtypes = (ctypes.c_char_p,)
    XOpenDisplay.restype = ctypes.c_void_p
    dpy = XOpenDisplay(name)
    if not dpy:
        raise OSError("XOpenDisplay failed (check DISPLAY).")
    return dpy


def close_display(display: ctypes.c_void_p) -> None:
    XCloseDisplay = _lib().XCloseDisplay
    XCloseDisplay.argtypes = (ctypes.c_void_p,)
    XCloseDisplay.restype = ctypes.c_int
    XCloseDisplay(display)


def default_screen(display: ctypes.c_void_p) -> int:
    fn = _lib().XDefaultScreen
    fn.argtypes = (ctypes.c_void_p,)
    fn.restype = ctypes.c_int
    return int(fn(display))


def root_window(display: ctypes.c_void_p, screen: int) -> int:
    fn = _lib().XRootWindow
    fn.argtypes = (ctypes.c_void_p, ctypes.c_int)
    fn.restype = ctypes.c_ulong
    return int(fn(display, screen))


def black_pixel(display: ctypes.c_void_p, screen: int) -> int:
    fn = _lib().XBlackPixel
    fn.argtypes = (ctypes.c_void_p, ctypes.c_int)
    fn.restype = ctypes.c_ulong
    return int(fn(display, screen))


def white_pixel(display: ctypes.c_void_p, screen: int) -> int:
    fn = _lib().XWhitePixel
    fn.argtypes = (ctypes.c_void_p, ctypes.c_int)
    fn.restype = ctypes.c_ulong
    return int(fn(display, screen))


def default_colormap(display: ctypes.c_void_p, screen: int) -> int:
    fn = _lib().XDefaultColormap
    fn.argtypes = (ctypes.c_void_p, ctypes.c_int)
    fn.restype = ctypes.c_ulong
    return int(fn(display, screen))


def create_simple_window(
    display: ctypes.c_void_p,
    parent: int,
    x: int,
    y: int,
    width: int,
    height: int,
    border_width: int,
    border_pixel: int,
    background_pixel: int,
) -> int:
    fn = _lib().XCreateSimpleWindow
    fn.argtypes = (
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_uint,
        ctypes.c_uint,
        ctypes.c_uint,
        ctypes.c_ulong,
        ctypes.c_ulong,
    )
    fn.restype = ctypes.c_ulong
    return int(
        fn(
            display,
            parent,
            x,
            y,
            width,
            height,
            border_width,
            border_pixel,
            background_pixel,
        ),
    )


def map_window(display: ctypes.c_void_p, window: int) -> None:
    fn = _lib().XMapWindow
    fn.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
    fn.restype = ctypes.c_int
    fn(display, window)


def store_name(display: ctypes.c_void_p, window: int, title: str) -> None:
    fn = _lib().XStoreName
    fn.argtypes = (ctypes.c_void_p, ctypes.c_ulong, ctypes.c_char_p)
    fn.restype = ctypes.c_int
    fn(display, window, ctypes.c_char_p(title.encode()))


def intern_atom(display: ctypes.c_void_p, name: bytes, only_if_exists: bool) -> int:
    fn = _lib().XInternAtom
    fn.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool)
    fn.restype = ctypes.c_ulong
    return int(fn(display, ctypes.c_char_p(name), only_if_exists))


def set_wm_protocols(
    display: ctypes.c_void_p, window: int, protocols: list[int]
) -> None:
    fn = _lib().XSetWMProtocols
    fn.argtypes = (
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.POINTER(ctypes.c_ulong),
        ctypes.c_int,
    )
    fn.restype = ctypes.c_int
    arr = (ctypes.c_ulong * len(protocols))(*protocols)
    fn(display, window, arr, len(protocols))


def select_input(display: ctypes.c_void_p, window: int, event_mask: int) -> None:
    fn = _lib().XSelectInput
    fn.argtypes = (ctypes.c_void_p, ctypes.c_ulong, ctypes.c_long)
    fn.restype = ctypes.c_int
    fn(display, window, event_mask)


def next_event(display: ctypes.c_void_p, event_return: Any) -> None:
    fn = _lib().XNextEvent
    fn.argtypes = (ctypes.c_void_p, ctypes.c_void_p)
    fn.restype = ctypes.c_int
    fn(display, event_return)


def flush(display: ctypes.c_void_p) -> None:
    fn = _lib().XFlush
    fn.argtypes = (ctypes.c_void_p,)
    fn.restype = ctypes.c_int
    fn(display)


def get_window_geometry(display: ctypes.c_void_p, window: int) -> tuple[int, int]:
    fn = _lib().XGetGeometry
    root = ctypes.c_ulong()
    x = ctypes.c_int()
    y = ctypes.c_int()
    width = ctypes.c_uint()
    height = ctypes.c_uint()
    border_width = ctypes.c_uint()
    depth = ctypes.c_uint()
    fn.argtypes = (
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.POINTER(ctypes.c_ulong),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_uint),
        ctypes.POINTER(ctypes.c_uint),
        ctypes.POINTER(ctypes.c_uint),
        ctypes.POINTER(ctypes.c_uint),
    )
    fn.restype = ctypes.c_int
    fn(
        display,
        window,
        ctypes.byref(root),
        ctypes.byref(x),
        ctypes.byref(y),
        ctypes.byref(width),
        ctypes.byref(height),
        ctypes.byref(border_width),
        ctypes.byref(depth),
    )
    return int(width.value), int(height.value)


def create_gc(display: ctypes.c_void_p, drawable: int) -> int:
    fn = _lib().XCreateGC
    fn.argtypes = (
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_void_p,
    )
    fn.restype = ctypes.c_ulong
    return int(fn(display, drawable, 0, None))


def free_gc(display: ctypes.c_void_p, gc: int) -> None:
    fn = _lib().XFreeGC
    fn.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
    fn.restype = ctypes.c_int
    fn(display, gc)


def set_foreground(display: ctypes.c_void_p, gc: int, pixel: int) -> None:
    fn = _lib().XSetForeground
    fn.argtypes = (ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong)
    fn.restype = ctypes.c_int
    fn(display, gc, pixel)


def set_background(display: ctypes.c_void_p, gc: int, pixel: int) -> None:
    fn = _lib().XSetBackground
    fn.argtypes = (ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong)
    fn.restype = ctypes.c_int
    fn(display, gc, pixel)


def set_line_attributes(
    display: ctypes.c_void_p,
    gc: int,
    line_width: int,
    line_style: int,
    cap_style: int,
    join_style: int,
) -> None:
    fn = _lib().XSetLineAttributes
    fn.argtypes = (
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.c_uint,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    )
    fn.restype = ctypes.c_int
    fn(display, gc, line_width, line_style, cap_style, join_style)


def fill_rectangle(
    display: ctypes.c_void_p,
    drawable: int,
    gc: int,
    x: int,
    y: int,
    width: int,
    height: int,
) -> None:
    fn = _lib().XFillRectangle
    fn.argtypes = (
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_uint,
        ctypes.c_uint,
    )
    fn.restype = ctypes.c_int
    fn(display, drawable, gc, x, y, width, height)


def draw_rectangle(
    display: ctypes.c_void_p,
    drawable: int,
    gc: int,
    x: int,
    y: int,
    width: int,
    height: int,
) -> None:
    fn = _lib().XDrawRectangle
    fn.argtypes = (
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_uint,
        ctypes.c_uint,
    )
    fn.restype = ctypes.c_int
    fn(display, drawable, gc, x, y, width, height)


def draw_string(
    display: ctypes.c_void_p,
    drawable: int,
    gc: int,
    x: int,
    y: int,
    text: bytes,
) -> None:
    fn = _lib().XDrawString
    fn.argtypes = (
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    )
    fn.restype = ctypes.c_int
    fn(display, drawable, gc, x, y, text, len(text))


def parse_color(
    display: ctypes.c_void_p, colormap: int, spec: bytes, color_out: Any
) -> bool:
    fn = _lib().XParseColor
    fn.argtypes = (
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.c_char_p,
        ctypes.c_void_p,
    )
    fn.restype = ctypes.c_int
    return bool(fn(display, colormap, ctypes.c_char_p(spec), ctypes.byref(color_out)))


def alloc_color(display: ctypes.c_void_p, colormap: int, color_in_out: Any) -> bool:
    fn = _lib().XAllocColor
    fn.argtypes = (ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p)
    fn.restype = ctypes.c_int
    return bool(fn(display, colormap, ctypes.byref(color_in_out)))


def load_query_font(display: ctypes.c_void_p, name: bytes) -> Any:
    fn = _lib().XLoadQueryFont
    fn.argtypes = (ctypes.c_void_p, ctypes.c_char_p)
    fn.restype = ctypes.POINTER(XFontStruct)
    return fn(display, ctypes.c_char_p(name))


def free_font(display: ctypes.c_void_p, font: Any) -> None:
    fn = _lib().XFreeFont
    fn.argtypes = (ctypes.c_void_p, ctypes.POINTER(XFontStruct))
    fn.restype = ctypes.c_int
    fn(display, font)


def clear_window(display: ctypes.c_void_p, window: int) -> None:
    fn = _lib().XClearWindow
    fn.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
    fn.restype = ctypes.c_int
    fn(display, window)


def set_font(display: ctypes.c_void_p, gc: int, font_id: int) -> None:
    fn = _lib().XSetFont
    fn.argtypes = (ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong)
    fn.restype = ctypes.c_int
    fn(display, gc, font_id)


def alloc_rgb_pixel(
    display: ctypes.c_void_p,
    colormap: int,
    r: int,
    g: int,
    b: int,
) -> int:
    spec = f"#{r:02x}{g:02x}{b:02x}".encode("ascii")
    color = XColor()
    if not parse_color(display, colormap, spec, color):
        raise OSError(f"XParseColor failed for {spec!r}")
    if not alloc_color(display, colormap, color):
        raise OSError(f"XAllocColor failed for {spec!r}")
    return int(color.pixel)


def event_bytes() -> int:
    return 192  # conservative; XEvent includes large client message payload


def client_message_from_buffer(
    buf: ctypes.Array[ctypes.c_byte],
) -> XClientMessageEvent:
    return ctypes.cast(
        ctypes.pointer(buf),
        ctypes.POINTER(XClientMessageEvent),
    ).contents


__all__ = [
    "XCharStruct",
    "XClientMessageEvent",
    "XColor",
    "XFontStruct",
    "alloc_color",
    "alloc_rgb_pixel",
    "clear_window",
    "client_message_from_buffer",
    "close_display",
    "create_gc",
    "create_simple_window",
    "default_colormap",
    "default_screen",
    "draw_rectangle",
    "draw_string",
    "event_bytes",
    "fill_rectangle",
    "flush",
    "free_font",
    "free_gc",
    "get_window_geometry",
    "intern_atom",
    "load_query_font",
    "map_window",
    "next_event",
    "open_display",
    "parse_color",
    "root_window",
    "select_input",
    "set_background",
    "set_font",
    "set_foreground",
    "set_line_attributes",
    "set_wm_protocols",
    "store_name",
    "black_pixel",
    "white_pixel",
]
