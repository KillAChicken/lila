"""Test cases for parse_field method of JSON parser."""

import random

import pytest

from lila.core.field import InputType
from lila.serialization.json.parser import JSONParser


def test_invalid_json():
    """Test that ValueError is raised if input data are not a valid JSON object.

    1. Create a json parser.
    2. Try to call parse_field method with object() as data.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_field(data=object())

    assert error_info.value.args[0] == "Specified data are not a valid JSON object", "Wrong error"


@pytest.mark.parametrize(
    argnames="name",
    argvalues=[
        "simple name",
        u"Имя на русском",
        "",
        ],
    ids=[
        "Simple",
        "Unicode",
        "Empty",
        ],
    )
def test_name(json_data_factory, name):
    """Test that name is properly parsed.

    1. Create a json parser.
    2. Parse a field from a dictionary with a specific name.
    3. Check name of the parsed field.
    """
    field_data = json_data_factory.create_field_data(name=name)
    field = JSONParser().parse_field(field_data)

    assert field.name == name, "Wrong name"


def test_missing_name(json_data_factory):
    """Test that ValueError is raised if input data don't contain a name.

    1. Create a json parser.
    2. Try to parse a field from a dictionary without 'name' key.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    field_data = json_data_factory.create_field_data(name="name")
    field_data.pop("name", None)

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_field(data=field_data)

    assert error_info.value.args[0] == "Field data do not have required 'name' key", "Wrong error"


@pytest.mark.parametrize(
    argnames="classes",
    argvalues=[
        ("class1", "class2"),
        (),
        ],
    ids=[
        "Simple",
        "Empty",
        ],
    )
def test_classes(json_data_factory, classes):
    """Test that classes are properly parsed.

    1. Create a json parser.
    2. Parse a field from a dictionary with specific classes.
    3. Check classes of the parsed field.
    """
    field_data = json_data_factory.create_field_data(classes=classes)
    field = JSONParser().parse_field(field_data)

    assert field.classes == tuple(classes), "Wrong classes"


def test_missing_classes(json_data_factory):
    """Test that field can be parsed if classes are not specified.

    1. Create a json parser.
    2. Parse a field from a dictionary without 'class' key.
    3. Check that parsed field has empty list of classes.
    """
    field_data = json_data_factory.create_field_data(classes=["class"])
    field_data.pop("class", None)
    field = JSONParser().parse_field(field_data)

    assert field.classes == (), "Wrong classes"


def test_input_type(json_data_factory):
    """Test that input type is properly parsed.

    1. Create a json parser.
    2. Parse a field from a dictionary with specific input type.
    3. Check input type of the parsed field.
    """
    input_type = random.choice(list(InputType))
    field_data = json_data_factory.create_field_data(input_type=input_type)
    field = JSONParser().parse_field(field_data)

    assert field.input_type == input_type, "Wrong input type"


def test_missing_input_type(json_data_factory):
    """Test that field can be parsed if input type is not specified.

    1. Create a json parser.
    2. Parse a field from a dictionary without 'type' key.
    3. Check input type of the parsed field.
    """
    field_data = json_data_factory.create_field_data(input_type=InputType.HIDDEN)
    field_data.pop("type", None)
    field = JSONParser().parse_field(field_data)

    assert field.input_type == InputType.TEXT, "Wrong input type"


def test_invalid_input_type(json_data_factory):
    """Test that ValueError is raised if input type is invalid.

    1. Create a json parser.
    2. Try to parse a field from a dictionary with invalid value for input type.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    field_data = json_data_factory.create_field_data()
    field_data["type"] = "fake input value"

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_field(field_data)

    assert error_info.value.args[0] == "Unsupported input type is specified", "Wrong error"


@pytest.mark.parametrize(
    argnames="value,expected_value",
    argvalues=[
        ("simple value", "simple value"),
        (u"Значение", u"Значение"),
        ("", ""),
        (1, "1"),
        (None, None),
        ],
    ids=[
        "Simple string",
        "Unicode string",
        "Empty string",
        "Integer",
        "None",
        ],
    )
def test_value(json_data_factory, value, expected_value):
    """Test that value is properly parsed.

    1. Create a json parser.
    2. Parse a field from a dictionary with a specific value.
    3. Check the value of the parsed field.
    """
    field_data = json_data_factory.create_field_data(value=value)
    field = JSONParser().parse_field(field_data)

    assert field.value == expected_value, "Wrong value"


def test_missing_value(json_data_factory):
    """Test that field can be parsed if value is not specified.

    1. Create a json parser.
    2. Parse a field from a dictionary without 'value' key.
    3. Check that parsed field has None as a value.
    """
    field_data = json_data_factory.create_field_data(value="value")
    field_data.pop("value", None)
    field = JSONParser().parse_field(field_data)

    assert field.value is None, "Wrong value"


@pytest.mark.parametrize(
    argnames="title",
    argvalues=[
        "simple title",
        u"Заголовок",
        "",
        None,
        ],
    ids=[
        "Simple",
        "Unicode",
        "Empty",
        "None",
        ],
    )
def test_title(json_data_factory, title):
    """Test that title is properly parsed.

    1. Create a json parser.
    2. Parse a field from a dictionary with a specific title.
    3. Check the title of the parsed field.
    """
    field_data = json_data_factory.create_field_data(title=title)
    field = JSONParser().parse_field(field_data)

    assert field.title == title, "Wrong title"


def test_missing_title(json_data_factory):
    """Test that field can be parsed if title is not specified.

    1. Create a json parser.
    2. Parse a field from a dictionary without 'title' key.
    3. Check that parsed field has None as a title.
    """
    field_data = json_data_factory.create_field_data(title="title")
    field_data.pop("title", None)
    field = JSONParser().parse_field(field_data)

    assert field.title is None, "Wrong title"


def test_creation_error(json_data_factory, monkeypatch):
    """Test that ValueError from Field creation is reraised by parser.

    1. Create a json parser.
    2. Try to parse a field from a dictionary causing ValueError during the creation of
       an instance of Field class.
    3. Check that ValueError is raised.
    """
    # ValueError is not raised at the moment during Field creation,
    # so we mock this behavior with another class
    expected_error = ValueError("Field error")

    class _FakeField:
        # pylint: disable=too-few-public-methods
        def __init__(self, *args, **kwargs):
            raise expected_error

    import lila.serialization.json.parser as json_parser_module     # pylint: disable=import-outside-toplevel
    monkeypatch.setattr(json_parser_module, "Field", _FakeField)

    field_data = json_data_factory.create_field_data()
    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_field(field_data)

    assert error_info.value is expected_error, "Wrong error"
