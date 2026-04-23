from ui.types import Element, Point, Rect, Size
import logging

logger = logging.getLogger(__name__)


def size_element(element: Element, available: Rect) -> None:
    fixed_size = element.fixed()
    grow_size = element.grow(available)
    element.rect.width = fixed_size.w or grow_size.w
    element.rect.height = fixed_size.h or grow_size.h


def position_element(element: Element, available: Rect) -> None:
    position = Point(available.min.x + element.margin, available.min.y + element.margin)
    element.rect.position = position


def layout(element: Element, available: Rect) -> None:
    """
    Layout the element and its children within the available space.

    Args:
        element (Element): The element to layout.
        available (Rect): The available space for this element to occupy.
    """

    # 1. Size and position the element
    size_element(element, available)
    position_element(element, available)

    # 2. Calculate the content area

    # 2.1. Start position for child elements
    delta = Point(element.rect.x + element.padding, element.rect.y + element.padding)

    # 2.2. Available space for children (content area)
    content = Size(
        element.rect.width - (element.padding * 2),
        element.rect.height - (element.padding * 2),
    )

    # 3. Layout children
    child_count = len(element.children)

    # If no children, just return
    if not child_count:
        return

    # 3.1. Calculate total gap space used by children
    gap_space = element.gap * (child_count - 1)

    # 3.2. Calculate total fixed space used by children
    fixed_children = [c for c in element.children if c.display == "fixed"]
    match element.direction:
        case "vertical":
            fixed_space = sum(c.fixed_rect.height for c in fixed_children)
        case "horizontal":
            fixed_space = sum(c.fixed_rect.width for c in fixed_children)

    # 3.3. Calculate remaining grow space after accounting for fixed children
    # and gaps
    match element.direction:
        case "vertical":
            remaining = content.h - fixed_space - gap_space
        case "horizontal":
            remaining = content.w - fixed_space - gap_space

    grow_children = [c for c in element.children if c.display == "grow"]
    grow_space = remaining / len(grow_children) if len(grow_children) > 0 else 0.0

    # 3.4. Remaining space after accounting for children's margins and gaps
    match element.direction:
        case "vertical":
            remaining = content.h
        case "horizontal":
            remaining = content.w

    # 3.5. Distribute remaining space equally among children
    match element.direction:
        case "vertical":
            content.h = remaining / child_count
        case "horizontal":
            content.w = remaining / child_count

    # 3.6. Position each child with its own available space
    for child in element.children:
        # Calculate the available space for the child based on the child's
        # display and the parent's direction.
        match child.display:
            # For fixed children, use their fixed size plus margins
            case "fixed":
                match element.direction:
                    case "vertical":
                        child_height = child.fixed_rect.height + (child.margin * 2)
                        child_width = content.w
                    case "horizontal":
                        child_width = child.fixed_rect.width + (child.margin * 2)
                        child_height = content.h
            # For grow children, use the calculated grow space
            case "grow":
                match element.direction:
                    case "vertical":
                        child_height = grow_space
                        child_width = content.w
                    case "horizontal":
                        child_width = grow_space
                        child_height = content.h
            # For content children, use the content size
            case "content":
                child_width = content.w
                child_height = content.h

        # Recursively layout the child
        layout(child, Rect(delta.x, delta.y, child_width, child_height))

        # Update position for next child
        match element.direction:
            case "vertical":
                delta.y += child.rect.height + element.gap
            case "horizontal":
                delta.x += child.rect.width + element.gap
