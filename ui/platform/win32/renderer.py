from __future__ import annotations

from ctypes import wintypes
from typing import override

from ui.layout import layout
from ui.platform.generic.renderer import DEPTH_COLORS_RGB, GenericRenderer
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
from ui.types import RGB, Element, Rect


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
    def draw_element(self, context: int, element: Element, level: int = 0) -> None:
        rect = element.rect
        left = int(rect.x)
        top = int(rect.y)
        right = int(rect.x + rect.width)
        bottom = int(rect.y + rect.height)

        fill = DEPTH_COLORS_RGB[level % len(DEPTH_COLORS_RGB)]
        stroke = fill - RGB(50, 50, 50)

        with draw(context, fill, stroke):
            rectangle(context, left, top, right, bottom)

        if rect.width > 50 and rect.height > 30:
            self.draw_element_label(context, element)

        for child in element.children:
            self.draw_element(context, child, level + 1)

    @override
    def draw_element_label(self, context: int, element: Element) -> None:
        pos_text = f"{int(element.rect.x)}x, {int(element.rect.y)}y"
        size_text = f"{int(element.rect.width)}w, {int(element.rect.height)}h"
        label_text = f"{element.id} [{pos_text}], [{size_text}]"
        label_padding = 5

        rect = element.rect
        label_rect = wintypes.RECT(
            int(rect.x) + label_padding,
            int(rect.y) + label_padding,
            int(rect.x + rect.width) - label_padding,
            int(rect.y + rect.height) - label_padding,
        )
        label_fmt = types.DrawTextFormat.NO_PREFIX | types.DrawTextFormat.WORD_BREAK

        draw_text(context, label_text, -1, label_rect, label_fmt)
