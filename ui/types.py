from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from bs4 import BeautifulSoup, Tag

from pydantic import AliasChoices, BaseModel, Field

from ui.css import parse_style

SupportsArithmetic = float | int


DEFAULT_POSITION = "static"
DEFAULT_DISPLAY = "grow"
DEFAULT_DIRECTION = "vertical"


@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0

    def __bool__(self):
        return bool(self.x) or bool(self.y)

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
class Size:
    w: float = 0.0
    h: float = 0.0

    def __bool__(self) -> bool:
        return bool(self.w) or bool(self.h)

    def __add__(self, other: Size | SupportsArithmetic) -> Size:
        if isinstance(other, SupportsArithmetic):
            return Size(self.w + other, self.h + other)
        if isinstance(other, Size):
            return Size(self.w + other.w, self.h + other.h)
        raise TypeError(f"Unsupported type for addition: {type(other)}")

    def __sub__(self, other: Size | SupportsArithmetic) -> Size:
        if isinstance(other, SupportsArithmetic):
            return Size(self.w - other, self.h - other)
        if isinstance(other, Size):
            return Size(self.w - other.w, self.h - other.h)
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

    @property
    def size(self) -> Size:
        return Size(self.width, self.height)

    @size.setter
    def size(self, new_size: Size) -> None:
        self.width = new_size.w
        self.height = new_size.h

    @property
    def position(self) -> Point:
        return Point(self.x, self.y)

    @position.setter
    def position(self, new_position: Point) -> None:
        self.x = new_position.x
        self.y = new_position.y

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


Display = Literal["grow", "fixed"]
Position = Literal["static", "relative", "absolute", "fixed"]
Direction = Literal["horizontal", "vertical"]


class Element(BaseModel):
    rect: Rect = Field(default_factory=Rect)
    fixed_rect: Rect = Field(default_factory=Rect)

    # Display and positioning
    display: Display = "grow"
    position: Position = "static"
    direction: Direction = "vertical"

    # Sizing
    padding: float = Field(
        default=0.0,
        validation_alias=AliasChoices("padding", "p"),
    )
    margin: float = Field(
        default=0.0,
        validation_alias=AliasChoices("margin", "m"),
    )
    border: float = Field(default=0.0)
    gap: float = Field(default=0.0)

    # Meta
    id: str = Field(default_factory=lambda: f"element_{id(object())}")
    children: list[Element] = Field(default_factory=list)
    parent: Element | None = None

    def fixed(self) -> Size:
        if not self.display == "fixed":
            return Size(0.0, 0.0)
        return self.fixed_rect.size

    def grow(self, available: Rect) -> Size:
        return Size(
            available.width - (self.margin * 2),
            available.height - (self.margin * 2),
        )

    def add_child(self, child: Element) -> None:
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: Element) -> None:
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    @classmethod
    def parse(cls, html_string: str | Tag) -> Element:
        """Parse an HTML string to create a tree of `Element`s."""

        if isinstance(html_string, str):
            soup = BeautifulSoup(html_string, "html.parser")
            html = soup.find()  # Get the first element
        else:
            html = html_string

        if html is None:
            raise ValueError("No valid HTML element found in the input string.")
        if not isinstance(html, Tag):
            raise ValueError("Parsed HTML is not a valid Tag element.")

        # Parse style attribute if present
        style = {}
        if style_attr := html.get("style"):
            style = parse_style(str(style_attr))

        element_id = str(html.get("id", f"element_{id(html)}"))
        display = style.get("display", DEFAULT_DISPLAY)
        position = style.get("position", DEFAULT_POSITION)
        direction = style.get("direction", DEFAULT_DIRECTION)
        padding = float(style.get("padding", 0.0))
        margin = float(style.get("margin", 0.0))
        border = float(style.get("border", 0.0))
        gap = float(style.get("gap", 0.0))

        fixed_width = float(style.get("width", 0.0))
        fixed_height = float(style.get("height", 0.0))

        element = cls(
            id=element_id,
            display=display,  # type: ignore
            position=position,  # type: ignore
            direction=direction,  # type: ignore
            padding=padding,
            margin=margin,
            border=border,
            gap=gap,
            fixed_rect=Rect(width=fixed_width, height=fixed_height),
        )

        for child_html in html.find_all(recursive=False):
            child_element = Element.parse(child_html)
            element.add_child(child_element)

        return element
