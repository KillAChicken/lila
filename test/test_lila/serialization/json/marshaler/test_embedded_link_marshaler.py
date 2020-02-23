"""Test cases for a marshaler class for an embedded link."""

from collections import namedtuple

import pytest

from lila.core.link import EmbeddedLink
from lila.serialization.json.link import EmbeddedLinkMarshaler


def test_missing_relations():
    """Test that ValueError is raised if an embedded link does not have relations attribute.

    1. Create an embedded link marshaler for an object without relations attibute.
    2. Try to call marshal_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkMarshaler(embedded_link=object()).marshal_relations()

    assert error_info.value.args[0] == "Failed to get relations of the embedded link", "Wrong error"


def test_non_iterable_relations():
    """Test that ValueError is raised if an embedded link has a non-iterable object as relations.

    1. Create an embedded link marshaler for an object with non-iterable relations.
    2. Try to call marshal_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    RelationsLink = namedtuple("RelationsLink", "relations")
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkMarshaler(embedded_link=RelationsLink(relations=None)).marshal_relations()

    assert error_info.value.args[0] == "Failed to iterate over relations of the embedded link", (
        "Wrong error"
    )


@pytest.mark.parametrize(
    argnames="relations,expected_relations",
    argvalues=[
        ([], []),
        (["self"], ["self"]),
        (["prev", "next"], ["prev", "next"]),
        (("first", None, [1, 2]), ["first", "None", "[1, 2]"]),
        ],
    ids=[
        "Empty list",
        "Single relation",
        "Multiple relations",
        "Non-string relations",
        ],
    )
def test_relations(relations, expected_relations):
    """Test that relations are properly marshaled.

    1. Create an embedded link marshaler for an object with specific relations.
    2. Marshal relations.
    3. Check the marshaled relations.
    """
    RelationsLink = namedtuple("RelationsLink", "relations")
    marshaler = EmbeddedLinkMarshaler(embedded_link=RelationsLink(relations=relations))
    actual_relations = marshaler.marshal_relations()
    assert actual_relations == expected_relations, "Wrong relations"


def test_missing_classes():
    """Test that ValueError is raised if an embedded link does not have classes attribute.

    1. Create an embedded link marshaler for an object without classes attibute.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkMarshaler(embedded_link=object()).marshal_classes()

    assert error_info.value.args[0] == "Failed to get classes of the embedded link", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if an embedded link has a non-iterable object as its classes.

    1. Create an embedded link marshaler for an object with non-iterable classes.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    ClassesLink = namedtuple("ClassesLink", "classes")
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkMarshaler(embedded_link=ClassesLink(classes=None)).marshal_classes()

    assert error_info.value.args[0] == "Failed to iterate over classes of the embedded link", (
        "Wrong error"
    )


@pytest.mark.parametrize(
    argnames="classes,expected_classes",
    argvalues=[
        ([], []),
        (["link class"], ["link class"]),
        (["first link class", "second link class"], ["first link class", "second link class"]),
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

    1. Create an embedded link marshaler for an object with specific classes.
    2. Marshal classes.
    3. Check the marshaled classes.
    """
    ClassesLink = namedtuple("ClassesLink", "classes")
    marshaler = EmbeddedLinkMarshaler(embedded_link=ClassesLink(classes=classes))
    actual_classes = marshaler.marshal_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_missing_target():
    """Test that ValueError is raised if an embedded link does not have target attribute.

    1. Create an embedded link marshaler for an object without target attibute.
    2. Try to call marshal_target method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkMarshaler(embedded_link=object()).marshal_target()

    assert error_info.value.args[0] == "Failed to get target of the embedded link", "Wrong error"


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

    1. Create an embedded link marshaler for an object with specific target.
    2. Marshal link's target.
    3. Check the marshaled target.
    """
    TargetLink = namedtuple("TargetLink", "target")
    actual_target = EmbeddedLinkMarshaler(embedded_link=TargetLink(target=target)).marshal_target()
    assert actual_target == expected_target, "Wrong target"


def test_missing_title():
    """Test that ValueError is raised if an embedded link does not have title attribute.

    1. Create an embedded link marshaler for an object without title attibute.
    2. Try to call marshal_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkMarshaler(embedded_link=object()).marshal_title()

    assert error_info.value.args[0] == "Failed to get title of the embedded link", "Wrong error"


@pytest.mark.parametrize(
    argnames="title,expected_title",
    argvalues=[
        ("link title", "link title"),
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

    1. Create an embedded link marshaler for an object with specific title.
    2. Marshal link's title.
    3. Check the marshaled title.
    """
    TitleLink = namedtuple("TitleLink", "title")
    actual_title = EmbeddedLinkMarshaler(embedded_link=TitleLink(title=title)).marshal_title()
    assert actual_title == expected_title, "Wrong title"


def test_missing_target_media_type():
    """Test that ValueError is raised if an embedded link does not have target media type attribute.

    1. Create an embedded link marshaler for an object without target media type attibute.
    2. Try to call marshal_target_media_type method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkMarshaler(embedded_link=object()).marshal_target_media_type()

    assert error_info.value.args[0] == "Failed to get target media type of the embedded link", (
        "Wrong error"
    )


@pytest.mark.parametrize(
    argnames="target_media_type,expected_target_media_type",
    argvalues=[
        ("application/json", "application/json"),
        ("", ""),
        (None, None),
        ],
    ids=[
        "Simple",
        "Empty",
        "None",
        ],
    )
def test_target_media_type(target_media_type, expected_target_media_type):
    """Test that target media type is properly marshaled.

    1. Create an embedded link marshaler for an object with specific target media type.
    2. Marshal link's target media type.
    3. Check the marshaled target media type.
    """
    TargetMediaTypeLink = namedtuple("TargetMediaTypeLink", "target_media_type")
    marshaler = EmbeddedLinkMarshaler(
        embedded_link=TargetMediaTypeLink(target_media_type=target_media_type),
        )
    actual_target_media_type = marshaler.marshal_target_media_type()
    assert actual_target_media_type == expected_target_media_type, "Wrong target media type"


def test_marshal():
    """Test that embedded link data is properly marshaled.

    1. Create an embedded link.
    2. Create an embedded link marshaler for the embedded link.
    3. Replace marshaler methods so that they return predefined data.
    4. Marshal the embedded link.
    5. Check the marshaled data.
    """
    marshaler = EmbeddedLinkMarshaler(EmbeddedLink(relations=["self"], target="/link"))
    marshaler.marshal_relations = lambda: "marshal_relations"
    marshaler.marshal_classes = lambda: "marshal_classes"
    marshaler.marshal_target = lambda: "marshal_target"
    marshaler.marshal_title = lambda: "marshal_title"
    marshaler.marshal_target_media_type = lambda: "marshal_target_media_type"

    actual_data = marshaler.marshal()
    expected_data = {
        "rel": "marshal_relations",
        "class": "marshal_classes",
        "href": "marshal_target",
        "title": "marshal_title",
        "type": "marshal_target_media_type",
        }
    assert actual_data == expected_data, "Field is not properly marshaled"
