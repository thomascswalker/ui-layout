"""
Layout algorithm implementation.

Processes the element tree and calculates positions and sizes based on
display type and positioning rules.
"""

from ui.types import Element, Point, Rect
import logging

logger = logging.getLogger(__name__)


def layout(root: Element, available: Rect) -> None:
    # 1. First calculate size based on display type and content
    size(root, available)

    # 2. Then calculate position based on positioning rules
    position(root, available.min)

    # 3. Recursively layout children

    dx = root.rect.x + root.padding  # Delta X
    dy = root.rect.y + root.padding  # Delta Y
    aw = root.rect.width - root.padding * 2  # Available Width
    ah = root.rect.height - root.padding * 2  # Available Height

    # Calculate available height for each child (if there are any children)
    child_count = len(root.children)
    if child_count > 0:
        # 1. Compute the total gap height and subtract it from the available height
        # 2. Divide the remaining height by the number of children to get the
        # height per child
        gap_height = ah - root.gap * (child_count - 1)
        ah = gap_height / child_count

    for child in root.children:
        # Layout this child
        layout(child, Rect(dx, dy, aw, ah))

        # Move down the delta Y for the next child, accounting for the gap
        dy += child.rect.height + root.gap


def size(element: Element, available: Rect) -> None:
    element.rect.width = available.width
    element.rect.height = available.height


def position(element: Element, origin: Point) -> None:
    # TODO: Implement relative, absolute, fixed positioning logic
    element.rect.x = origin.x
    element.rect.y = origin.y
