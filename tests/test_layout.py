import pytest

from ui.types import Element, Rect, Display, Position, Point
from ui.layout import layout, size, position

ROOT_WIDTH = 640
ROOT_HEIGHT = 480


@pytest.fixture
def root() -> Element:
    return Element(
        display=Display.FIXED,
        padding=0,
        border=0,
        rect=Rect(
            x=0,
            y=0,
            width=ROOT_WIDTH,
            height=ROOT_HEIGHT,
        ),
    )


def test_layout_basic_sizing(root: Element):
    element = Element()
    root.add_child(element)
    layout(root, root.rect)

    assert element.rect.width == ROOT_WIDTH
    assert element.rect.height == ROOT_HEIGHT


def test_layout_with_padding(root: Element):
    element = Element(padding=10)
    root.add_child(element)
    layout(root, root.rect)

    assert element.rect.width == ROOT_WIDTH - 20
    assert element.rect.height == ROOT_HEIGHT - 20
