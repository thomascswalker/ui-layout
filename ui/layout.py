from ui.types import Element, Rect
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
    # 1. Set the root element's size to the available space
    root.rect.width = available.width
    root.rect.height = available.height

    # 2. Set the root element's position to the top-left corner of the available
    # space
    root.rect.x = available.min.x
    root.rect.y = available.min.y

    # 3. Layout each child element

    # 3.1. Calculate delta X/Y for child elements, starting from the
    # top-left corner of the content area.
    delta_x = root.rect.x + root.padding
    delta_y = root.rect.y + root.padding

    # 3.2. Calculate available width and height for children. Padding is
    # subtracted from both sides, so we multiply by 2.
    available_width = root.rect.width - (root.padding * 2)
    available_height = root.rect.height - (root.padding * 2)

    # 3.3. Calculate available height for each child (if there are any children)
    child_count = len(root.children)

    # 3.4. If there are children and a gap is specified, we need to account for
    # the total gap space between children.
    if child_count > 0:
        # Calculate total gap between children.
        total_gap = root.gap * (child_count - 1)

        # Subtract the total gap from the available directional space, then
        # divide the remaining space by the number of children to get the
        # space per child.
        match root.direction:
            case "vertical":
                available_height = (available_height - total_gap) / child_count
            case "horizontal":
                available_width = (available_width - total_gap) / child_count

    # 3.5. Layout each child element, updating delta X/Y for the next child
    # based on the layout direction.
    for child in root.children:
        # Layout this child
        layout(child, Rect(delta_x, delta_y, available_width, available_height))

        # Increase delta X/Y for the next child, accounting for the gap
        match root.direction:
            case "vertical":
                delta_y += child.rect.height + root.gap
            case "horizontal":
                delta_x += child.rect.width + root.gap
