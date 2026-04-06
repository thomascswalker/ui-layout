import pytest

from tests.conftest import Operator
from ui.types import Point


def test_point_create():
    p = Point(1, 2)
    assert p.x == 1
    assert p.y == 2


@pytest.mark.parametrize(
    "operator, other, result",
    [
        ("+", Point(3, 4), Point(4, 6)),
        ("+", 3.0, Point(4, 5)),
        ("-", Point(3, 4), Point(-2, -2)),
        ("-", 3.0, Point(-2, -1)),
    ],
)
def test_point_arithmetic(operator: Operator, other: Point | float, result: Point):
    p1 = Point(1, 2)
    match operator:
        case "+":
            res = p1 + other
        case "-":
            res = p1 - other
        case _:
            pytest.fail(f"Unsupported operator: {operator}")
    assert res.x == result.x
    assert res.y == result.y


@pytest.mark.parametrize("operator", ["+", "-"])
def test_point_arithmetic_invalid_type(operator: Operator):
    p = Point(1, 2)
    with pytest.raises(TypeError):
        match operator:
            case "+":
                p + "invalid"  # type: ignore
            case "-":
                p - "invalid"  # type: ignore
