from dataclasses import dataclass

SupportsArithmetic = float | int

@dataclass
class Point:
    x: float
    y: float

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
    x: float
    y: float
    width: float
    height: float

    @property
    def center(self) -> Point:
        center_x = self.x + self.width / 2.0
        center_y = self.y + self.height / 2.0
        return Point(center_x, center_y)

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
            return Rect(self.x + other, self.y + other, self.width + other, self.height + other)
        if isinstance(other, Rect):
            return Rect(self.x + other.x, self.y + other.y, self.width + other.width, self.height + other.height)
        raise TypeError(f"Unsupported type for addition: {type(other)}")
    
    def __sub__(self, other: Rect | SupportsArithmetic) -> Rect:
        if isinstance(other, SupportsArithmetic):
            return Rect(self.x - other, self.y - other, self.width - other, self.height - other)
        if isinstance(other, Rect):
            return Rect(self.x - other.x, self.y - other.y, self.width - other.width, self.height - other.height)
        raise TypeError(f"Unsupported type for subtraction: {type(other)}")


@dataclass
class Element:
    rect: Rect
