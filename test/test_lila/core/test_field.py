"""Test cases for Siren Fields."""

import random

import pytest

from lila.core.field import InputType, Field


@pytest.mark.parametrize(
    argnames="name, expected_name",
    argvalues=[
        ("string name", "string name"),
        (None, "None"),
        (12, "12"),
    ],
    ids=[
        "String",
        "None",
        "Integer",
    ],
)
def test_name(name, expected_name):
    """Check name of a field.

    1. Create a field with different names.
    2. Get name of the field.
    3. Check the name.
    """
    field = Field(name=name)
    assert field.name == expected_name, "Wrong name"


def test_default_classes():
    """Check default classes of the field.

    1. Create a field without specifying classes.
    2. Check classes of the field.
    """
    field = Field(name="test default classes")
    assert field.classes == (), "Wrong classes"


@pytest.mark.parametrize(
    argnames="classes, expected_classes",
    argvalues=[
        (["field-class1", "field-class2"], ("field-class1", "field-class2")),
    ],
    ids=[
        "Happy path",
    ],
)
def test_classes(classes, expected_classes):
    """Check classes of a field.

    1. Create a field with different classes.
    2. Get classes of the field.
    3. Check the classes.
    """
    field = Field(name="test classes", classes=classes)
    assert field.classes == expected_classes, "Wrong classes"


def test_invalid_classes():
    """Check that ValueError is raised if invalid classes are passed.

    1. Try to create a field with non-iterable classes.
    2. Check that ValueError is raised.
    """
    with pytest.raises(ValueError):
        Field(name="test invalid classes", classes=1)


def test_input_type():
    """Check input type of the field.

    1. Create a field with explicit input type.
    2. Get input type of the field.
    3. Check the type.
    """
    input_type = random.choice(list(InputType))
    field = Field(name="test input type", input_type=input_type)
    assert field.input_type == input_type, "Wrong input type"


def test_default_input_type():
    """Check default input type of the field.

    1. Create a field without specifying input type.
    2. Check input field of the field.
    """
    field = Field(name="test default input type")
    assert field.input_type == InputType.TEXT, "Wrong default input type"


def test_invalid_input_type():
    """Check that ValueError is raised if invalid input type is specified.

    1. Try to create a field with name of the input field instead of constant from enumeration.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    invalid_input_type = InputType.TEXT.name

    with pytest.raises(ValueError) as error_info:
        Field(name="test invalid input type", input_type=invalid_input_type)

    assert error_info.value.args[0] == "Unsupported input type '{0}'".format(invalid_input_type), (
        "Wrong error message"
        )


@pytest.mark.parametrize(
    argnames="value, expected_value",
    argvalues=[
        ("string value", "string value"),
        (None, None),
        (123, "123"),
    ],
    ids=[
        "String",
        "None",
        "Integer",
    ],
)
def test_value(value, expected_value):
    """Check value of a field.

    1. Create a field with different values.
    2. Get value of the field.
    3. Check the value.
    """
    field = Field(name="test title", value=value)
    assert field.value == expected_value, "Wrong value"


def test_default_value():
    """Check default value of a field.

    1. Create a field without specifying a value.
    2. Check the value of the field.
    """
    field = Field(name="test default title")
    assert field.value is None, "Wrong value"


@pytest.mark.parametrize(
    argnames="title, expected_title",
    argvalues=[
        ("string title", "string title"),
        (None, None),
        (12, "12"),
    ],
    ids=[
        "String",
        "None",
        "Integer",
    ],
)
def test_title(title, expected_title):
    """Check title of a field.

    1. Create a field with different titles.
    2. Get title of the field.
    3. Check the title.
    """
    field = Field(name="test title", title=title)
    assert field.title == expected_title, "Wrong title"


def test_default_title():
    """Check default title of a field.

    1. Create a field without specifying a title.
    2. Check the title of the field.
    """
    field = Field(name="test default title")
    assert field.title is None, "Wrong title"
