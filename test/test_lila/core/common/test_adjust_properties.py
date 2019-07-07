"""Test cases for adjust_properties function."""

from collections import namedtuple

import pytest

from lila.core.common import adjust_properties


Namedtuple = namedtuple("Namedtuple", "first second")


def test_string_keys():
    """Check that all keys are converted to strings.

    1. Create a list with property items  with keys of different types.
    2. Pass the dictionary to adjust_properties.
    3. Check keys of the returned dictionary.
    """
    properties = [
        ("plain string", "string value"),
        (1, "integer value"),
        (("tuple", ), "tuple value"),
        ]
    assert set(adjust_properties(properties).keys()) == set(("plain string", "1", "('tuple',)")), (
        "Wrong convertion"
        )


@pytest.mark.parametrize(
    argnames="actual_value, expected_value",
    argvalues=[
        ["String value", "String value"],
        [12, 12],
        [None, None],
        [("iterable", 1, "2"), ["iterable", 1, "2"]],
        [{"key": "value"}, {"key": "value"}],
        [Namedtuple("field1", "field2"), ["field1", "field2"]],
    ],
    ids=[
        "String",
        "Integer",
        "None",
        "Iterable",
        "Nested dictionary",
        "Namedtuple",
    ],
)
def test_valid_values(actual_value, expected_value):
    """Check that valid values are properly converted.

    1. Create a dictionary with 1 property and value of different types.
    2. Pass the dictionary to adjust_properties.
    3. Check the converted value.
    """
    property_name = "key"
    properties = {property_name: actual_value}
    adjusted_value = adjust_properties(properties)[property_name]
    assert type(adjusted_value) == type(expected_value), "Wrong type"   # pylint: disable=unidiomatic-typecheck
    assert adjusted_value == expected_value, "Wrong value"


@pytest.mark.parametrize(
    argnames="properties",
    argvalues=[
        None,
        [(["list"], "unhashable key")],
        ["test"],
    ],
    ids=[
        "None",
        "Unhashable key",
        "Iterable without items",
    ],
)
def test_invalid_dictionary(properties):
    """Check that ValueError is raised if properties can't be converted to a dictionary.

    1. Call adjust_properties with object, that can't be converted to dictionary.
    2. Check that ValueError is raised.
    3. Check error message.
    """
    with pytest.raises(ValueError) as error_info:
        adjust_properties(properties)

    assert error_info.value.args[0] == "Can't create dictionary from properties", (
        "Wrong error message"
        )


@pytest.mark.parametrize(
    argnames="invalid_value",
    argvalues=[
        object(),
    ],
    ids=[
        "Object",
    ],
)
def test_invalid_values(invalid_value):
    """Check that ValueError is raised if one of the properties has invalid value.

    1. Create a dictionary with 1 key. Its value is invalid.
    2. Pass the dictionary to adjust_properties.
    3. Check that ValueError is raised.
    4. Check error message.
    """
    property_name = "invalid_property"
    with pytest.raises(ValueError) as error_info:
        adjust_properties({property_name: invalid_value})

    expected_message = "Unsupported value for property '{name}'".format(name=property_name)
    assert error_info.value.args[0] == expected_message, "Wrong error message"
