from __future__ import annotations

from ctypes import wintypes
from typing import override

from ui.layout import layout
from ui.platform.generic.renderer import GenericRenderer
from ui.platform.win32 import types
from ui.platform.win32.winapi import (
    create_solid_brush,
    delete_object,
    draw,
    draw_text,
    fill_rect,
    get_client_rect,
    rectangle,
    set_background_mode,
    set_text_color,
)
from ui.types import RGB, Rect


class Win32Renderer(GenericRenderer):
    @override
    def paint(self, window: int, context: int) -> None:
        # Get the window client rectangle
        rect = wintypes.RECT()
        get_client_rect(window, rect)
        w = rect.right - rect.left
        h = rect.bottom - rect.top
        if w <= 0 or h <= 0:
            return

        # Fill the background with white
        bg = create_solid_brush(int(RGB.white()))
        rect = wintypes.RECT(0, 0, w, h)
        fill_rect(context, rect, bg)
        delete_object(bg)

        # Set the background mode to transparent and the text color to black
        set_background_mode(context, int(types.BackgroundMode.TRANSPARENT))
        set_text_color(context, int(RGB.black()))

        # Layout the root element and its children
        available = Rect(x=0.0, y=0.0, width=float(w), height=float(h))
        layout(self.root, available)

        # Recursively draw the root element and its children
        self.draw_element(context, self.root)

    @override
    def draw_rect(self, context: int, rect: Rect, fill: RGB, stroke: RGB) -> None:
        left = int(rect.x)
        top = int(rect.y)
        right = int(rect.x + rect.width)
        bottom = int(rect.y + rect.height)

        with draw(context, fill, stroke):
            rectangle(context, left, top, right, bottom)

    @override
    def draw_text(self, context: int, text: str, rect: Rect) -> None:
        left = int(rect.x)
        top = int(rect.y)
        right = int(rect.x + rect.width)
        bottom = int(rect.y + rect.height)

        label_rect = wintypes.RECT(left, top, right, bottom)
        label_fmt = types.DrawTextFormat.NO_PREFIX | types.DrawTextFormat.WORD_BREAK

        draw_text(context, text, -1, label_rect, label_fmt)
