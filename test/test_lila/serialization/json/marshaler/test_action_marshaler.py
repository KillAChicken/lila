"""Test cases for a marshaler class for an action."""

import random
from collections import namedtuple

import pytest

from lila.core.field import Field
from lila.core.action import Action, Method
from lila.serialization.json.marshaler import JSONMarshaler
from lila.serialization.json.action import ActionMarshaler


def test_missing_name():
    """Test that ValueError is raised if an action does not have name attribute.

    1. Create an action marshaler for an object without name attibute.
    2. Try to call marshal_name method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_name()

    assert error_info.value.args[0] == "Failed to get action's name", "Wrong error"


@pytest.mark.parametrize(
    argnames="name,expected_name",
    argvalues=[
        ("name", "name"),
        (u"Русское имя", u"Русское имя"),
        ("", ""),
        (None, "None"),
        ([1, 2], "[1, 2]"),
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

    1. Create an action marshaler for an object with specific name.
    2. Marshal action's name.
    3. Check the marshaled name.
    """
    NameAction = namedtuple("NameAction", "name")
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=NameAction(name=name))
    actual_name = marshaler.marshal_name()
    assert actual_name == expected_name, "Wrong name"


def test_missing_classes():
    """Test that ValueError is raised if an action does not have classes attribute.

    1. Create an action marshaler for an object without classes attribute.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_classes()

    assert error_info.value.args[0] == "Failed to get action's classes", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if an action provides a non-iterable object as its classes.

    1. Create an action marshaler for an object with non-iterable classes.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    ClassesAction = namedtuple("ClassesAction", "classes")
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=ClassesAction(classes=None))
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_classes()

    assert error_info.value.args[0] == "Failed to iterate over action's classes", "Wrong error"


@pytest.mark.parametrize(
    argnames="classes,expected_classes",
    argvalues=[
        ([], []),
        (["action class"], ["action class"]),
        (
            ["first action class", "second action class"],
            ["first action class", "second action class"],
            ),
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

    1. Create an action marshaler for an object with specific classes.
    2. Marshal classes.
    3. Check the marshaled classes.
    """
    ClassesAction = namedtuple("ClassesAction", "classes")
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=ClassesAction(classes=classes))

    actual_classes = marshaler.marshal_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_missing_method():
    """Test that ValueError is raised if an action does not have input type attribute.

    1. Create an action marshaler for an object without method.
    2. Try to call marshal_method method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_method()

    assert error_info.value.args[0] == "Failed to get action's method", "Wrong error"


def test_not_supported_method():
    """Test that ValueError is raised if method of an action is not supported.

    1. Create an action marshaler for an object with unsupported method.
    2. Try to call marshal_method method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    MethodAction = namedtuple("MethodAction", "method")
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=MethodAction(method="get"))
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_method()

    assert error_info.value.args[0] == "Action's method is not supported", "Wrong error"


@pytest.mark.parametrize(
    argnames="method",
    argvalues=[
        random.choice(list(Method)),
        random.choice(list(Method)).value,
        ],
    ids=[
        "Enumeration item",
        "String",
        ],
    )
def test_method(method):
    """Test that method is properly marshaled.

    1. Create an action marshaler for an object with specific method.
    2. Marshal action's method.
    3. Check the marshaled method.
    """
    MethodAction = namedtuple("MethodAction", "method")
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=MethodAction(method=method))

    actual_method = marshaler.marshal_method()
    assert actual_method == Method(method).value, "Wrong method"


def test_missing_target():
    """Test that ValueError is raised if an action does not have target attribute.

    1. Create an action marshaler for an object without target attibute.
    2. Try to call marshal_target method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_target()

    assert error_info.value.args[0] == "Failed to get action's target", "Wrong error"


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
    """Test that target is properly marshaled.

    1. Create an action marshaler for an object with specific target.
    2. Marshal action's target.
    3. Check the marshaled target.
    """
    TargetAction = namedtuple("TargetAction", "target")
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=TargetAction(target=target))

    actual_target = marshaler.marshal_target()
    assert actual_target == expected_target, "Wrong target"


def test_missing_title():
    """Test that ValueError is raised if an action does not have title attribute.

    1. Create an action marshaler for an object without title attibute.
    2. Try to call marshal_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_title()

    assert error_info.value.args[0] == "Failed to get action's title", "Wrong error"


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
    """Test that title is properly marshaled.

    1. Create an action marshaler for an object with specific title.
    2. Marshal action's title.
    3. Check the marshaled title.
    """
    TitleAction = namedtuple("TitleAction", "title")
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=TitleAction(title=title))

    actual_title = marshaler.marshal_title()
    assert actual_title == expected_title, "Wrong title"


