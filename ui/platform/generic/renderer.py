from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import final

from ui.types import RGB, Element
from ui.util import find_file

logger = logging.getLogger(__name__)

DEPTH_COLORS_RGB: list[RGB] = [
    RGB(0xEF, 0x44, 0x44),
    RGB(0xF9, 0x9B, 0x16),
    RGB(0xEA, 0xAD, 0x08),
    RGB(0x22, 0xC5, 0x5E),
    RGB(0x3B, 0x82, 0xF6),
]


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
    def draw_element_label(self, context: int, element: Element) -> None:
        raise NotImplementedError("`draw_element_label` must be implemented.")

    @abstractmethod
    def draw_element(self, context: int, element: Element, level: int = 0) -> None:
        raise NotImplementedError("`draw_element` must be implemented.")
