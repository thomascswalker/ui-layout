from ui.types import Element, Rect, Display, Position, Point
from ui.layout import layout, size, position


def test_layout_basic_sizing():
    """Test that basic sizing works correctly."""
    element = Element(
        display=Display.CONTENT,
        content_width=100,
        content_height=50,
        padding=5,
        border=2
    )

    size(element)

    # CONTENT display: width/height = content + padding + border
    expected_width = 100 + (5 * 2) + (2 * 2)  # 114
    expected_height = 50 + (5 * 2) + (2 * 2)  # 64

    assert element.rect.width == expected_width, f"Expected width {expected_width}, got {element.rect.width}"
    assert element.rect.height == expected_height, f"Expected height {expected_height}, got {element.rect.height}"


def test_layout_explicit_sizing():
    """Test that explicit width/height overrides content sizing."""
    element = Element(
        display=Display.CONTENT,
        content_width=50,
        content_height=25,
        padding=5,
        border=2
    )
    # Set explicit width/height by setting rect dimensions (non-default values)
    element.rect.width = 200
    element.rect.height = 100

    size(element)

    # Explicit sizing: width/height = explicit + padding + border
    expected_width = 200 + (5 * 2) + (2 * 2)  # 214
    expected_height = 100 + (5 * 2) + (2 * 2)  # 114

    assert element.rect.width == expected_width, f"Expected width {expected_width}, got {element.rect.width}"
    assert element.rect.height == expected_height, f"Expected height {expected_height}, got {element.rect.height}"


def test_layout_grow_display():
    """Test GROW display type (height grows based on content)."""
    element = Element(
        display=Display.GROW,
        content_width=100,
        content_height=50,
        padding=5,
        border=2
    )

    size(element)

    # GROW display: width uses content, height uses content
    expected_width = 100 + (5 * 2) + (2 * 2)  # 114
    expected_height = 50 + (5 * 2) + (2 * 2)  # 64

    assert element.rect.width == expected_width, f"Expected width {expected_width}, got {element.rect.width}"
    assert element.rect.height == expected_height, f"Expected height {expected_height}, got {element.rect.height}"


def test_layout_positioning_static():
    """Test static positioning."""
    element = Element(position=Position.STATIC)
    origin = Point(10, 20)

    position(element, origin)

    assert element.rect.x == 10, f"Expected x=10, got {element.rect.x}"
    assert element.rect.y == 20, f"Expected y=20, got {element.rect.y}"


def test_layout_positioning_relative():
    """Test relative positioning."""
    element = Element(
        position=Position.RELATIVE,
        offset_x=5,
        offset_y=10
    )
    origin = Point(10, 20)

    position(element, origin)

    assert element.rect.x == 15, f"Expected x=15, got {element.rect.x}"
    assert element.rect.y == 30, f"Expected y=30, got {element.rect.y}"


def test_layout_positioning_absolute():
    """Test absolute positioning."""
    element = Element(
        position=Position.ABSOLUTE,
        offset_x=50,
        offset_y=75
    )
    origin = Point(10, 20)

    position(element, origin)

    assert element.rect.x == 60, f"Expected x=60, got {element.rect.x}"
    assert element.rect.y == 95, f"Expected y=95, got {element.rect.y}"


def test_layout_positioning_fixed():
    """Test fixed positioning."""
    element = Element(
        position=Position.FIXED,
        offset_x=100,
        offset_y=200
    )
    origin = Point(10, 20)

    position(element, origin)

    # Fixed positioning ignores origin and uses absolute coordinates
    assert element.rect.x == 100, f"Expected x=100, got {element.rect.x}"
    assert element.rect.y == 200, f"Expected y=200, got {element.rect.y}"


def test_layout_nested_elements():
    """Test layout of nested elements with static positioning."""
    # Create parent
    parent = Element(
        display=Display.CONTENT,
        content_width=200,
        content_height=100,
        padding=5,
        border=2
    )

    # Create child
    child = Element(
        display=Display.CONTENT,
        content_width=50,
        content_height=30,
        padding=3,
        border=1
    )

    parent.add_child(child)

    # Layout the tree
    layout(parent, Point(0, 0))

    # Check parent sizing
    parent_expected_width = 200 + (5 * 2) + (2 * 2)  # 214
    parent_expected_height = 100 + (5 * 2) + (2 * 2)  # 114
    assert parent.rect.width == parent_expected_width
    assert parent.rect.height == parent_expected_height

    # Check child sizing
    child_expected_width = 50 + (3 * 2) + (1 * 2)  # 58
    child_expected_height = 30 + (3 * 2) + (1 * 2)  # 38
    assert child.rect.width == child_expected_width
    assert child.rect.height == child_expected_height

    # Check child positioning (static, so should be positioned at parent location)
    assert child.rect.x == parent.rect.x  # Same x as parent
    assert child.rect.y == parent.rect.y  # Same y as parent (inside parent)


def test_layout_mixed_positioning():
    """Test layout with mixed positioning types."""
    # Create parent
    parent = Element(
        display=Display.CONTENT,
        content_width=200,
        content_height=100,
        padding=5,
        border=2
    )

    # Create static child
    static_child = Element(
        display=Display.CONTENT,
        content_width=50,
        content_height=30,
        padding=3,
        border=1,
        position=Position.STATIC
    )

    # Create absolute child
    absolute_child = Element(
        display=Display.CONTENT,
        content_width=40,
        content_height=20,
        padding=2,
        border=1,
        position=Position.ABSOLUTE,
        offset_x=10,
        offset_y=15
    )

    parent.add_child(static_child)
    parent.add_child(absolute_child)

    # Layout the tree
    layout(parent, Point(0, 0))

    # Check parent sizing
    parent_expected_width = 200 + (5 * 2) + (2 * 2)  # 214
    parent_expected_height = 100 + (5 * 2) + (2 * 2)  # 114
    assert parent.rect.width == parent_expected_width
    assert parent.rect.height == parent_expected_height

    # Check static child positioning (should be at parent location)
    assert static_child.rect.x == parent.rect.x
    assert static_child.rect.y == parent.rect.y

    # Check absolute child positioning (relative to parent origin)
    assert absolute_child.rect.x == parent.rect.x + 10
    assert absolute_child.rect.y == parent.rect.y + 15