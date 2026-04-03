from ui.types import Point


def test_point_creation():
    p = Point(1, 2)
    assert p.x == 1
    assert p.y == 2


def test_point_addition():
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    result = p1 + p2
    assert result.x == 4
    assert result.y == 6


def test_point_subtraction():
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    result = p1 - p2
    assert result.x == -2
    assert result.y == -2


def test_point_addition_with_scalar():
    p = Point(1, 2)
    result = p + 3
    assert result.x == 4
    assert result.y == 5


def test_point_subtraction_with_scalar():
    p = Point(1, 2)
    result = p - 3
    assert result.x == -2
    assert result.y == -1
