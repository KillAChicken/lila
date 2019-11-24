"""Test cases for parse_action method of JSON parser."""

from copy import deepcopy
import random

import pytest

from lila.core.field import Field
from lila.core.action import Method, Action
from lila.serialization.json.parser import JSONParser


def test_invalid_json():
    """Test that ValueError is raised if input data are not a valid JSON object.

    1. Create a json parser.
    2. Try to call parse_action method with object() as data.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_action(data=object())

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
    2. Parse an action from a dictionary with a specific name.
    3. Check name of the parsed action.
    """
    action_data = json_data_factory.create_action_data(name=name)
    action = JSONParser().parse_action(action_data)

    assert action.name == name, "Wrong name"


def test_missing_name(json_data_factory):
    """Test that ValueError is raised if input data don't contain a name.

    1. Create a json parser.
    2. Try to parse an action from a dictionary without 'name' key.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    action_data = json_data_factory.create_action_data(name="name")
    action_data.pop("name", None)

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_action(data=action_data)

    assert error_info.value.args[0] == "Action data do not have required 'name' key", "Wrong error"


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
    2. Parse an action from a dictionary with specific classes.
    3. Check classes of the parsed action.
    """
    action_data = json_data_factory.create_action_data(classes=classes)
    action = JSONParser().parse_action(action_data)

    assert action.classes == tuple(classes), "Wrong classes"


def test_missing_classes(json_data_factory):
    """Test that action can be parsed if classes are not specified.

    1. Create a json parser.
    2. Parse an action from a dictionary without 'class' key.
    3. Check that parsed action has empty list of classes.
    """
    action_data = json_data_factory.create_action_data(classes=["class"])
    action_data.pop("class", None)
    action = JSONParser().parse_action(action_data)

    assert action.classes == (), "Wrong classes"


def test_method(json_data_factory):
    """Test that method is properly parsed.

    1. Create a json parser.
    2. Parse an action from a dictionary with a specific method.
    3. Check method of the parsed action.
    """
    method = random.choice(list(Method))
    action_data = json_data_factory.create_action_data(method=method)
    action = JSONParser().parse_action(action_data)

    assert action.method == method, "Wrong method"


def test_missing_method(json_data_factory):
    """Test that action can be parsed if method is not specified.

    1. Create a json parser.
    2. Parse an action from a dictionary without 'method' key.
    3. Check that parsed action has GET as an action.
    """
    action_data = json_data_factory.create_action_data(method=Method.POST)
    action_data.pop("method", None)
    action = JSONParser().parse_action(action_data)

    assert action.method == Method.GET, "Wrong method"


