from __future__ import annotations

from abc import ABC, abstractmethod

from ui.platform.generic.constants import (
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_X,
    DEFAULT_Y,
)


class GenericWindow(ABC):
    def __init__(
        self,
        filename: str,
        *,
        width: int | None = None,
        height: int | None = None,
        x: int | None = None,
        y: int | None = None,
    ) -> None:
        self.filename = filename
        self.width = width if width is not None else DEFAULT_WINDOW_WIDTH
        self.height = height if height is not None else DEFAULT_WINDOW_HEIGHT
        self.x = x if x is not None else DEFAULT_X
        self.y = y if y is not None else DEFAULT_Y

    @abstractmethod
    def show(self) -> None:
        raise NotImplementedError("`show` must be implemented.")

    @abstractmethod
    def run(self) -> int:
        raise NotImplementedError("`run` must be implemented.")
