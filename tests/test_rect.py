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

def test_rect_addition():
    rect1 = Rect(10, 20, 100, 200)
    rect2 = Rect(5, 5, 50, 50)
    result = rect1 + rect2
    assert result.x == 15
    assert result.y == 25
    assert result.width == 150
    assert result.height == 250

def test_rect_subtraction():
    rect1 = Rect(10, 20, 100, 200)
    rect2 = Rect(5, 5, 50, 50)
    result = rect1 - rect2
    assert result.x == 5
    assert result.y == 15
    assert result.width == 50
    assert result.height == 150