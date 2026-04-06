"""
Layout algorithm implementation.

Processes the element tree and calculates positions and sizes based on
display type and positioning rules.
"""

from ui.types import Element, Point, Rect
import logging

logger = logging.getLogger(__name__)


def layout(
    root: Element,
    available: Rect,
) -> None:
    # Apply padding to the available space for this element
    available.x += root.padding
    available.y += root.padding
    available.width -= root.padding * 2
    available.height -= root.padding * 2

    # First calculate size based on display type and content
    size(root, available)

    # Then calculate position based on positioning rules
    position(root, available.min)

    # Recursively layout children
    dy = root.rect.y

    for child in root.children:
        layout(
            child,
            Rect(
                root.rect.x,
                dy,
                root.rect.width,
                root.rect.height / len(root.children),
            ),
        )
        dy += child.rect.height


def size(element: Element, available: Rect) -> None:
    logger.info(f"Sizing element {element.id}")

    element.rect.width = available.width
    element.rect.height = available.height


def position(
    element: Element,
    origin: Point,
) -> None:
    # TODO: Implement relative, absolute, fixed positioning logic
    element.rect.x = origin.x
    element.rect.y = origin.y
