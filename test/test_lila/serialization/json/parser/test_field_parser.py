"""Test cases for a parser class for field data."""

import random

import pytest

from lila.core.field import Field, InputType
from lila.serialization.json.field import FieldParser


def test_unobtainable_name():
    """Test that ValueError is raised if name can't be retrieved from field data.

    1. Create a field parser for a non-subscriptable object.
    2. Try to call parse_name method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldParser(data=None).parse_name()

    assert error_info.value.args[0] == "Failed to get name from field data", "Wrong error"


def test_missing_name():
    """Test that ValueError is raised if field data don't contain 'name' key.

    1. Create a field parser for a dictionary without name.
    2. Try to call parse_name method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldParser(data={}).parse_name()

    assert error_info.value.args[0] == "Field data do not have required 'name' key", "Wrong error"


@pytest.mark.parametrize(
    argnames="name,expected_name",
    argvalues=[
        ("name", "name"),
        (u"Имя на русском", u"Имя на русском"),
        ("", ""),
        (None, "None"),
        ([1, 2, 3], "[1, 2, 3]"),
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
    """Test that name is properly parsed.

    1. Create a field parser for dictionary with specific name.
    2. Parse a name.
    3. Check the parsed name.
    """
    actual_name = FieldParser(data={"name": name}).parse_name()
    assert actual_name == expected_name, "Wrong name"


def test_unobtainable_classes():
    """Test that ValueError is raised if classes can't be retrieved from field data.

    1. Create a field parser for a non-subscriptable object.
    2. Try to call parse_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldParser(data=None).parse_classes()

    assert error_info.value.args[0] == "Failed to get classes from field data", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if field data has a non-iterable object for classes.

    1. Create a field parser for a dictionary with non-iterable classes.
    2. Try to call parse_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldParser(data={"class": None}).parse_classes()

    assert error_info.value.args[0] == "Failed to iterate over classes from field data", (
        "Wrong error"
        )


def test_missing_classes():
    """Test that empty tuple is returned if field data don't have 'class' key.

    1. Create a field parser for a dictionary without classes.
    2. Parse classes.
    3. Check that empty tuple is returned.
    """
    actual_classes = FieldParser(data={}).parse_classes()
    assert actual_classes == (), "Wrong classes"


@pytest.mark.parametrize(
    argnames="classes,expected_classes",
    argvalues=[
        ([], ()),
        (["field class"], ("field class", )),
        (["first field class", "second field class"], ("first field class", "second field class")),
        (("first", None, [1, 2]), ("first", "None", "[1, 2]")),
        ],
    ids=[
        "Empty list",
        "Single class",
        "Multiple classes",
        "Non-string classes",
        ],
    )
def test_classes(classes, expected_classes):
    """Test that classes are properly parsed.

    1. Create a field parser for a dictionary with specific classes.
    2. Parse classes.
    3. Check the parsed classes.
    """
    actual_classes = FieldParser(data={"class": classes}).parse_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_unobtainable_input_type():
    """Test that ValueError is raised if input type can't be retrieved from field data.

    1. Create a field parser for a non-subscriptable object.
    2. Try to call parse_input_type method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldParser(data=None).parse_input_type()

    assert error_info.value.args[0] == "Failed to get input type from field data", "Wrong error"


def test_not_supported_input_type():
    """Test that ValueError is raised if input type is not supported.

    1. Create a field parser for a dictionary with not supported value for input type.
    2. Try to call parse_input_type method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldParser(data={"type": "invalid input type"}).parse_input_type()

    assert error_info.value.args[0] == "Field data contain not supported input type", "Wrong error"


def test_missing_input_type():
    """Test that text input type is returned if field data don't have 'type' key.

    1. Create a field parser for a dictionary without input type.
    2. Parse input type.
    3. Check that text input type is returned.
    """
    actual_input_type = FieldParser(data={}).parse_input_type()
    assert actual_input_type == InputType.TEXT, "Wrong input type"


def test_input_type():
    """Test that input type are properly parsed.

    1. Create a field parser for a dictionary with specific input type.
    2. Parse input type.
    3. Check the parsed input type.
    """
    input_type = random.choice(list(InputType))
    actual_input_type = FieldParser(data={"type": input_type.value}).parse_input_type()
    assert actual_input_type == input_type, "Wrong input type"


def test_unobtainable_value():
    """Test that ValueError is raised if value can't be retrieved from field data.

    1. Create a field parser for a non-subscriptable object.
    2. Try to call parse_value method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldParser(data=None).parse_value()

    assert error_info.value.args[0] == "Failed to get value from field data", "Wrong error"


def test_missing_value():
    """Test that None is returned if field data don't have 'value' key.

    1. Create a field parser for a dictionary without value.
    2. Parse value.
    3. Check that None is returned.
    """
    actual_value = FieldParser(data={}).parse_value()
    assert actual_value is None, "Wrong value"


@pytest.mark.parametrize(
    argnames="value,expected_value",
    argvalues=[
        ("field value", "field value"),
        (u"Значение на русском", u"Значение на русском"),
        ("", ""),
        (None, None),
        ([1, 1], "[1, 1]"),
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
    """Test that value is properly parsed.

    1. Create a field parser for dictionary with specific value.
    2. Parse a value.
    3. Check the parsed value.
    """
    actual_value = FieldParser(data={"value": value}).parse_value()
    assert actual_value == expected_value, "Wrong value"


def test_unobtainable_title():
    """Test that ValueError is raised if title can't be retrieved from field data.

    1. Create a field parser for a non-subscriptable object.
    2. Try to call parse_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        FieldParser(data=None).parse_title()

    assert error_info.value.args[0] == "Failed to get title from field data", "Wrong error"


def test_missing_title():
    """Test that None is returned if field data don't have 'title' key.

    1. Create a field parser for a dictionary without title.
    2. Parse title.
    3. Check that None is returned.
    """
    actual_title = FieldParser(data={}).parse_title()
    assert actual_title is None, "Wrong title"


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
    """Test that title is properly parsed.

    1. Create a field parser for dictionary with specific title.
    2. Parse a title.
    3. Check the parsed title.
    """
    actual_title = FieldParser(data={"title": title}).parse_title()
    assert actual_title == expected_title, "Wrong title"


def test_field_creation_error():
    """Test that ValueError is raised if an error occurs during field creation.

    1. Create a field parser.
    2. Replace parse_input_type method so that it returns invalid input type.
    3. Try to call parse method.
    4. Check that ValueError is raised.
    5. Check the error message.
    """
    field_data = {
        "name": "name",
        "classes": [],
        }
    parser = FieldParser(data=field_data)
    parser.parse_input_type = lambda: "invalid input type"

    with pytest.raises(ValueError) as error_info:
        parser.parse()

    assert error_info.value.args[0] == "Failed to create a field with provided data", "Wrong error"


def test_parse(component_validator):
    """Test that field data is properly parsed.

    1. Create a field.
    2. Create a field parser.
    3. Replace parser methods so that they return predefined data.
    4. Parse the field.
    5. Check the parsed data.
    """
    field = Field(
        name="parsed name",
        classes=("parsed class 1", "parsed class 2"),
        input_type=InputType.HIDDEN,
        value="parsed value",
        title="parsed title",
        )

    parser = FieldParser(data={})
    parser.parse_name = lambda: field.name
    parser.parse_classes = lambda: field.classes
    parser.parse_input_type = lambda: field.input_type
    parser.parse_value = lambda: field.value
    parser.parse_title = lambda: field.title

    actual_field = parser.parse()
    component_validator.validate_field(actual_field, field)
