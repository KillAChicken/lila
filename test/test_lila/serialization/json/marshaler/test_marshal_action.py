"""Test cases for marshal_action method of JSON marshaler."""

import random

import pytest

from lila.core.field import Field
from lila.core.action import Action, Method
from lila.serialization.json.marshaler import JSONMarshaler


def test_missing_name():
    """Test that ValueError is raised if an action does not have name attribute.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object without name attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingNameAction(Action):
        @property
        def name(self):
            raise AttributeError()

    action = _MissingNameAction(name="no name", target="/no/name")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

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

    1. Create a json marshaler.
    2. Marshal an action with a specific name.
    3. Check a key with the name in the marshaled data.
    """
    class _FixedNameAction(Action):
        @property
        def name(self):
            return name

    action = _FixedNameAction(name="fixed name", target="/fixed/name")

    action_data = JSONMarshaler().marshal_action(action=action)
    assert "name" in action_data, "Marshaled data does not have 'name' key"
    assert action_data["name"] == expected_name, "Wrong name"


def test_missing_classes():
    """Test that ValueError is raised if an action does not have classes attribute.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object without classes attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingClassesAction(Action):
        @property
        def classes(self):
            raise AttributeError()

    action = _MissingClassesAction(name="no classes", target="/no/classes")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

    assert error_info.value.args[0] == "Failed to get action's classes", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if action provides a non-iterable object as its classes.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object with non-iterable classes.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableClassesAction(Action):
        @property
        def classes(self):
            return None

    action = _NonIterableClassesAction(
        name="'classes' attribute is not iterable",
        target="/classes-are-not-iterable",
        )

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

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

    1. Create a json marshaler.
    2. Marshal an action with specific classes.
    3. Check a key with the classes in the marshaled data.
    """
    class _FixedClassesAction(Action):
        @property
        def classes(self):
            return classes

    action = _FixedClassesAction(name="fixed classes", target="/test/classes")

    action_data = JSONMarshaler().marshal_action(action=action)
    assert "class" in action_data, "Marshaled data does not have 'class' key"
    assert action_data["class"] == expected_classes, "Wrong classes"


def test_missing_method():
    """Test that ValueError is raised if an aciton does not have method attribute.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object without method attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingMethodAction(Action):
        @property
        def method(self):
            raise AttributeError()

    action = _MissingMethodAction(name="no method", target="/missing/method")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

    assert error_info.value.args[0] == "Failed to get action's method", "Wrong error"


def test_not_supported_method():
    """Test that ValueError is raised if method of the action is not supported.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object with unsupported method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NotSupportedMethodAction(Action):
        @property
        def method(self):
            return "GET"

    action = _NotSupportedMethodAction(name="Method is not supported", target="/unsupported-method")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

    assert error_info.value.args[0] == "Action's method is not supported", "Wrong error"


def test_method():
    """Test that method is properly marshaled.

    1. Create a json marshaler.
    2. Marshal an action with a specific method.
    3. Check a key with the method in the marshaled data.
    """
    method = random.choice(list(Method))
    action = Action(name="fixed method", target="/fixed/method", method=method)

    action_data = JSONMarshaler().marshal_action(action=action)
    assert "method" in action_data, "Marshaled data does not have 'method' key"
    assert action_data["method"] == method.value, "Wrong method"


def test_missing_target():
    """Test that ValueError is raised if an action does not have target attribute.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object without target attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTargetAction(Action):
        @property
        def target(self):
            raise AttributeError()

    action = _MissingTargetAction(name="no target", target="/no/target")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

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

    1. Create a json marshaler.
    2. Marshal an action with a specific target.
    3. Check a key with the target in the marshaled data.
    """
    class _FixedTargetAction(Action):
        @property
        def target(self):
            return target

    action = _FixedTargetAction(name="fixed target", target="/fixed/target")

    action_data = JSONMarshaler().marshal_action(action=action)
    assert "href" in action_data, "Marshaled data does not have 'href' key"
    assert action_data["href"] == expected_target, "Wrong target"


def test_missing_title():
    """Test that ValueError is raised if an action does not have title attribute.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object without title attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTitleAction(Action):
        @property
        def title(self):
            raise AttributeError()

    action = _MissingTitleAction(name="no title", target="/no/title")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

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

    1. Create a json marshaler.
    2. Marshal an action with a specific title.
    3. Check a key with the title in the marshaled data.
    """
    class _FixedTitleAction(Action):
        @property
        def title(self):
            return title

    action = _FixedTitleAction(name="fixed title", target="/fixed-title")

    action_data = JSONMarshaler().marshal_action(action=action)
    assert "title" in action_data, "Marshaled data does not have 'title' key"
    assert action_data["title"] == expected_title, "Wrong title"


def test_missing_encoding_type():
    """Test that ValueError is raised if an action does not have encoding type attribute.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object without encoding type attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingEncodingTypeAction(Action):
        @property
        def encoding_type(self):
            raise AttributeError()

    action = _MissingEncodingTypeAction(name="no encoding type", target="/no/encoding/type")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

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

    1. Create a json marshaler.
    2. Marshal an action with a specific encoding type.
    3. Check a key with the encoding type in the marshaled data.
    """
    class _FixedEncodingTypeAction(Action):
        @property
        def encoding_type(self):
            return encoding_type

    action = _FixedEncodingTypeAction(name="fixed encoding type", target="/fixed-encoding-type")

    action_data = JSONMarshaler().marshal_action(action=action)
    assert "type" in action_data, "Marshaled data does not have 'type' key"
    assert action_data["type"] == expected_encoding_type, "Wrong encoding type"


def test_missing_fields():
    """Test that ValueError is raised if an action does not have fields attribute.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object without fields attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingFieldsAction(Action):
        @property
        def fields(self):
            raise AttributeError()

    action = _MissingFieldsAction(name="no fields", target="/no/fields")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

    assert error_info.value.args[0] == "Failed to get action's fields", "Wrong error"


def test_non_iterable_fields():
    """Test that ValueError is raised if action provides a non-iterable object as its fields.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object with non-iterable fields.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableFieldsAction(Action):
        @property
        def fields(self):
            return None

    action = _NonIterableFieldsAction(
        name="'fields' attribute is not iterable",
        target="/fields-are-not-iterable",
        )

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

    assert error_info.value.args[0] == "Failed to iterate over action's fields", "Wrong error"


def test_non_marshalable_fields():
    """Test that ValueError is raised if one of action fields is not marshallable.

    1. Create a json marshaller.
    2. Try to call marshal_action method for an object with fields that are not marshalable.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonMarshalableFieldsAction(Action):
        @property
        def fields(self):
            return [Field(name="first"), None, Field(name="last")]

    action = _NonMarshalableFieldsAction(
        name="one of fields is not marshalable",
        target="/fields-are-not-marshalable",
        )

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_action(action=action)

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

    1. Create a json marshaler.
    2. Replace marshal_field of the marshaler so that it returns fake data.
    3. Marshal an action with specific fields.
    4. Check a key with the fields (fake data) in the marshaled data.
    """
    class _FixedFieldsAction(Action):
        @property
        def fields(self):
            return fields

    action = _FixedFieldsAction(name="fixed fields", target="/test/fields")

    marshaler = JSONMarshaler()
    marshaler.marshal_field = fields.index

    action_data = marshaler.marshal_action(action=action)
    assert "fields" in action_data, "Marshaled data does not have 'fields' key"
    assert action_data["fields"] == list(range(len(fields))), "Wrong fields"
