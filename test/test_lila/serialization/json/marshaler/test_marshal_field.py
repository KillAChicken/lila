"""Test cases for marshal_field method of JSON marshaler."""

import random

import pytest

from lila.core.field import Field, InputType
from lila.serialization.json.marshaler import JSONMarshaler


def test_missing_name():
    """Test that ValueError is raised if a field does not have name attribute.

    1. Create a json marshaller.
    2. Try to call marshal_field method for an object without name attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingNameField(Field):
        @property
        def name(self):
            raise AttributeError()

    field = _MissingNameField(name="no name")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_field(field=field)

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

    1. Create a json marshaler.
    2. Marshal a field with a specific name.
    3. Check a key with the name in the marshaled data.
    """
    class _FixedNameField(Field):
        @property
        def name(self):
            return name

    field = _FixedNameField(name="fixed name")

    field_data = JSONMarshaler().marshal_field(field=field)
    assert "name" in field_data, "Marshaled data does not have 'name' key"
    assert field_data["name"] == expected_name, "Wrong name"


def test_missing_classes():
    """Test that ValueError is raised if a field does not have classes attribute.

    1. Create a json marshaller.
    2. Try to call marshal_field method for an object without classes attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingClassesField(Field):
        @property
        def classes(self):
            raise AttributeError()

    field = _MissingClassesField(name="no classes")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_field(field=field)

    assert error_info.value.args[0] == "Failed to get field's classes", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if fields provides a non-iterable object as its classes.

    1. Create a json marshaller.
    2. Try to call marshal_field method for an object with non-iterable classes.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableClassesField(Field):
        @property
        def classes(self):
            return None

    field = _NonIterableClassesField(name="'classes' attribute is not iterable")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_field(field=field)

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

    1. Create a json marshaler.
    2. Marshal a field with specific classes.
    3. Check a key with the classes in the marshaled data.
    """
    class _FixedClassesField(Field):
        @property
        def classes(self):
            return classes

    field = _FixedClassesField(name="fixed classes")

    field_data = JSONMarshaler().marshal_field(field=field)
    assert "class" in field_data, "Marshaled data does not have 'class' key"
    assert field_data["class"] == expected_classes, "Wrong classes"


def test_missing_input_type():
    """Test that ValueError is raised if a field does not have input type attribute.

    1. Create a json marshaller.
    2. Try to call marshal_field method for an object without input type attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingInputTypeField(Field):
        @property
        def input_type(self):
            raise AttributeError()

    field = _MissingInputTypeField(name="no input field")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_field(field=field)

    assert error_info.value.args[0] == "Failed to get field's input type", "Wrong error"


def test_not_supported_input_type():
    """Test that ValueError is raised if input type of the field is not supported.

    1. Create a json marshaller.
    2. Try to call marshal_field method for an object with unsupported input type.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NotSupportedInputTypeField(Field):
        @property
        def input_type(self):
            return "text"

    field = _NotSupportedInputTypeField(name="Input type is not supported")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_field(field=field)

    assert error_info.value.args[0] == "Field's input type is not supported", "Wrong error"


def test_input_type():
    """Test that input type is properly marshaled.

    1. Create a json marshaler.
    2. Marshal a field with a specific input type.
    3. Check a key with the input type in the marshaled data.
    """
    input_type = random.choice(list(InputType))
    field = Field(name="fixed input type", input_type=input_type)

    field_data = JSONMarshaler().marshal_field(field=field)
    assert "type" in field_data, "Marshaled data does not have 'type' key"
    assert field_data["type"] == input_type.value, "Wrong input type"


def test_missing_value():
    """Test that ValueError is raised if a field does not have value attribute.

    1. Create a json marshaller.
    2. Try to call marshal_field method for an object without value attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingValueField(Field):
        @property
        def value(self):
            raise AttributeError()

    field = _MissingValueField(name="no value")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_field(field=field)

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

    1. Create a json marshaler.
    2. Marshal a field with a specific value.
    3. Check a key with the value in the marshaled data.
    """
    class _FixedValueField(Field):
        @property
        def value(self):
            return value

    field = _FixedValueField(name="fixed value")

    field_data = JSONMarshaler().marshal_field(field=field)
    assert "value" in field_data, "Marshaled data does not have 'value' key"
    assert field_data["value"] == expected_value, "Wrong value"


def test_missing_title():
    """Test that ValueError is raised if a field does not have title attribute.

    1. Create a json marshaller.
    2. Try to call marshal_field method for an object without title attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTitleField(Field):
        @property
        def title(self):
            raise AttributeError()

    field = _MissingTitleField(name="no title")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_field(field=field)

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

    1. Create a json marshaler.
    2. Marshal a field with a specific title.
    3. Check a key with the title in the marshaled data.
    """
    class _FixedTitleField(Field):
        @property
        def title(self):
            return title

    field = _FixedTitleField(name="fixed title")

    field_data = JSONMarshaler().marshal_field(field=field)
    assert "title" in field_data, "Marshaled data does not have 'title' key"
    assert field_data["title"] == expected_title, "Wrong title"
