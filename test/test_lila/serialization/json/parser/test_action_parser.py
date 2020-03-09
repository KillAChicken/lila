"""Test cases for a parser class for action data."""

import random

import pytest

from lila.core.field import Field
from lila.core.action import Action, Method
from lila.serialization.json.parser import JSONParser
from lila.serialization.json.action import ActionParser


def test_unobtainable_name():
    """Test that ValueError is raised if name can't be retrieved from action data.

    1. Create an action parser for a non-subscriptable object.
    2. Try to call parse_name method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data=None, parser=JSONParser()).parse_name()

    assert error_info.value.args[0] == "Failed to get name from action data", "Wrong error"


def test_missing_name():
    """Test that ValueError is raised if action data don't contain 'name' key.

    1. Create an action parser for a dictionary without name.
    2. Try to call parse_name method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data={}, parser=JSONParser()).parse_name()

    assert error_info.value.args[0] == "Action data do not have required 'name' key", "Wrong error"


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

    1. Create an action parser for dictionary with specific name.
    2. Parse a name.
    3. Check the parsed name.
    """
    actual_name = ActionParser(data={"name": name}, parser=JSONParser()).parse_name()
    assert actual_name == expected_name, "Wrong name"


def test_unobtainable_classes():
    """Test that ValueError is raised if classes can't be retrieved from action data.

    1. Create an action parser for a non-subscriptable object.
    2. Try to call parse_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data=None, parser=JSONParser()).parse_classes()

    assert error_info.value.args[0] == "Failed to get classes from action data", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if action data has a non-iterable object for classes.

    1. Create an action parser for a dictionary with non-iterable classes.
    2. Try to call parse_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data={"class": None}, parser=JSONParser()).parse_classes()

    assert error_info.value.args[0] == "Failed to iterate over classes from action data", (
        "Wrong error"
        )


def test_missing_classes():
    """Test that empty tuple is returned if action data don't have 'class' key.

    1. Create an action parser for a dictionary without classes.
    2. Parse classes.
    3. Check that empty tuple is returned.
    """
    actual_classes = ActionParser(data={}, parser=JSONParser()).parse_classes()
    assert actual_classes == (), "Wrong classes"


@pytest.mark.parametrize(
    argnames="classes,expected_classes",
    argvalues=[
        ([], ()),
        (["action class"], ("action class", )),
        (
            ["first action class", "second action class"],
            ("first action class", "second action class"),
            ),
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

    1. Create an action parser for a dictionary with specific classes.
    2. Parse classes.
    3. Check the parsed classes.
    """
    actual_classes = ActionParser(data={"class": classes}, parser=JSONParser()).parse_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_unobtainable_method():
    """Test that ValueError is raised if method can't be retrieved from action data.

    1. Create an action parser for a non-subscriptable object.
    2. Try to call parse_method method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data=None, parser=JSONParser()).parse_method()

    assert error_info.value.args[0] == "Failed to get method from action data", "Wrong error"


def test_not_supported_method():
    """Test that ValueError is raised if method is not supported.

    1. Create an action parser for a dictionary with not supported value for method.
    2. Try to call parse_method method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data={"method": "invalid method"}, parser=JSONParser()).parse_method()

    assert error_info.value.args[0] == "Action data contain not supported method", "Wrong error"


def test_missing_method():
    """Test that GET method is returned if action data don't have 'method' key.

    1. Create an action parser for a dictionary without method.
    2. Parse method.
    3. Check that GET method is returned.
    """
    actual_method = ActionParser(data={}, parser=JSONParser()).parse_method()
    assert actual_method == Method.GET, "Wrong method"


def test_method():
    """Test that method are properly parsed.

    1. Create an action parser for a dictionary with specific method.
    2. Parse method.
    3. Check the parsed method.
    """
    method = random.choice(list(Method))
    actual_method = ActionParser(data={"method": method.value}, parser=JSONParser()).parse_method()
    assert actual_method == method, "Wrong method"


def test_unobtainable_target():
    """Test that ValueError is raised if target can't be retrieved from action data.

    1. Create an action parser for a non-subscriptable object.
    2. Try to call parse_target method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data=None, parser=JSONParser()).parse_target()

    assert error_info.value.args[0] == "Failed to get target from action data", "Wrong error"


def test_missing_target():
    """Test that ValueError is raised if action data don't contain 'href' key.

    1. Create an action parser for a dictionary without target.
    2. Try to call parse_target method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data={}, parser=JSONParser()).parse_target()

    assert error_info.value.args[0] == "Action data do not have required 'href' key", "Wrong error"


@pytest.mark.parametrize(
    argnames="target,expected_target",
    argvalues=[
        ("/target", "/target"),
        ("", ""),
        (None, "None"),
        ],
    ids=[
        "Simple",
        "Empty",
        "None",
        ],
    )
def test_target(target, expected_target):
    """Test that target is properly parsed.

    1. Create an action parser for dictionary with specific target.
    2. Parse a target.
    3. Check the parsed target.
    """
    actual_target = ActionParser(data={"href": target}, parser=JSONParser()).parse_target()
    assert actual_target == expected_target, "Wrong target"


def test_unobtainable_title():
    """Test that ValueError is raised if title can't be retrieved from action data.

    1. Create an action parser for a non-subscriptable object.
    2. Try to call parse_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data=None, parser=JSONParser()).parse_title()

    assert error_info.value.args[0] == "Failed to get title from action data", "Wrong error"


def test_missing_title():
    """Test that None is returned if action data don't have 'title' key.

    1. Create an action parser for a dictionary without title.
    2. Parse title.
    3. Check that None is returned.
    """
    actual_title = ActionParser(data={}, parser=JSONParser()).parse_title()
    assert actual_title is None, "Wrong title"


