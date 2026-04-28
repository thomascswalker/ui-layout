from __future__ import annotations

from ctypes import byref, wintypes

from ui.layout import layout
from ui.platform.win32 import types, winapi
from ui.renderer import BORDER_WIDTH, DEPTH_COLORS_RGB, GenericRenderer
from ui.types import Element, Rect


def _rgb(r: int, g: int, b: int) -> int:
    return r | (g << 8) | (b << 16)


def _border_rgb(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = rgb
    return (max(0, r - 50), max(0, g - 50), max(0, b - 50))


class Win32Renderer(GenericRenderer):
    """Loads layout data and paints it with GDI when the host window calls `paint`."""

    def paint(self, hwnd: int, hdc: int) -> None:
        client = wintypes.RECT()
        winapi.get_client_rect(hwnd, client)
        w = client.right - client.left
        h = client.bottom - client.top
        if w <= 0 or h <= 0:
            return

        bg = winapi.create_solid_brush(_rgb(255, 255, 255))
        full = wintypes.RECT(0, 0, w, h)
        winapi.fill_rect(hdc, byref(full), bg)
        winapi.delete_object(bg)

        available = Rect(x=0.0, y=0.0, width=float(w), height=float(h))
        layout(self._root, available)

        winapi.set_bk_mode(hdc, int(types.BackgroundMode.TRANSPARENT))
        winapi.set_text_color(hdc, _rgb(0, 0, 0))
        self._draw_element(hdc, self._root, 0)

    def _draw_element(self, hdc: int, element: Element, level: int) -> None:
        rect = element.rect
        left = int(rect.x)
        top = int(rect.y)
        right = int(rect.x + rect.width)
        bottom = int(rect.y + rect.height)

        base = DEPTH_COLORS_RGB[level % len(DEPTH_COLORS_RGB)]
        border = _border_rgb(base)
        fill_br = winapi.create_solid_brush(_rgb(*base))
        pen = winapi.create_pen(types.PenStyle.SOLID, BORDER_WIDTH, _rgb(*border))
        old_br = winapi.select_object(hdc, fill_br)
        old_pen = winapi.select_object(hdc, pen)
        winapi.rectangle(hdc, left, top, right, bottom)
        winapi.select_object(hdc, old_br)
        winapi.select_object(hdc, old_pen)
        winapi.delete_object(fill_br)
        winapi.delete_object(pen)

        if rect.width > 50 and rect.height > 30:
            pos_text = f"{int(element.rect.x)}x, {int(element.rect.y)}y"
            size_text = f"{int(element.rect.width)}w, {int(element.rect.height)}h"
            label_text = f"{element.id} [{pos_text}], [{size_text}]"
            label_padding = 5

            label_rect = wintypes.RECT(
                int(rect.x) + label_padding,
                int(rect.y) + label_padding,
                int(rect.x + rect.width) - label_padding,
                int(rect.y + rect.height) - label_padding,
            )
            label_fmt = types.DrawTextFormat.NO_PREFIX | types.DrawTextFormat.WORD_BREAK

            winapi.draw_text(hdc, label_text, -1, byref(label_rect), label_fmt)

        for child in element.children:
            self._draw_element(hdc, child, level + 1)
