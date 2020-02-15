"""Test cases for Siren Actions."""

import random

import pytest

from lila.core.action import Method, Action
from lila.core.field import Field


def test_string_method():
    """Check that string representation of Method is its value.

    1. Get a method from the enumeration.
    2. Check that its string representation is equal to its value.
    """
    method = random.choice(list(Method))
    assert str(method) == method.value, "Wrong string representation"


@pytest.mark.parametrize(
    argnames="name, expected_name",
    argvalues=[
        ("action name", "action name"),
        (1, "1"),
        (None, "None"),
    ],
    ids=[
        "String",
        "Integer",
        "None",
    ],
)
def test_name(name, expected_name):
    """Check name of an action.

    1. Create an action with different names.
    2. Get name of the action.
    3. Check the action.
    """
    action = Action(name=name, target="/do-nothing")
    assert action.name == expected_name, "Wrong name"


@pytest.mark.parametrize(
    argnames="target, expected_target",
    argvalues=[
        ("https://example.com/somepath", "https://example.com/somepath"),
        ("/somepath", "/somepath"),
        (None, "None"),
    ],
    ids=[
        "Absolute",
        "Relative",
        "Not string",
    ],
)
def test_target(target, expected_target):
    """Check target of an action.

    1. Create an action with a target.
    2. Get target.
    3. Check the target.
    """
    action = Action(name="test action target", target=target)
    assert action.target == expected_target, "Wrong target"


@pytest.mark.parametrize(
    argnames="classes, expected_classes",
    argvalues=[
        (["action-class1", "action-class2"], ("action-class1", "action-class2")),
    ],
    ids=[
        "Happy path",
    ],
)
def test_classes(classes, expected_classes):
    """Check classes of an action.

    1. Create an action with different classes.
    2. Get classes of the action.
    3. Check the classes.
    """
    action = Action(name="test action classes", target="/test-action-classes", classes=classes)
    assert action.classes == expected_classes, "Wrong classes"


def test_default_classes():
    """Check default classes of an action.

    1. Create an action without specifying classes.
    2. Check classes of the action.
    """
    action = Action(name="test default classes", target="/test-default-clases")
    assert action.classes == (), "Wrong classes"


def test_invalid_classes():
    """Check that ValueError is raised if invalid classes are passed.

    1. Try to create an action with non-iterable classes.
    2. Check that ValueError is raised.
    """
    with pytest.raises(ValueError):
        Action(name="test invalid classes", target="/test-invalid-classes", classes=1)


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
    """Check method of an action.

    1. Create an action with different methods.
    2. Get method of the action.
    3. Check the method.
    """
    action = Action(name="test action method", target="/test-action-method/", method=method)
    assert action.method == Method(method), "Wrong method"


def test_default_method():
    """Check default method of an action.

    1. Create an action without specifying a method.
    2. Get method of the action.
    3. Check the method.
    """
    action = Action(name="test default method", target="/test-default-method/")
    assert action.method == Method.GET, "Wrong method"


