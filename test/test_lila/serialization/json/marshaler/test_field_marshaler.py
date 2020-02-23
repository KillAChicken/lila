"""Test cases for a marshaler class for a field."""

import random
from collections import namedtuple

import pytest

from lila.core.field import Field, InputType
from lila.serialization.json.field import FieldMarshaler


def test_missing_name():
    """Test that ValueError is raised if a field does not have name attribute.

    1. Create a field marshaler for an object without name attibute.
    2. Try to call marshal_name method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldMarshaler(object()).marshal_name()

    assert error_info.value.args[0] == "Failed to get field's name", "Wrong error"


@pytest.mark.parametrize(
    argnames="name,expected_name",
    argvalues=[
        ("name", "name"),
        (u"Имя на русском", u"Имя на русском"),
        ("", ""),
        (None, "None"),
        ([1, 2, 5], "[1, 2, 5]"),
        ],
    ids=[
        "Simple",
        "Unicode",
        "Empty",
        "None",
        "List",
        ],
    )
def test_name(name, expected_name):
    """Test that name is properly marshaled.

    1. Create a field marshaler for an object with specific name.
    2. Marshal field's name.
    3. Check the marshaled name.
    """
    NameField = namedtuple("NameField", "name")
    actual_name = FieldMarshaler(NameField(name=name)).marshal_name()
    assert actual_name == expected_name, "Wrong name"


def test_missing_classes():
    """Test that ValueError is raised if a field does not have classes attribute.

    1. Create a field marshaler for an object without classes attribute.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldMarshaler(object()).marshal_classes()

    assert error_info.value.args[0] == "Failed to get field's classes", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if a field provides a non-iterable object as its classes.

    1. Create a field marshaler for an object with non-iterable classes.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    ClassesField = namedtuple("ClassesField", "classes")
    with pytest.raises(ValueError) as error_info:
        FieldMarshaler(ClassesField(classes=None)).marshal_classes()

    assert error_info.value.args[0] == "Failed to iterate over field's classes", "Wrong error"


@pytest.mark.parametrize(
    argnames="classes,expected_classes",
    argvalues=[
        ([], []),
        (["field class"], ["field class"]),
        (["first field class", "second field class"], ["first field class", "second field class"]),
        (("first", None, [1, 2]), ["first", "None", "[1, 2]"]),
        ],
    ids=[
        "Empty list",
        "Single class",
        "Multiple classes",
        "Non-string classes",
        ],
    )
def test_classes(classes, expected_classes):
    """Test that classes are properly marshaled.

    1. Create a field marshaler for an object with specific classes.
    2. Marshal classes.
    3. Check the marshaled classes.
    """
    ClassesField = namedtuple("ClassesField", "classes")
    actual_classes = FieldMarshaler(ClassesField(classes=classes)).marshal_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_missing_input_type():
    """Test that ValueError is raised if a field does not have input type attribute.

    1. Create a field marshaler for an object without input type.
    2. Try to call marshal_input_type method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldMarshaler(object()).marshal_input_type()

    assert error_info.value.args[0] == "Failed to get field's input type", "Wrong error"


def test_not_supported_input_type():
    """Test that ValueError is raised if input type of the field is not supported.

    1. Create a field marshaler for an object with unsupported input type.
    2. Try to call marshal_input_type method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    InputTypeField = namedtuple("InputTypeField", "input_type")
    with pytest.raises(ValueError) as error_info:
        FieldMarshaler(InputTypeField(input_type="TEXT")).marshal_input_type()

    assert error_info.value.args[0] == "Field's input type is not supported", "Wrong error"


@pytest.mark.parametrize(
    argnames="input_type",
    argvalues=[
        random.choice(list(InputType)),
        random.choice(list(InputType)).value,
        ],
    ids=[
        "Enumeration item",
        "String",
        ],
    )
def test_input_type(input_type):
    """Test that input type is properly marshaled.

    1. Create a field marshaler for an object with specific input type.
    2. Marshal field's input type.
    3. Check the marshaled input type.
    """
    InputTypeField = namedtuple("Field", "input_type")
    actual_input_type = FieldMarshaler(InputTypeField(input_type=input_type)).marshal_input_type()
    assert actual_input_type == InputType(input_type).value, "Wrong input type"


def test_missing_value():
    """Test that ValueError is raised if a field does not have value attribute.

    1. Create a field marshaler for an object without value attribute.
    2. Try to call marshal_value method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldMarshaler(object()).marshal_value()

    assert error_info.value.args[0] == "Failed to get field's value", "Wrong error"


@pytest.mark.parametrize(
    argnames="value,expected_value",
    argvalues=[
        ("field value", "field value"),
        (u"Значение на русском", u"Значение на русском"),
        ("", ""),
        (None, None),
        ([7, 4], "[7, 4]"),
        ],
    ids=[
        "Simple",
        "Unicode",
        "Empty",
        "None",
        "List",
        ],
    )
def test_value(value, expected_value):
    """Test that value is properly marshaled.

    1. Create a field marshaler for an object with specific value.
    2. Marshal field's value.
    3. Check the marshaled value.
    """
    ValueField = namedtuple("ValueField", "value")
    actual_value = FieldMarshaler(ValueField(value=value)).marshal_value()
    assert actual_value == expected_value, "Wrong value"


def test_missing_title():
    """Test that ValueError is raised if a field does not have title attribute.

    1. Create a field marshaler for an object without title attribute.
    2. Try to call marshal_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldMarshaler(object()).marshal_title()

    assert error_info.value.args[0] == "Failed to get field's title", "Wrong error"


@pytest.mark.parametrize(
    argnames="title,expected_title",
    argvalues=[
        ("field title", "field title"),
        (u"Заголовок на русском", u"Заголовок на русском"),
        ("", ""),
        (None, None),
        ],
    ids=[
        "Simple",
        "Unicode",
        "Empty",
        "None",
        ],
    )
def test_title(title, expected_title):
    """Test that title is properly marshaled.

    1. Create a field marshaler for an object with specific title.
    2. Marshal field's title.
    3. Check the marshaled title.
    """
    TitleField = namedtuple("TitleField", "title")
    actual_title = FieldMarshaler(TitleField(title=title)).marshal_title()
    assert actual_title == expected_title, "Wrong title"


def test_marshal():
    """Test that field data is properly marshaled.

    1. Create a field.
    2. Create a field marshaler for the field.
    3. Replace marshaler methods so that they return predefined data.
    4. Marshal the field.
    5. Check the marshaled data.
    """
    marshaler = FieldMarshaler(Field(name="field"))
    marshaler.marshal_name = lambda: "marshal_name"
    marshaler.marshal_classes = lambda: "marshal_classes"
    marshaler.marshal_input_type = lambda: "marshal_input_type"
    marshaler.marshal_value = lambda: "marshal_value"
    marshaler.marshal_title = lambda: "marshal_title"

    actual_data = marshaler.marshal()
    expected_data = {
        "name": "marshal_name",
        "class": "marshal_classes",
        "type": "marshal_input_type",
        "value": "marshal_value",
        "title": "marshal_title",
        }
    assert actual_data == expected_data, "Field is not properly marshaled"
