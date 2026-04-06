"""
Layout algorithm implementation.

Processes the element tree and calculates positions and sizes based on
display type and positioning rules.
"""

from ui.types import Element, Display, Point, Position, Rect
import logging

logger = logging.getLogger(__name__)


def layout(
    root: Element,
    available: Rect,
) -> None:
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
    padding = element.padding * 2 + element.border * 2
    logger.debug(f"Padding: {padding}")

    element.rect.width = available.width - padding
    element.rect.height = available.height - padding


def position(
    element: Element,
    origin: Point,
) -> None:
    # TODO: Implement relative, absolute, fixed positioning logic
    element.rect.x = origin.x
    element.rect.y = origin.y
