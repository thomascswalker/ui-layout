from ui.types import Element, Point, Rect
import logging

logger = logging.getLogger(__name__)


def layout(root: Element, available: Rect) -> None:
    """
    Layout the element and its children within the available space.

    ```
    root.rect.x,
    root.rect.y
    ↓
    ╭─ root.margin ─────────────────────────╮
    │ ╭ root.border ────────────────────╮ ↑ │
    │ │ ╭ root.padding ───────────────╮ │ │ │
    │ │ │ ╭─────────────────────────╮ │ │ │ │
    │ │ │ │                         │ │ │ │ ┆
    │ │ │ │     child (content)     │ │ │ ├ root.rect.height
    │ │ │ │                         │ │ │ │ ┆
    │ │ │ ╰─────────────────────────╯ │ │ │ │
    │ │ ╰─────────────────────────────╯ │ │ │
    │ ╰─────────────────────────────────╯ ↓ │
    │ ←─────────────────┬───────────────→   │
    │           root.rect.width             │
    ╰───────────────────────────────────────╯ ← root.rect.x + root.rect.width,
                                                root.rect.y + root.rect.height
    ```
    """
    # 1. Account for this element's margin when sizing and positioning
    root.rect.width = available.width - (root.margin * 2)
    root.rect.height = available.height - (root.margin * 2)
    root.rect.x = available.min.x + root.margin
    root.rect.y = available.min.y + root.margin

    # 2. Calculate the content area (inside padding)

    # 2.1. Start position for child elements
    delta = Point(root.rect.x + root.padding, root.rect.y + root.padding)

    # 2.2. Available space for children (content area)
    content = Point(
        root.rect.width - (root.padding * 2),
        root.rect.height - (root.padding * 2),
    )

    # 3. Layout children
    child_count = len(root.children)

    # If no children, just return
    if not child_count:
        return

    # 3.1. Account for margin space used by all children
    # Each child will use: size + (margin * 2)
    total_margin = sum(child.margin * 2 for child in root.children)
    total_gap = root.gap * (child_count - 1)

    # 3.2. Remaining space after accounting for children's margins and gaps
    match root.direction:
        case "vertical":
            remaining = content.y
        case "horizontal":
            remaining = content.x
    remaining -= total_margin + total_gap

    # 3.3. Distribute remaining space equally among children
    match root.direction:
        case "vertical":
            content.y = remaining / child_count
        case "horizontal":
            content.x = remaining / child_count

    # 3.4. Position each child with its own available space
    for child in root.children:
        # Child rect
        child_available = Rect(delta.x, delta.y, content.x, content.y)

        # Calculate available space for this child, including its margin
        match root.direction:
            case "vertical":
                child_available.height = content.y + (child.margin * 2)
            case "horizontal":
                child_available.width = content.x + (child.margin * 2)

        # Recursively layout the child
        layout(child, child_available)

        # Update position for next child
        match root.direction:
            case "vertical":
                delta.y += child_available.height + root.gap
            case "horizontal":
                delta.x += child_available.width + root.gap
