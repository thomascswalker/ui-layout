from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
import xml.etree.ElementTree as ET

from pydantic import AliasChoices, BaseModel, Field

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
    FIXED = "fixed"


class Position(StrEnum):
    STATIC = "static"
    RELATIVE = "relative"
    ABSOLUTE = "absolute"
    FIXED = "fixed"


class Element(BaseModel):
    rect: Rect = Field(default_factory=Rect)

    # Display and positioning
    display: Display = Display.GROW
    position: Position = Position.STATIC

    # Sizing
    padding: float = Field(default=0.0, validation_alias=AliasChoices("padding", "p"))
    border: float = Field(default=0.0)

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

    @classmethod
    def parse(cls, xml_string: str | ET.Element) -> Element:
        """Parse an XML string to create an Element tree."""

        if isinstance(xml_string, str):
            xml = ET.fromstring(xml_string)
        else:
            xml = xml_string

        elem_id = xml.get("id", f"element_{id(xml)}")
        display = Display(xml.get("display", "grow"))
        position = Position(xml.get("position", "static"))
        padding = float(xml.get("padding", 0.0))
        border = float(xml.get("border", 0.0))

        element = cls(
            id=elem_id,
            display=display,
            position=position,
            padding=padding,
            border=border,
        )

        for child_xml in xml:
            child_element = Element.parse(child_xml)
            element.add_child(child_element)

        return element
