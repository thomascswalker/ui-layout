import pytest

from ui.types import Element, Rect, Display
from ui.layout import layout

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


@pytest.mark.parametrize("padding", range(0, 25, 5))
def test_layout_with_padding(root: Element, padding: float):
    element = Element(padding=padding)
    root.add_child(element)
    layout(root, root.rect)

    assert element.rect.width == ROOT_WIDTH - (2 * padding)
    assert element.rect.height == ROOT_HEIGHT - (2 * padding)


@pytest.mark.parametrize("depth", range(1, 4))
@pytest.mark.parametrize("padding", range(0, 25, 5))
def test_layout_nested_elements(root: Element, depth: int, padding: float):
    """Test that nested elements to N depth with padding are sized correctly."""

    top_parent = Element(padding=padding)
    parent = top_parent
    for _ in range(depth - 1):
        child = Element(padding=padding)
        parent.add_child(child)
        parent = child
    root.add_child(top_parent)

    layout(root, root.rect)

    padding2 = padding * 2
    current_parent = top_parent
    for _ in range(depth - 1):
        current_child = current_parent.children[0]
        assert current_child.rect.width == current_parent.rect.width - padding2
        assert current_child.rect.height == current_parent.rect.height - padding2
        current_parent = current_child
