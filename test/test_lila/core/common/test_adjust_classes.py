"""Test cases for adjust_classes function."""

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