def test_invalid_method(json_data_factory):
    """Test that ValueError is raised if method is invalid.

    1. Create a json parser.
    2. Try to parse an action from a dictionary with invalid value for method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    action_data = json_data_factory.create_action_data()
    action_data["method"] = "fake method"

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_action(action_data)

    assert error_info.value.args[0] == "Unsupported method is specified", "Wrong error"


@pytest.mark.parametrize(
    argnames="target",
    argvalues=[
        "/simple/target",
        ],
    ids=[
        "Simple",
        ],
    )
def test_target(json_data_factory, target):
    """Test that target is properly parsed.

    1. Create a json parser.
    2. Parse an action from a dictionary with a specific target.
    3. Check name of the parsed action.
    """
    action_data = json_data_factory.create_action_data(target=target)
    action = JSONParser().parse_action(action_data)

    assert action.target == target, "Wrong target"


def test_missing_target(json_data_factory):
    """Test that ValueError is raised if input data don't contain a target.

    1. Create a json parser.
    2. Try to parse an action from a dictionary without 'href' key.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    action_data = json_data_factory.create_action_data(target="/target")
    action_data.pop("href", None)

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_action(data=action_data)

    assert error_info.value.args[0] == "Action data do not have required 'href' key", "Wrong error"


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
    2. Parse an action from a dictionary with a specific title.
    3. Check the title of the parsed action.
    """
    action_data = json_data_factory.create_action_data(title=title)
    action = JSONParser().parse_action(action_data)

    assert action.title == title, "Wrong title"


def test_missing_title(json_data_factory):
    """Test that action can be parsed if title is not specified.

    1. Create a json parser.
    2. Parse an action from a dictionary without 'title' key.
    3. Check that parsed action has None as a title.
    """
    action_data = json_data_factory.create_action_data(title="title")
    action_data.pop("title", None)
    action = JSONParser().parse_action(action_data)

    assert action.title is None, "Wrong title"


@pytest.mark.parametrize(
    argnames="encoding_type,fields,expected_encoding_type",
    argvalues=[
        ("application/json", (), "application/json"),
        ("application/json", (Field(name="name"), ), "application/json"),
        (None, (), None),
        (None, (Field(name="name"), ), "application/x-www-form-urlencoded"),
        ],
    ids=[
        "Explicit type without fields",
        "Explicit type with fields",
        "None type without fields",
        "None type with fields",
        ],
    )
def test_encoding_type(json_data_factory, encoding_type, fields, expected_encoding_type):
    """Test that encoding type is properly parsed.

    1. Create a json parser.
    2. Parse an action from a dictionary with specific encoding type and fields.
    3. Check the encoding type of the action.
    """
    action_data = json_data_factory.create_action_data(encoding_type=encoding_type, fields=fields)
    action = JSONParser().parse_action(action_data)

    assert action.encoding_type == expected_encoding_type, "Wrong encoding type"


@pytest.mark.parametrize(
    argnames="fields,expected_encoding_type",
    argvalues=[
        ((), None),
        ((Field(name="name"), ), "application/x-www-form-urlencoded"),
        ],
    ids=[
        "Without fields",
        "With fields",
        ],
    )
def test_missing_encoding_type(json_data_factory, fields, expected_encoding_type):
    """Test that action can be parsed if encoding type is not specified.

    1. Create a json parser.
    2. Parse an action from a dictionary without 'type' key with spefied fields.
    3. Check the encoding type of the action.
    """
    action_data = json_data_factory.create_action_data(
        fields=fields,
        encoding_type="application/xml",
        )
    action_data.pop("type", None)
    action = JSONParser().parse_action(action_data)

    assert action.encoding_type == expected_encoding_type, "Wrong encoding type"


@pytest.mark.parametrize(
    argnames="fields",
    argvalues=[
        (),
        (Field(name="name"), ),
        (Field(name="first"), Field(name="second")),
        ],
    ids=[
        "Without fields",
        "One field",
        "Several fields",
        ],
    )
def test_fields(json_data_factory, fields):
    """Test that fields are properly parsed.

    1. Create a json parser.
    2. Decorate parse_field method of the parser so that passed data and parsed fields are stored.
    3. Parse an action from a dictionary with specific fields.
    4. Check that passed field data are taken from the action data.
    5. Check that fields of the action are the parsed fields.
    """
    action_data = json_data_factory.create_action_data(fields=fields)
    parser = JSONParser()

    parse_field = parser.parse_field

    passed_fields_data = []
    parsed_fields = []

    def _decorated_parse_field(data):
        passed_fields_data.append(deepcopy(data))
        parsed_field = parse_field(data)
        parsed_fields.append(parsed_field)
        return parsed_field

    parser.parse_field = _decorated_parse_field

    # use deepcopy to catch a case when the passed action data is accidentally changed
    action = parser.parse_action(deepcopy(action_data))

    assert passed_fields_data == action_data["fields"], "Wrong data is passed to parse_field method"
    assert action.fields == tuple(parsed_fields), "Wrong fields"


def test_missing_fields(json_data_factory):
    """Test that action can be parsed if fields are not specified.

    1. Create a json parser.
    2. Parse an action from a dictionary without 'fields' key.
    3. Check that parsed action has empty tuple of fields.
    """
    action_data = json_data_factory.create_action_data(fields=[Field(name="name")])
    action_data.pop("fields", None)
    action = JSONParser().parse_action(action_data)

    assert action.fields == (), "Wrong fields"


@pytest.mark.parametrize(
    argnames="invalid_fields_data",
    argvalues=[
        None,
        123,
        [{}],
        ],
    ids=[
        "None",
        "Non-iterable",
        "Invalid field data",
        ],
    )
def test_invalid_fields(json_data_factory, invalid_fields_data):
    """Test that ValueError is raised if fields data is invalid.

    1. Create a json parser.
    2. Try to parse an action from a dictionary with invalid fields data.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    action_data = json_data_factory.create_action_data()
    action_data["fields"] = invalid_fields_data

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_action(data=action_data)

    assert error_info.value.args[0] == "Failed to parse action fields", "Wrong error"


def test_creation_error(json_data_factory):
    """Test that ValueError from Action creation is reraised by parser.

    1. Create a json parser.
    2. Try to parse an action from a dictionary causing ValueError during the creation of
       an instance of Action class.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    action_data = json_data_factory.create_action_data(fields=[Field(name="ignored field")])
    parser = JSONParser()
    parser.parse_field = lambda data: "invalid field"

    with pytest.raises(ValueError) as error_info:
        parser.parse_action(action_data)

    with pytest.raises(ValueError) as expected_error_info:
        Action(name="name", target="/target", fields=["invalid field"])

    assert error_info.value.args[0] == expected_error_info.value.args[0], "Wrong error"
