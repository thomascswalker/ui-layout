from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from bs4 import BeautifulSoup, Tag

from pydantic import AliasChoices, BaseModel, Field

SupportsArithmetic = float | int


DEFAULT_POSITION = "static"
DEFAULT_DISPLAY = "grow"
DEFAULT_DIRECTION = "vertical"


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


Display = Literal["grow", "fixed"]
Position = Literal["static", "relative", "absolute", "fixed"]
Direction = Literal["horizontal", "vertical"]


class Element(BaseModel):
    rect: Rect = Field(default_factory=Rect)

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

    def add_child(self, child: Element) -> None:
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: Element) -> None:
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    @staticmethod
    def _parse_style(style_str: str) -> dict[str, str]:
        """Parse a CSS style string into a dictionary of property-value pairs."""
        if not style_str:
            return {}

        styles = {}
        # Split by semicolon and strip whitespace
        for declaration in style_str.split(";"):
            declaration = declaration.strip()
            if ":" in declaration:
                prop, value = declaration.split(":", 1)
                styles[prop.strip()] = value.strip()
        return styles

    @classmethod
    def parse(cls, xml_string: str | Tag) -> Element:
        """Parse an HTML string to create a tree of `Element`s."""

        if isinstance(xml_string, str):
            soup = BeautifulSoup(xml_string, "html.parser")
            html = soup.find()  # Get the first element
        else:
            html = xml_string

        if html is None:
            raise ValueError("No valid HTML element found in the input string.")

        # Parse style attribute if present
        style_dict = {}
        style_attr = html.get("style")
        if style_attr:
            style_dict = cls._parse_style(str(style_attr))

        element_id = str(html.get("id", f"element_{id(html)}"))  # type: ignore

        # Get values from style or fall back to individual attributes
        display: Display = style_dict.get(
            "display", html.get("display", DEFAULT_DISPLAY)
        )  # type: ignore
        position: Position = style_dict.get(
            "position", html.get("position", DEFAULT_POSITION)
        )  # type: ignore
        direction: Direction = style_dict.get(
            "direction", html.get("direction", DEFAULT_DIRECTION)
        )  # type: ignore
        padding = float(style_dict.get("padding", html.get("padding", 0.0)))  # type: ignore
        margin = float(style_dict.get("margin", html.get("margin", 0.0)))  # type: ignore
        border = float(style_dict.get("border", html.get("border", 0.0)))  # type: ignore
        gap = float(style_dict.get("gap", html.get("gap", 0.0)))  # type: ignore

        element = cls(
            id=element_id,
            display=display,
            position=position,
            direction=direction,
            padding=padding,
            margin=margin,
            border=border,
            gap=gap,
        )

        for child_xml in html.find_all(recursive=False):
            child_element = Element.parse(child_xml)
            element.add_child(child_element)

        return element
