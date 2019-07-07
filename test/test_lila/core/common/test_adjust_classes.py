"""Test cases for adjust_classes function."""

import pytest

from lila.core.common import adjust_classes


def test_string_values():
    """Check that all values are converted to strings.

    1. Create a list with different values.
    2. Pass the list to adjust_classes.
    3. Check values of the returned tuple.
    """
    classes = ["plain string", 1, None, ["nested"]]
    assert adjust_classes(classes) == ("plain string", "1", "None", "['nested']"), (
        "Wrong convertion"
        )


def test_invalid_classes():
    """Check that ValueError is raised if invalid object is passed to the function.

    1. Pass non-iterable value to adjust_classes.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        adjust_classes(None)

    assert error_info.value.args[0] == "Classes must be iterable with string values"
