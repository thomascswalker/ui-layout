from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path

from ui.types import Element

logger = logging.getLogger(__name__)

MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

BORDER_WIDTH = 2

DEPTH_COLORS_RGB: list[tuple[int, int, int]] = [
    (0xEF, 0x44, 0x44),
    (0xF9, 0x9B, 0x16),
    (0xEA, 0xAD, 0x08),
    (0x22, 0xC5, 0x5E),
    (0x3B, 0x82, 0xF6),
]


def _find_file(filename: str) -> Path:
    path = Path(filename)
    if path.exists() and path.is_file():
        return path

    current_dir_path = Path.cwd()
    pattern = f"**/{filename}"
    if not pattern.endswith(".html"):
        pattern += ".html"
    html_files = list(current_dir_path.glob(pattern))
    if html_files:
        return html_files[0]

    raise FileNotFoundError(
        f"File '{filename}' not found in current directory or provided path."
    )


class GenericRenderer(ABC):
    def load_file(self, filename: str) -> None:
        logger.info(f"Initializing renderer for {filename}...")
        self.filename = filename
        path = _find_file(filename)
        self._title = path.stem
        with open(path, encoding="utf-8") as f:
            self._root = Element.parse(f.read())

    @abstractmethod
    def paint(self, hwnd: int, hdc: int) -> None:
        """Draw the layout into the given native surface."""
