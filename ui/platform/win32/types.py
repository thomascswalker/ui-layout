import ctypes
from ctypes import wintypes
from enum import IntEnum

WNDPROC = ctypes.WINFUNCTYPE(
    ctypes.c_uint64,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)


class WindowsMessage(IntEnum):
    DESTROY = 2
    PAINT = 15
    SIZE = 5


class IconType(IntEnum):
    APPLICATION = 32512
    ERROR = 32513
    QUESTION = 32514
    WARNING = 32515
    INFORMATION = 32516
    WINLOGO = 32517
    SHIELD = 32518


class WindowStyle(IntEnum):
    OVERLAPPED = 0x00000000
    CAPTION = 0x00C00000
    SYS_MENU = 0x00080000
    THICK_FRAME = 0x00040000
    MINIMIZE_BOX = 0x00020000
    MAXIMIZE_BOX = 0x00010000

    OVERLAPPED_WINDOW = (
        OVERLAPPED | CAPTION | SYS_MENU | THICK_FRAME | MINIMIZE_BOX | MAXIMIZE_BOX
    )


class ClassStyle(IntEnum):
    V_REDRAW = 1
    H_REDRAW = 2


class SystemCursor(IntEnum):
    ARROW = 32512


class StockBrush(IntEnum):
    WHITE = 0


class ShowWindowCommand(IntEnum):
    SHOW_NORMAL = 1


class DrawTextFormat(IntEnum):
    SINGLE_LINE = 32
    CENTER = 1
    V_CENTER = 4
    NO_PREFIX = 0x800
    WORD_BREAK = 0x10


class PenStyle(IntEnum):
    SOLID = 0


class BackgroundMode(IntEnum):
    TRANSPARENT = 1
    OPAQUE = 2


class SystemIcon(IntEnum):
    APPLICATION = 32512
