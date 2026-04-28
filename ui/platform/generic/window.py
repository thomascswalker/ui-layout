from __future__ import annotations

from abc import ABC, abstractmethod


class GenericWindow(ABC):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    @abstractmethod
    def show(self) -> None:
        raise NotImplementedError("`show` must be implemented.")

    @abstractmethod
    def run(self) -> int:
        raise NotImplementedError("`run` must be implemented.")