@pytest.mark.parametrize(
    argnames="method",
    argvalues=[
        "get",
        None,
    ],
    ids=[
        "Not supported",
        "None",
    ],
)
def test_invalid_method(method):
    """Check that ValueError is raised if an invalid method is passed.

    1. Try to create an action with unsupported method.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        Action(name="test invalid method", target="/test-invalid-method", method=method)

    expected_method = "Method '{0}' is not supported".format(method)
    assert error_info.value.args[0] == expected_method, "Wrong error message"


@pytest.mark.parametrize(
    argnames="title, expected_title",
    argvalues=[
        ("action title", "action title"),
        (None, None),
        (23, "23"),
    ],
    ids=[
        "String",
        "None",
        "Integer",
    ],
)
def test_title(title, expected_title):
    """Check title of an action.

    1. Create an action with different titles.
    2. Get title of the action.
    3. Check the title.
    """
    action = Action(name="test action title", target="/test/action/title", title=title)
    assert action.title == expected_title, "Wrong title"


def test_default_title():
    """Check default title of an action.

    1. Create an action without specifying a title.
    2. Check the title of the action.
    """
    action = Action(name="test default title", target="/test/default/title")
    assert action.title is None, "Wrong title"


@pytest.mark.parametrize(
    argnames="fields",
    argvalues=[
        [],
        [Field(name="single")],
        [Field(name="first"), Field(name="second")],
    ],
    ids=[
        "Without fields",
        "Single",
        "Several",
    ],
)
def test_fields(fields):
    """Check fields of an action.

    1. Create an action with different number of fields.
    2. Get fields of the action.
    3. Check the fields.
    """
    action = Action(name="test action fields", target="/test-action-fields", fields=fields)
    assert action.fields == tuple(fields), "Wrong fields"


def test_default_fields():
    """Check default set of fields of an action.

    1. Create an action without specifying fields.
    2. Get fields of the action.
    3. Check the fields.
    """
    action = Action(name="test default fields", target="/test-default-fields")
    assert action.fields == (), "Wrong fields"


@pytest.mark.parametrize(
    argnames="fields",
    argvalues=[
        [None, Field(name="field")],
        [Field(name="first"), "second field", Field(name="third")],
    ],
    ids=[
        "First field",
        "Field in the middle",
    ],
)
def test_incompatible_fields(fields):
    """Check that ValueError is raised if at least one of the fields is of incompatible type.

    1. Try to create an action with incompatible field type.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        Action(name="test incompatible fields", target="/test-incompatible-fields", fields=fields)

    assert error_info.value.args[0] == "Some of the fields are of incompatible type"


@pytest.mark.parametrize(
    argnames="encoding_type",
    argvalues=[
        None,
        "application/x-www-form-urlencoded",
        "application/json",
    ],
    ids=[
        "None",
        "Common",
        "Uncommon",
    ],
)
def test_encoding_type_without_fields(encoding_type):
    """Check encoding type of an action without fields.

    1. Create an action with different encoding type without fields.
    2. Get encoding type of the action.
    3. Check the encoding type.
    """
    action = Action(
        name="test encoding type. No fields",
        target="/test-encoding-types",
        fields=(),
        encoding_type=encoding_type,
        )
    assert action.encoding_type == encoding_type, "Wrong encoding type"


@pytest.mark.parametrize(
    argnames="encoding_type, expected_encoding_type",
    argvalues=[
        (None, "application/x-www-form-urlencoded"),
        ("application/x-www-form-urlencoded", "application/x-www-form-urlencoded"),
        ("application/json", "application/json"),
    ],
    ids=[
        "None",
        "Common",
        "Uncommon",
    ],
)
def test_encoding_type_with_fields(encoding_type, expected_encoding_type):
    """Check encoding type of an action with fields.

    1. Create an action with different encoding type with 1 field.
    2. Get encoding type of the action.
    3. Check the encoding type.
    """
    action = Action(
        name="test encoding type. No fields",
        target="/test-encoding-types",
        fields=[Field(name="single field")],
        encoding_type=encoding_type,
        )
    assert action.encoding_type == expected_encoding_type, "Wrong encoding type"


@pytest.mark.parametrize(
    argnames="fields, expected_encoding_type",
    argvalues=[
        [(), None],
        [[Field(name="field")], "application/x-www-form-urlencoded"],
    ],
    ids=[
        "Without fields",
        "With fields",
    ],
)
def test_default_encoding_type(fields, expected_encoding_type):
    """Check default enconding type of an action.

    1. Create an action without specifying encoding type.
    2. Get encoding type of the action.
    3. Check the encoding type.
    """
    action = Action(
        name="test default encoding type",
        target="/test-default-encoding-type",
        fields=fields,
        )
    assert action.encoding_type == expected_encoding_type, "Wrong encoding type"
