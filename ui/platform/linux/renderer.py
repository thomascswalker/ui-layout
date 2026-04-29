from __future__ import annotations

import ctypes
from typing import Any, override

from ui.layout import layout
from ui.platform.generic.renderer import GenericRenderer
from ui.platform.linux import types as xtypes
from ui.platform.linux import x11
from ui.types import RGB, Rect


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

    @override
    def paint(self, window: int, context: int) -> None:
        display = self._display

        w, h = x11.get_window_geometry(display, window)
        if w <= 0 or h <= 0:
            return

        white = x11.white_pixel(display, self._screen)
        x11.set_foreground(display, context, white)
        x11.fill_rectangle(display, window, context, 0, 0, w, h)

        available = Rect(x=0.0, y=0.0, width=float(w), height=float(h))
        layout(self._root, available)

        black = self._pixel(0, 0, 0)
        x11.set_foreground(display, context, black)
        self.draw_element(context, self.root)
        x11.flush(display)

    @override
    def draw_rect(
        self,
        context: int,
        rect: Rect,
        fill: RGB,
        stroke: RGB,
    ) -> None:
        left = int(rect.x)
        top = int(rect.y)
        rw = max(0, int(rect.width))
        rh = max(0, int(rect.height))

        fill_px = self._pixel(fill.r, fill.g, fill.b)
        border_px = self._pixel(stroke.r, stroke.g, stroke.b)

        x11.set_foreground(self._display, context, fill_px)
        x11.fill_rectangle(self._display, self._window, context, left, top, rw, rh)

        x11.set_foreground(self._display, context, border_px)
        x11.set_line_attributes(
            self._display,
            context,
            1,
            int(xtypes.LineStyle.SOLID),
            int(xtypes.CapStyle.BUTT),
            int(xtypes.JoinStyle.MITER),
        )
        x11.draw_rectangle(self._display, self._window, context, left, top, rw, rh)

    def draw_text(self, context: int, text: str, rect: Rect) -> None:
        x11.set_foreground(self._display, context, self._pixel(0, 0, 0))
        x11.draw_string(
            self._display,
            self._window,
            context,
            int(rect.x),
            int(rect.y) + int(self._font.contents.ascent),
            text.encode("latin-1", errors="replace"),
        )
