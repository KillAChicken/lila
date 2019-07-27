"""Test cases for the base class of Siren component."""

import pytest

from lila.core.base import Component


@pytest.mark.parametrize(
    argnames="classes, expected_classes",
    argvalues=[
        (["class1", "class2"], ("class1", "class2")),
        ([], ()),
    ],
    ids=[
        "Happy path",
        "Empty list",
    ],
)
def test_classes(classes, expected_classes):
    """Check classes of a component.

    1. Create a component with different classes.
    2. Get classes of the component.
    3. Check the classes.
    """
    component = Component(classes=classes)
    assert component.classes == expected_classes, "Wrong classes"


def test_default_classes():
    """Check default classes of a component.

    1. Create a component without specifying classes.
    2. Check classes of the component.
    """
    component = Component()
    assert component.classes == (), "Wrong classes"


def test_invalid_classes():
    """Check that ValueError is raised if invalid classes are passed.

    1. Try to create a component with non-iterable classes.
    2. Check that ValueError is raised.
    3. Check the message of the error.
    """
    with pytest.raises(ValueError) as error_info:
        Component(classes=1)

    assert error_info.value.args[0] == "Classes must be iterable with string values"
