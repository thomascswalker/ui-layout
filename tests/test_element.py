import pytest

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


@pytest.mark.parametrize("xml_filename", ["basic.xml"])
def test_element_parse(xml_filename: str):
    with open(f"tests/fixtures/{xml_filename}", "r") as f:
        xml_string = f.read()
    root_element = Element.parse(xml_string)

    assert root_element.id == "root"
    assert root_element.display == "grow"
    assert len(root_element.children) == 2

    child1 = root_element.children[0]
    assert child1.id == "child1"
    assert child1.display == "grow"

    child2 = root_element.children[1]
    assert child2.id == "child2"
    assert child2.display == "fixed"