def test_missing_encoding_type():
    """Test that ValueError is raised if an action does not have encoding type attribute.

    1. Create an action marshaler for an object without encoding type attibute.
    2. Try to call marshal_encoding_type method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_encoding_type()

    assert error_info.value.args[0] == "Failed to get action's encoding type", "Wrong error"


@pytest.mark.parametrize(
    argnames="encoding_type,expected_encoding_type",
    argvalues=[
        ("application/x-www-form-urlencoded", "application/x-www-form-urlencoded"),
        (None, None),
        ],
    ids=[
        "Simple",
        "None",
        ],
    )
def test_encoding_type(encoding_type, expected_encoding_type):
    """Test that encoding type is properly marshaled.

    1. Create an action marshaler for an object with specific encoding type.
    2. Marshal action's encoding type.
    3. Check the marshaled encoding type.
    """
    EncodingTypeAction = namedtuple("EncodingTypeAction", "encoding_type")
    marshaler = ActionMarshaler(
        marshaler=JSONMarshaler(),
        action=EncodingTypeAction(encoding_type=encoding_type),
        )

    actual_encoding_type = marshaler.marshal_encoding_type()
    assert actual_encoding_type == expected_encoding_type, "Wrong encoding type"


def test_missing_fields():
    """Test that ValueError is raised if an action does not have fields attribute.

    1. Create an action marshaler for an object without fields attibute.
    2. Try to call marshal_fields method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_fields()

    assert error_info.value.args[0] == "Failed to get action's fields", "Wrong error"


def test_non_iterable_fields():
    """Test that ValueError is raised if an action provides a non-iterable object as its fields.

    1. Create an action marshaler for an object with non-iterable fields.
    2. Try to call marshal_fields.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    FieldsAction = namedtuple("FieldsAction", "fields")
    marshaler = ActionMarshaler(marshaler=JSONMarshaler(), action=FieldsAction(fields=None))
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_fields()

    assert error_info.value.args[0] == "Failed to iterate over action's fields", "Wrong error"


def test_non_marshalable_fields():
    """Test that ValueError is raised if one of action fields is not marshallable.

    1. Create an action marshaler for an object with fields that are not marshalable.
    2. Try to call marshal_fields method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    FieldsAction = namedtuple("FieldsAction", "fields")
    marshaler = ActionMarshaler(
        marshaler=JSONMarshaler(),
        action=FieldsAction(fields=[Field(name="first"), None, Field(name="last")]),
        )

    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_fields()

    assert error_info.value.args[0] == "Failed to marshal action's fields", "Wrong error"


@pytest.mark.parametrize(
    argnames="fields",
    argvalues=[
        [],
        [Field(name="single field")],
        [Field(name="first"), Field(name="second")],
        ],
    ids=[
        "Empty list",
        "Single field",
        "Multiple fields",
        ],
    )
def test_fields(fields):
    """Test that fields are properly marshaled.

    1. Create an action marshaler.
    2. Replace marshal_field of the marshaler so that it returns fake data.
    3. Marshal fields.
    4. Check the marshaled fields.
    """
    json_marshaler = JSONMarshaler()
    json_marshaler.marshal_field = fields.index

    FieldsAction = namedtuple("FieldsAction", "fields")
    marshaler = ActionMarshaler(marshaler=json_marshaler, action=FieldsAction(fields=fields))

    actual_data = marshaler.marshal_fields()
    assert actual_data == list(range(len(fields))), "Wrong fields"


def test_marshal():
    """Test that action data is properly marshaled.

    1. Create an action.
    2. Create an action marshaler for the action.
    3. Replace marshaler methods so that they return predefined data.
    4. Marshal the action.
    5. Check the marshaled data.
    """
    marshaler = ActionMarshaler(
        marshaler=JSONMarshaler(),
        action=Action(name="action", target="/target"),
        )
    marshaler.marshal_name = lambda: "marshal_name"
    marshaler.marshal_classes = lambda: "marshal_classes"
    marshaler.marshal_method = lambda: "marshal_method"
    marshaler.marshal_target = lambda: "marshal_target"
    marshaler.marshal_title = lambda: "marshal_title"
    marshaler.marshal_encoding_type = lambda: "marshal_encoding_type"
    marshaler.marshal_fields = lambda: "marshal_fields"

    actual_data = marshaler.marshal()
    expected_data = {
        "name": "marshal_name",
        "class": "marshal_classes",
        "method": "marshal_method",
        "href": "marshal_target",
        "title": "marshal_title",
        "type": "marshal_encoding_type",
        "fields": "marshal_fields",
        }
    assert actual_data == expected_data, "Action is not properly marshaled"
