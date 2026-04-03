from ui.types import Element, Point, Rect


def layout_grow(available: Rect, element: Element) -> Point:
    # Grow the element to fill the available space
    element.rect = available

    # Return the new maximum point of the element
    return element.rect.max
