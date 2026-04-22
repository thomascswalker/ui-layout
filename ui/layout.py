from ui.types import Element, Point, Rect
import logging

logger = logging.getLogger(__name__)


def layout(root: Element, available: Rect) -> None:
    """
    Layout the element and its children within the available space.

    ```
    root.rect.x, root.rect.y (top-left origin)
    ↓
    ╭─ margin ────────────────────────────╮ ↑
    │ ╭ border ─────────────────────────╮ │ │
    │ │ ╭ padding ────────────────────╮ │ │ │
    │ │ │ ╭─────────────────────────╮ │ │ │ │
    │ │ │ │                         │ │ │ │ │ root.rect.height
    │ │ │ │        Content          │ │ │ │ │
    │ │ │ │                         │ │ │ │ │
    │ │ │ ╰─────────────────────────╯ │ │ │ │
    │ │ ╰─────────────────────────────╯ │ │ │
    │ ╰─────────────────────────────────╯ │ │
    ╰─────────────────────────────────────╯ ↓
    ←─────────────────────────────────────→
                root.rect.width
    ```
    """
    # 1. Calculate size
    size(root, available)

    # 2. Calculate position
    position(root, available.min)

    # Calculate delta X and Y for child elements, starting from the top-left corner of
    # the content area
    dx = root.rect.x + root.padding  # Delta X
    dy = root.rect.y + root.padding  # Delta Y

    # Calculate available width and height for children. Padding is subtracted from both sides,
    # so we multiply by 2.
    aw = root.rect.width - root.padding * 2  # Available Width
    ah = root.rect.height - root.padding * 2  # Available Height

    # Calculate available height for each child (if there are any children)
    child_count = len(root.children)
    if child_count > 0:
        # Compute the total gap height and subtract it from the available height
        gap_height = ah - root.gap * (child_count - 1)

        # Divide the remaining height by the number of children to get the
        # height per child
        ah = gap_height / child_count

    for child in root.children:
        # Layout this child
        layout(child, Rect(dx, dy, aw, ah))

        # Increase delta Y for the next child, accounting for the gap
        dy += child.rect.height + root.gap


def size(element: Element, available: Rect) -> None:
    element.rect.width = available.width
    element.rect.height = available.height


def position(element: Element, origin: Point) -> None:
    element.rect.x = origin.x
    element.rect.y = origin.y
