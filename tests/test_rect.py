import pytest

from tests.conftest import Operator
from ui.types import Rect, Point


def test_rect_create():
    rect = Rect(10, 20, 100, 200)
    assert rect.x == 10
    assert rect.y == 20
    assert rect.width == 100
    assert rect.height == 200


def test_rect_min_max():
    rect = Rect(10, 20, 100, 200)
    min_point = rect.min
    assert isinstance(min_point, Point)
    max_point = rect.max
    assert isinstance(max_point, Point)
    assert min_point.x == 10
    assert min_point.y == 20
    assert max_point.x == 110
    assert max_point.y == 220


def test_rect_center():
    rect = Rect(10, 20, 100, 200)
    center_point = rect.center
    assert isinstance(center_point, Point)
    assert center_point.x == 60
    assert center_point.y == 120


@pytest.mark.parametrize(
    "operator, other, result",
    [
        ("+", Rect(5, 5, 50, 50), Rect(15, 25, 150, 250)),
        ("+", 5.0, Rect(15, 25, 105, 205)),
        ("-", Rect(5, 5, 50, 50), Rect(5, 15, 50, 150)),
        ("-", 5.0, Rect(5, 15, 95, 195)),
    ],
)
def test_rect_arithmetic(operator: Operator, other: Rect | float, result: Rect):
    rect1 = Rect(10, 20, 100, 200)
    match operator:
        case "+":
            res = rect1 + other
        case "-":
            res = rect1 - other
        case _:
            pytest.fail(f"Unsupported operator: {operator}")
    assert res.x == result.x
    assert res.y == result.y
    assert res.width == result.width
    assert res.height == result.height


@pytest.mark.parametrize("operator", ["+", "-"])
def test_rect_arithmetic_invalid_type(operator: Operator):
    rect = Rect(10, 20, 100, 200)
    with pytest.raises(TypeError):
        match operator:
            case "+":
                rect + "invalid"  # type: ignore
            case "-":
                rect - "invalid"  # type: ignore
