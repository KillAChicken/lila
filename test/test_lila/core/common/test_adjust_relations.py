"""Test cases for adjust_relations function."""

import pytest

from lila.core.common import adjust_relations


def test_string_values():
    """Check that all values are converted to strings.

    1. Create a list with different values.
    2. Pass the list to adjust_relations.
    3. Check values of the returned tuple.
    """
    relations = ["plain string", 1, None, ["nested"]]
    assert adjust_relations(relations) == ("plain string", "1", "None", "['nested']"), (
        "Wrong convertion"
        )


def test_invalid_relations():
    """Check that ValueError is raised if invalid object is passed to the function.

    1. Pass non-iterable value to adjust_relations.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        adjust_relations(None)

    assert error_info.value.args[0] == "Relationships must be iterable with string values"
