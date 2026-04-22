import pytest

from ui.types import Direction, Element, Rect
from ui.layout import layout

ROOT_WIDTH = 640
ROOT_HEIGHT = 480


@pytest.fixture
def root() -> Element:
    return Element(
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
def test_layout_with_padding(root: Element, padding: int):
    root.padding = padding
    element = Element()
    root.add_child(element)
    layout(root, root.rect)

    assert element.rect.width == root.rect.width - (padding * 2)
    assert element.rect.height == root.rect.height - (padding * 2)


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


def test_layout_vertical_direction_no_gap(root: Element):
    """Test vertical direction with no gap between children."""
    root.direction = "vertical"
    child1 = Element()
    child2 = Element()
    child3 = Element()
    root.add_child(child1)
    root.add_child(child2)
    root.add_child(child3)
    layout(root, root.rect)

    # All children should have full width
    assert child1.rect.width == ROOT_WIDTH
    assert child2.rect.width == ROOT_WIDTH
    assert child3.rect.width == ROOT_WIDTH

    # Each child should have equal height
    expected_height = ROOT_HEIGHT / 3
    assert child1.rect.height == expected_height
    assert child2.rect.height == expected_height
    assert child3.rect.height == expected_height

    # Positions: child1 at top, child2 below, child3 at bottom
    assert child1.rect.x == 0
    assert child1.rect.y == 0
    assert child2.rect.x == 0
    assert child2.rect.y == expected_height
    assert child3.rect.x == 0
    assert child3.rect.y == expected_height * 2


def test_layout_vertical_direction_with_gap(root: Element):
    """Test vertical direction with gap between children."""
    root.direction = "vertical"
    root.gap = 10
    child1 = Element()
    child2 = Element()
    root.add_child(child1)
    root.add_child(child2)
    layout(root, root.rect)

    # All children should have full width
    assert child1.rect.width == ROOT_WIDTH
    assert child2.rect.width == ROOT_WIDTH

    # Total height available for children: 480 - 10 (gap) = 470, divided by 2 = 235 each
    expected_height = (ROOT_HEIGHT - root.gap) / 2
    assert child1.rect.height == expected_height
    assert child2.rect.height == expected_height

    # Positions: child1 at top, child2 below with gap
    assert child1.rect.x == 0
    assert child1.rect.y == 0
    assert child2.rect.x == 0
    assert child2.rect.y == expected_height + root.gap


def test_layout_horizontal_direction_no_gap(root: Element):
    """Test horizontal direction with no gap between children."""
    root.direction = "horizontal"
    child1 = Element()
    child2 = Element()
    child3 = Element()
    root.add_child(child1)
    root.add_child(child2)
    root.add_child(child3)
    layout(root, root.rect)

    # All children should have full height
    assert child1.rect.height == ROOT_HEIGHT
    assert child2.rect.height == ROOT_HEIGHT
    assert child3.rect.height == ROOT_HEIGHT

    # Each child should have equal width
    expected_width = ROOT_WIDTH / 3
    assert child1.rect.width == expected_width
    assert child2.rect.width == expected_width
    assert child3.rect.width == expected_width

    # Positions: child1 at left, child2 right, child3 at rightmost
    assert child1.rect.x == 0
    assert child1.rect.y == 0
    assert child2.rect.x == expected_width
    assert child2.rect.y == 0
    assert child3.rect.x == expected_width * 2
    assert child3.rect.y == 0


def test_layout_horizontal_direction_with_gap(root: Element):
    """Test horizontal direction with gap between children."""
    root.direction = "horizontal"
    root.gap = 20
    child1 = Element()
    child2 = Element()
    root.add_child(child1)
    root.add_child(child2)
    layout(root, root.rect)

    # All children should have full height
    assert child1.rect.height == ROOT_HEIGHT
    assert child2.rect.height == ROOT_HEIGHT

    # Total width available for children: 640 - 20 (gap) = 620, divided by 2 = 310 each
    expected_width = (ROOT_WIDTH - root.gap) / 2
    assert child1.rect.width == expected_width
    assert child2.rect.width == expected_width

    # Positions: child1 at left, child2 right with gap
    assert child1.rect.x == 0
    assert child1.rect.y == 0
    assert child2.rect.x == expected_width + root.gap
    assert child2.rect.y == 0


def test_layout_vertical_direction_with_padding(root: Element):
    """Test vertical direction with padding on parent."""
    root.direction = "vertical"
    root.padding = 20
    child1 = Element()
    child2 = Element()
    root.add_child(child1)
    root.add_child(child2)
    layout(root, root.rect)

    # Children should be positioned inside padding
    assert child1.rect.x == root.padding
    assert child1.rect.y == root.padding
    assert child2.rect.x == root.padding
    assert child2.rect.y == root.padding + child1.rect.height

    # Width and height should account for padding
    available_width = ROOT_WIDTH - (root.padding * 2)
    available_height = (ROOT_HEIGHT - (root.padding * 2)) / 2
    assert child1.rect.width == available_width
    assert child1.rect.height == available_height
    assert child2.rect.width == available_width
    assert child2.rect.height == available_height


def test_layout_horizontal_direction_with_padding(root: Element):
    """Test horizontal direction with padding on parent."""
    root.direction = "horizontal"
    root.padding = 15
    child1 = Element()
    child2 = Element()
    root.add_child(child1)
    root.add_child(child2)
    layout(root, root.rect)

    # Children should be positioned inside padding
    assert child1.rect.x == root.padding
    assert child1.rect.y == root.padding
    assert child2.rect.x == root.padding + child1.rect.width
    assert child2.rect.y == root.padding

    # Width and height should account for padding
    available_height = ROOT_HEIGHT - (root.padding * 2)
    available_width = (ROOT_WIDTH - (root.padding * 2)) / 2
    assert child1.rect.width == available_width
    assert child1.rect.height == available_height
    assert child2.rect.width == available_width
    assert child2.rect.height == available_height


def test_layout_mixed_directions(root: Element):
    """Test nested elements with different directions."""
    root.direction = "vertical"
    vertical_child = Element(direction="vertical")
    horizontal_child = Element(direction="horizontal")
    root.add_child(vertical_child)
    root.add_child(horizontal_child)

    # Add children to vertical_child
    v1 = Element()
    v2 = Element()
    vertical_child.add_child(v1)
    vertical_child.add_child(v2)

    # Add children to horizontal_child
    h1 = Element()
    h2 = Element()
    horizontal_child.add_child(h1)
    horizontal_child.add_child(h2)

    layout(root, root.rect)

    # Root children: vertical_child and horizontal_child each get half height
    child_height = ROOT_HEIGHT / 2
    assert vertical_child.rect.height == child_height
    assert horizontal_child.rect.height == child_height
    assert vertical_child.rect.width == ROOT_WIDTH
    assert horizontal_child.rect.width == ROOT_WIDTH

    # vertical_child's children: v1 and v2 each get half of vertical_child's height
    v_child_height = child_height / 2
    assert v1.rect.height == v_child_height
    assert v2.rect.height == v_child_height
    assert v1.rect.width == ROOT_WIDTH
    assert v2.rect.width == ROOT_WIDTH

    # Positions for vertical_child's children
    assert v1.rect.x == 0
    assert v1.rect.y == 0
    assert v2.rect.x == 0
    assert v2.rect.y == v_child_height

    # horizontal_child's children: h1 and h2 each get half of horizontal_child's width
    h_child_width = ROOT_WIDTH / 2
    assert h1.rect.width == h_child_width
    assert h2.rect.width == h_child_width
    assert h1.rect.height == child_height
    assert h2.rect.height == child_height

    # Positions for horizontal_child's children
    assert h1.rect.x == 0
    assert h1.rect.y == child_height  # Below vertical_child
    assert h2.rect.x == h_child_width
    assert h2.rect.y == child_height


@pytest.mark.parametrize(
    "direction,gap,child_count",
    [
        ("vertical", 0, 3),
        ("vertical", 10, 2),
        ("horizontal", 0, 3),
        ("horizontal", 20, 2),
    ],
)
def test_layout_direction_with_gap(
    root: Element,
    direction: Direction,
    gap: float,
    child_count: int,
):
    """Test layout direction with and without gap between children."""
    root.direction = direction
    root.gap = gap

    children = [Element() for _ in range(child_count)]
    for child in children:
        root.add_child(child)

    layout(root, root.rect)

    if direction == "vertical":
        # All children should have full width
        for child in children:
            assert child.rect.width == ROOT_WIDTH

        # Each child should have equal height
        total_gap = gap * (len(children) - 1) if len(children) > 1 else 0
        expected_height = (ROOT_HEIGHT - total_gap) / len(children)
        for child in children:
            assert child.rect.height == expected_height

        # Positions: stacked vertically
        current_y = 0
        for child in children:
            assert child.rect.x == 0
            assert child.rect.y == current_y
            current_y += child.rect.height + gap

    elif direction == "horizontal":
        # All children should have full height
        for child in children:
            assert child.rect.height == ROOT_HEIGHT

        # Each child should have equal width
        total_gap = gap * (len(children) - 1) if len(children) > 1 else 0
        expected_width = (ROOT_WIDTH - total_gap) / len(children)
        for child in children:
            assert child.rect.width == expected_width

        # Positions: side by side horizontally
        current_x = 0
        for child in children:
            assert child.rect.x == current_x
            assert child.rect.y == 0
            current_x += child.rect.width + gap
