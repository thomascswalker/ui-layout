from __future__ import annotations

import ctypes
from typing import Any

from ui.layout import layout
from ui.platform.linux import types as xtypes
from ui.platform.linux import x11
from ui.renderer import BORDER_WIDTH, DEPTH_COLORS_RGB, GenericRenderer
from ui.types import Element, Rect


def _border_rgb(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = rgb
    return (max(0, r - 50), max(0, g - 50), max(0, b - 50))


class LinuxRenderer(GenericRenderer):
    """Loads layout data and paints it with X11 when the host window calls `paint`."""

    def __init__(self) -> None:
        self._color_cache: dict[tuple[int, int, int], int] = {}
        self._display: ctypes.c_void_p = ctypes.c_void_p(None)
        self._screen: int = 0
        self._window: int = 0
        self._gc: int = 0
        self._colormap: int = 0
        self._font: Any = None

    def bind(
        self,
        display: ctypes.c_void_p,
        screen: int,
        window: int,
        gc: int,
        font: Any,
    ) -> None:
        self._display = display
        self._screen = screen
        self._window = window
        self._gc = gc
        self._font = font
        self._colormap = x11.default_colormap(display, screen)

    def _pixel(self, r: int, g: int, b: int) -> int:
        key = (r, g, b)
        if key not in self._color_cache:
            self._color_cache[key] = x11.alloc_rgb_pixel(
                self._display,
                self._colormap,
                r,
                g,
                b,
            )
        return self._color_cache[key]

    def paint(self, hwnd: int, hdc: int) -> None:
        display = self._display
        window = hwnd
        gc = hdc

        w, h = x11.get_window_geometry(display, window)
        if w <= 0 or h <= 0:
            return

        white = x11.white_pixel(display, self._screen)
        x11.set_foreground(display, gc, white)
        x11.fill_rectangle(display, window, gc, 0, 0, w, h)

        available = Rect(x=0.0, y=0.0, width=float(w), height=float(h))
        layout(self._root, available)

        black = self._pixel(0, 0, 0)
        x11.set_foreground(display, gc, black)
        self._draw_element(display, window, gc, self._root, 0)
        x11.flush(display)

    def _draw_element(
        self,
        display: ctypes.c_void_p,
        window: int,
        gc: int,
        element: Element,
        level: int,
    ) -> None:
        rect = element.rect
        left = int(rect.x)
        top = int(rect.y)
        rw = max(0, int(rect.width))
        rh = max(0, int(rect.height))

        base = DEPTH_COLORS_RGB[level % len(DEPTH_COLORS_RGB)]
        border = _border_rgb(base)

        fill_px = self._pixel(*base)
        border_px = self._pixel(*border)

        x11.set_foreground(display, gc, fill_px)
        x11.fill_rectangle(display, window, gc, left, top, rw, rh)

        x11.set_foreground(display, gc, border_px)
        x11.set_line_attributes(
            display,
            gc,
            BORDER_WIDTH,
            int(xtypes.LineStyle.SOLID),
            int(xtypes.CapStyle.BUTT),
            int(xtypes.JoinStyle.MITER),
        )
        x11.draw_rectangle(display, window, gc, left, top, rw, rh)

        if self._font is not None and rect.width > 50 and rect.height > 30:
            pos_text = f"{int(element.rect.x)}x, {int(element.rect.y)}y"
            size_text = f"{int(element.rect.width)}w, {int(element.rect.height)}h"
            label_text = f"{element.id} [{pos_text}], [{size_text}]"
            label_padding = 5

            baseline_y = int(rect.y) + label_padding + int(self._font.contents.ascent)

            label_bytes = label_text.encode("latin-1", errors="replace")
            x11.set_foreground(display, gc, self._pixel(0, 0, 0))
            x11.draw_string(
                display,
                window,
                gc,
                int(rect.x) + label_padding,
                baseline_y,
                label_bytes,
            )

        for child in element.children:
            self._draw_element(display, window, gc, child, level + 1)