@pytest.mark.parametrize(
    argnames="title,expected_title",
    argvalues=[
        ("action title", "action title"),
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

    1. Create an action parser for dictionary with specific title.
    2. Parse a title.
    3. Check the parsed title.
    """
    actual_title = ActionParser(data={"title": title}, parser=JSONParser()).parse_title()
    assert actual_title == expected_title, "Wrong title"


def test_unobtainable_fields():
    """Test that ValueError is raised if fields data can't be retrieved from action data.

    1. Create an action parser for a non-subscriptable object.
    2. Try to call parse_fields method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data=None, parser=JSONParser()).parse_fields()

    assert error_info.value.args[0] == "Failed to get fields data from action data", "Wrong error"


def test_non_iterable_fields():
    """Test that ValueError is raised if action data has a non-iterable object for fields.

    1. Create an action parser for a dictionary with non-iterable fields data.
    2. Try to call parse_fields method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data={"fields": None}, parser=JSONParser()).parse_fields()

    assert error_info.value.args[0] == "Failed to iterate over fields data from action data", (
        "Wrong error"
        )


def test_missing_fields():
    """Test that empty tuple is returned if action data don't have 'fields' key.

    1. Create an action parser for a dictionary without fields.
    2. Parse fields.
    3. Check that empty tuple is returned.
    """
    actual_fields = ActionParser(data={}, parser=JSONParser()).parse_fields()
    assert actual_fields == (), "Wrong fields"


def test_non_parsable_fields():
    """Test that ValueError is raised if one of fields can't be parsed.

    1. Create json parser that raises exception when parse_field method is called.
    2. Create an action parser with the json parser.
    3. Try to call parse_fields method.
    4. Check that ValueError is raised.
    5. Check the error message.
    """
    class _FieldErrorParser(JSONParser):
        def parse_field(self, data):
            raise Exception()

    with pytest.raises(ValueError) as error_info:
        ActionParser(data={"fields": [{}]}, parser=_FieldErrorParser()).parse_fields()

    assert error_info.value.args[0] == "Failed to parse action's fields", "Wrong error"


@pytest.mark.parametrize(
    argnames="fields_data",
    argvalues=[
        [],
        [{"id": "single"}],
        [{"id": "first"}, {"id": "second"}],
        ],
    ids=[
        "Empty list",
        "Single field",
        "Multiple fields",
        ],
    )
def test_fields(fields_data):
    """Test that fields are properly parsed.

    1. Create an action parser.
    2. Replace parse_field of the json parser so that it returns fake data.
    3. Parse fields.
    4. Check the parsed fields.
    """
    json_parser = JSONParser()
    json_parser.parse_field = fields_data.index

    actual_fields = ActionParser(data={"fields": fields_data}, parser=json_parser).parse_fields()
    assert actual_fields == tuple(range(len(fields_data))), "Wrong fields"


def test_unobtainable_encoding_type():
    """Test that ValueError is raised if encoding type can't be retrieved from action data.

    1. Create an action parser for a non-subscriptable object.
    2. Try to call parse_encoding_type method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        ActionParser(data=None, parser=JSONParser()).parse_encoding_type()

    assert error_info.value.args[0] == "Failed to get encoding type from action data", "Wrong error"


@pytest.mark.parametrize(
    argnames="parsed_fields,expected_encoding_type",
    argvalues=[
        [(), None],
        [(Field(name="name"), ), "application/x-www-form-urlencoded"],
        ],
    ids=[
        "Without fields",
        "With fields",
        ],
    )
def test_missing_encoding_type(parsed_fields, expected_encoding_type):
    """Test that None is returned if action data don't have 'type' key.

    1. Create an action parser for a dictionary without encoding type.
    2. Replace parse_fields of the parser so that it returns predefined parsed fields.
    3. Parse encoding type.
    3. Check that default value is returned.
    """
    parser = ActionParser(data={}, parser=JSONParser())
    parser.parse_fields = lambda: parsed_fields

    actual_encoding_type = parser.parse_encoding_type()
    assert actual_encoding_type == expected_encoding_type, "Wrong encoding type"


@pytest.mark.parametrize(
    argnames="encoding_type,parsed_fields,expected_encoding_type",
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
def test_encoding_type(encoding_type, parsed_fields, expected_encoding_type):
    """Test that encoding type is properly parsed.

    1. Create an action parser for a dictionary with specific encoding type.
    2. Replace parse_fields of the parser so that it returns predefined parsed fields.
    3. Parse encoding type.
    3. Check parsed encoding type.
    """
    parser = ActionParser(data={"type": encoding_type}, parser=JSONParser())
    parser.parse_fields = lambda: parsed_fields

    actual_encoding_type = parser.parse_encoding_type()
    assert actual_encoding_type == expected_encoding_type, "Wrong encoding type"


def test_parse(component_validator):
    """Test that action data is properly parsed.

    1. Create an action.
    2. Create an action parser.
    3. Replace parser methods so that they return predefined data.
    4. Parse the action.
    5. Check the parsed data.
    """
    action = Action(
        name="parsed name",
        classes=("parsed class 1", "parsed class 2"),
        method=Method.PUT,
        target="/parsed/target",
        title="parsed title",
        encoding_type="application/parsed+type",
        fields=(Field(name="first"), Field(name="second")),
        )

    parser = ActionParser(data={}, parser=JSONParser())
    parser.parse_name = lambda: action.name
    parser.parse_classes = lambda: action.classes
    parser.parse_method = lambda: action.method
    parser.parse_target = lambda: action.target
    parser.parse_title = lambda: action.title
    parser.parse_encoding_type = lambda: action.encoding_type
    parser.parse_fields = lambda: action.fields

    actual_action = parser.parse()
    component_validator.validate_action(actual_action, action)
