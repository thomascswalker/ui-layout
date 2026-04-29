from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import final

from ui.types import RGB, Element, Rect
from ui.util import find_file

logger = logging.getLogger(__name__)

DEPTH_COLORS_RGB: list[RGB] = [
    RGB(0xEF, 0x44, 0x44),  # Red
    RGB(0xF9, 0x9B, 0x16),  # Orange
    RGB(0xEA, 0xAD, 0x08),  # Yellow
    RGB(0x22, 0xC5, 0x5E),  # Green
    RGB(0x3B, 0x82, 0xF6),  # Blue
]
LABEL_PADDING = 5


class GenericRenderer(ABC):
    @final
    def load_file(self, filename: str) -> None:
        logger.info(f"Initializing renderer for {filename}...")
        self.filename = filename
        path = find_file(filename)
        with open(path, encoding="utf-8") as f:
            self._root = Element.parse(f.read())

    @property
    def root(self) -> Element:
        """The root element of the layout."""
        return self._root

    @abstractmethod
    def paint(self, window: int, context: int) -> None:
        raise NotImplementedError("`paint` must be implemented.")

    @abstractmethod
    def draw_rect(self, context: int, rect: Rect, fill: RGB, stroke: RGB) -> None:
        raise NotImplementedError("`draw_rect` must be implemented.")

    @abstractmethod
    def draw_text(self, context: int, text: str, rect: Rect) -> None:
        raise NotImplementedError("`draw_text` must be implemented.")

    @final
    def draw_element(self, context: int, element: Element, level: int = 0) -> None:
        rect = element.rect
        fill = DEPTH_COLORS_RGB[level % len(DEPTH_COLORS_RGB)]
        stroke = fill - RGB(50, 50, 50)

        self.draw_rect(context, rect, fill, stroke)

        # Draw the element's label if it's large enough to fit it
        if rect.width > 50 and rect.height > 30:
            pos_text = f"{int(element.rect.x)}x, {int(element.rect.y)}y"
            size_text = f"{int(element.rect.width)}w, {int(element.rect.height)}h"
            label_text = f"{element.id} [{pos_text}], [{size_text}]"
            label_rect = element.rect.shrink(LABEL_PADDING, LABEL_PADDING)

            self.draw_text(
                context,
                label_text,
                label_rect,
            )

        for child in element.children:
            self.draw_element(context, child, level + 1)
