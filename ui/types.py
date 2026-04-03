from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum

SupportsArithmetic = float | int


@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: Point | SupportsArithmetic) -> Point:
        if isinstance(other, SupportsArithmetic):
            return Point(self.x + other, self.y + other)
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        raise TypeError(f"Unsupported type for addition: {type(other)}")

    def __sub__(self, other: Point | SupportsArithmetic) -> Point:
        if isinstance(other, SupportsArithmetic):
            return Point(self.x - other, self.y - other)
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        raise TypeError(f"Unsupported type for subtraction: {type(other)}")


@dataclass
class Rect:
    x: float = 0.0
    y: float = 0.0
    width: float = 1.0
    height: float = 1.0

    @property
    def center(self) -> Point:
        cx = self.x + self.width / 2.0
        cy = self.y + self.height / 2.0
        return Point(cx, cy)

    @property
    def min(self) -> Point:
        return Point(self.x, self.y)

    @property
    def max(self) -> Point:
        max_x = self.x + self.width
        max_y = self.y + self.height
        return Point(max_x, max_y)

    def __add__(self, other: Rect | SupportsArithmetic) -> Rect:
        if isinstance(other, SupportsArithmetic):
            return Rect(
                self.x + other, self.y + other, self.width + other, self.height + other
            )
        if isinstance(other, Rect):
            return Rect(
                self.x + other.x,
                self.y + other.y,
                self.width + other.width,
                self.height + other.height,
            )
        raise TypeError(f"Unsupported type for addition: {type(other)}")

    def __sub__(self, other: Rect | SupportsArithmetic) -> Rect:
        if isinstance(other, SupportsArithmetic):
            return Rect(
                self.x - other, self.y - other, self.width - other, self.height - other
            )
        if isinstance(other, Rect):
            return Rect(
                self.x - other.x,
                self.y - other.y,
                self.width - other.width,
                self.height - other.height,
            )
        raise TypeError(f"Unsupported type for subtraction: {type(other)}")


class Display(StrEnum):
    GROW = "grow"
    CONTENT = "content"
    FIXED = "fixed"


class Position(StrEnum):
    STATIC = "static"
    RELATIVE = "relative"
    ABSOLUTE = "absolute"
    FIXED = "fixed"


@dataclass(eq=True)
class Element:
    rect: Rect = field(default_factory=Rect)

    # Display and positioning
    display: Display = Display.GROW
    position: Position = Position.STATIC
    
    # Sizing
    padding: float = 0.0
    border: float = 0.0
    content_width: float = 0.0
    content_height: float = 0.0
    
    # Positioning offsets (for relative, absolute, fixed positioning)
    offset_x: float = 0.0
    offset_y: float = 0.0

    # Meta
    id: str = field(default_factory=lambda: f"element_{id(object())}")
    children: list[Element] = field(default_factory=list)
    parent: Element | None = None

    def __hash__(self) -> int:
        """Make Element hashable using its id for dictionary keys."""
        return hash(self.id)

    def add_child(self, child: Element) -> None:
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: Element) -> None:
        if child in self.children:
            self.children.remove(child)
            child.parent = None
