from ui.types import Element, Rect


def test_element_create():
    rect = Rect(0, 0, 100, 100)
    element = Element(rect=rect)

    assert element.rect == rect
    assert element.children == []
    assert element.parent is None


def test_element_add_child():
    parent_rect = Rect(0, 0, 100, 100)
    child_rect = Rect(10, 10, 50, 50)

    parent_element = Element(rect=parent_rect)
    child_element = Element(rect=child_rect)

    parent_element.add_child(child_element)

    assert child_element in parent_element.children
    assert child_element.parent == parent_element


def test_element_remove_child():
    parent_rect = Rect(0, 0, 100, 100)
    child_rect = Rect(10, 10, 50, 50)

    parent_element = Element(rect=parent_rect)
    child_element = Element(rect=child_rect)

    parent_element.add_child(child_element)
    parent_element.remove_child(child_element)

    assert child_element not in parent_element.children
    assert child_element.parent is None
