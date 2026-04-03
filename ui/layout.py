"""
Layout algorithm implementation.

Processes the element tree and calculates positions and sizes based on
display type and positioning rules.
"""

from ui.types import Element, Display, Point, Position


def layout(
    root: Element,
    origin: Point = Point(0.0, 0.0),
) -> None:
    # First calculate size based on display type and content
    size(root)

    # Then calculate position based on positioning rules
    position(root, origin)

    # Recursively layout children
    dy = root.rect.y
    for child in root.children:
        match child.position:
            # Static elements are laid out in normal flow (stacked vertically)
            case Position.STATIC:
                layout(child,  Point(root.rect.x, dy))
                dy += child.rect.height
            # All other positioning types are independent of normal flow and can be laid out 
            # at the root's origin
            case _:
                layout(child, Point(root.rect.x, root.rect.y))


def size(element: Element) -> None:
    # Calculate total padding as: content + padding + border
    padding = element.padding * 2 + element.border * 2

    # Check if width was explicitly set (not the default 1.0)
    if element.rect.width != 1.0:
        # Explicit width defined - add padding/border to existing width
        element.rect.width = element.rect.width + padding
    else:
        match element.display:
            case Display.GROW:
                # GROW: width will be set by parent during layout
                # For now, use content width as fallback
                element.rect.width = element.content_width + padding
            case Display.CONTENT:
                # CONTENT: width = size of content
                element.rect.width = element.content_width + padding
            case Display.FIXED:
                # FIXED: width = size of content if not explicit
                element.rect.width = element.content_width + padding

    # Check if height was explicitly set (not the default 1.0)
    if element.rect.height != 1.0:
        # Explicit height defined - add padding/border to existing height
        element.rect.height = element.rect.height + padding
    else:
        match element.display:
            case Display.GROW:
                # GROW: height = content-driven
                element.rect.height = element.content_height + padding
            case Display.CONTENT:
                # CONTENT: height = size of content
                element.rect.height = element.content_height + padding
            case Display.FIXED:
                # FIXED: height = size of content if not explicit
                element.rect.height = element.content_height + padding


def position(
    element: Element,
    origin: Point,
) -> None:
    match element.position:
        case Position.STATIC:
            # Normal flow: position at parent location
            element.rect.x = origin.x
            element.rect.y = origin.y
        case Position.RELATIVE:
            # Relative: offset from original flow position
            element.rect.x = origin.x + element.offset_x
            element.rect.y = origin.y + element.offset_y
        case Position.ABSOLUTE:
            # Absolute: position relative to parent's position
            element.rect.x = origin.x + element.offset_x
            element.rect.y = origin.y + element.offset_y
        case Position.FIXED:
            # Fixed: position relative to viewport (using offset as absolute coords)
            element.rect.x = element.offset_x
            element.rect.y = element.offset_y
        case _:
            element.rect.x = origin.x
            element.rect.y = origin.y
