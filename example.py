"""
Example demonstrating how to use the UI layout and rendering system.
"""

from ui import Element, Rect, Display, Position, layout, render


def example_basic_layout():
    """Create and render elements using the layout algorithm."""
    # Create root element
    root = Element(rect=Rect(0, 0, 800, 600), display=Display.GROW)

    # Create block elements that will stack vertically
    header = Element(display=Display.GROW, content_height=100, content_width=800)

    content = Element(display=Display.GROW, content_height=400, content_width=800)

    footer = Element(display=Display.GROW, content_height=100, content_width=800)

    # Add children to root
    root.add_child(header)
    root.add_child(content)
    root.add_child(footer)

    # Calculate layout
    layout(root)

    # Render the tree
    render(root, title="Basic Layout Example")


def example_inline_elements():
    """Create elements with inline display type."""
    # Create root element
    root = Element(rect=Rect(0, 0, 800, 600), display=Display.GROW)

    # Create inline elements
    child1 = Element(display=Display.GROW, content_width=150, content_height=50)

    child2 = Element(display=Display.GROW, content_width=150, content_height=50)

    child3 = Element(display=Display.GROW, content_width=150, content_height=50)

    # Add children to root
    root.add_child(child1)
    root.add_child(child2)
    root.add_child(child3)

    # Calculate layout
    layout(root)

    # Render the tree
    render(root, title="Inline Elements Example")


def example_positioned_elements():
    """Create elements with different positioning strategies."""
    # Create root element
    root = Element(rect=Rect(0, 0, 800, 600), display=Display.GROW)

    # Static elements (normal flow)
    static1 = Element(
        display=Display.GROW,
        content_height=80,
        content_width=800,
        position=Position.STATIC,
    )

    static2 = Element(
        display=Display.GROW,
        content_height=80,
        content_width=800,
        position=Position.STATIC,
    )

    # Relative element (offset from normal position)
    relative = Element(
        display=Display.GROW,
        content_height=80,
        content_width=200,
        position=Position.RELATIVE,
        offset_x=50,
        offset_y=20,
    )

    # Absolute element (positioned relative to parent)
    absolute = Element(
        display=Display.GROW,
        content_height=60,
        content_width=150,
        position=Position.ABSOLUTE,
        offset_x=400,
        offset_y=450,
    )

    # Add children to root
    root.add_child(static1)
    root.add_child(static2)
    root.add_child(relative)
    root.add_child(absolute)

    # Calculate layout
    layout(root)

    # Render the tree
    render(root, title="Positioned Elements Example")


def example_nested_blocks():
    """Create a nested element tree with block elements."""
    # Create root element
    root = Element(rect=Rect(0, 0, 800, 600), display=Display.GROW)

    # Create container
    container = Element(display=Display.GROW, content_height=500, content_width=750)

    # Create children inside container
    child1 = Element(display=Display.GROW, content_height=100, content_width=750)

    child2 = Element(display=Display.GROW, content_height=100, content_width=750)

    # Add children to container
    container.add_child(child1)
    container.add_child(child2)

    # Add container to root
    root.add_child(container)

    # Calculate layout
    layout(root)

    # Render the tree
    render(root, title="Nested Blocks Example")


if __name__ == "__main__":
    # Run examples (uncomment to try different ones)
    example_basic_layout()
    example_inline_elements()
    example_positioned_elements()
    example_nested_blocks()
