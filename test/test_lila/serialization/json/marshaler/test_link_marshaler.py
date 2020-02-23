"""Test cases for a marshaler class for a link."""

from collections import namedtuple

import pytest

from lila.core.link import Link
from lila.serialization.json.link import LinkMarshaler


def test_missing_relations():
    """Test that ValueError is raised if a link does not have relations attribute.

    1. Create a link marshaler for an object without relations attibute.
    2. Try to call marshal_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkMarshaler(link=object()).marshal_relations()

    assert error_info.value.args[0] == "Failed to get link's relations", "Wrong error"


def test_non_iterable_relations():
    """Test that ValueError is raised if a link provides a non-iterable object as its relations.

    1. Create a link marshaler for an object with non-iterable relations.
    2. Try to call marshal_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    RelationsLink = namedtuple("RelationsLink", "relations")
    with pytest.raises(ValueError) as error_info:
        LinkMarshaler(link=RelationsLink(relations=None)).marshal_relations()

    assert error_info.value.args[0] == "Failed to iterate over link's relations", "Wrong error"


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

    1. Create a link marshaler for an object with specific relations.
    2. Marshal relations.
    3. Check the marshaled relations.
    """
    RelationsLink = namedtuple("RelationsLink", "relations")
    actual_relations = LinkMarshaler(link=RelationsLink(relations=relations)).marshal_relations()
    assert actual_relations == expected_relations, "Wrong relations"


def test_missing_classes():
    """Test that ValueError is raised if a link does not have classes attribute.

    1. Create a link marshaler for an object without classes attibute.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkMarshaler(link=object()).marshal_classes()

    assert error_info.value.args[0] == "Failed to get link's classes", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if a link provides a non-iterable object as its classes.

    1. Create a link marshaler for an object with non-iterable classes.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    ClassesLink = namedtuple("ClassesLink", "classes")
    with pytest.raises(ValueError) as error_info:
        LinkMarshaler(link=ClassesLink(classes=None)).marshal_classes()

    assert error_info.value.args[0] == "Failed to iterate over link's classes", "Wrong error"


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

    1. Create a link marshaler for an object with specific classes.
    2. Marshal classes.
    3. Check the marshaled classes.
    """
    ClassesLink = namedtuple("ClassesLink", "classes")
    actual_classes = LinkMarshaler(link=ClassesLink(classes=classes)).marshal_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_missing_target():
    """Test that ValueError is raised if a link does not have target attribute.

    1. Create a link marshaler for an object without target attibute.
    2. Try to call marshal_target method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkMarshaler(link=object()).marshal_target()

    assert error_info.value.args[0] == "Failed to get link's target", "Wrong error"


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

    1. Create a link marshaler for an object with specific target.
    2. Marshal link's target.
    3. Check the marshaled target.
    """
    TargetLink = namedtuple("TargetLink", "target")
    actual_target = LinkMarshaler(link=TargetLink(target=target)).marshal_target()
    assert actual_target == expected_target, "Wrong target"


def test_missing_title():
    """Test that ValueError is raised if a link does not have title attribute.

    1. Create a link marshaler for an object without title attibute.
    2. Try to call marshal_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkMarshaler(link=object()).marshal_title()

    assert error_info.value.args[0] == "Failed to get link's title", "Wrong error"


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

    1. Create a link marshaler for an object with specific title.
    2. Marshal link's title.
    3. Check the marshaled title.
    """
    TitleLink = namedtuple("TitleLink", "title")
    actual_title = LinkMarshaler(link=TitleLink(title=title)).marshal_title()
    assert actual_title == expected_title, "Wrong title"


def test_missing_target_media_type():
    """Test that ValueError is raised if a link does not have target media type attribute.

    1. Create a link marshaler for an object without target media type attibute.
    2. Try to call marshal_target_media_type method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkMarshaler(link=object()).marshal_target_media_type()

    assert error_info.value.args[0] == "Failed to get link's target media type", "Wrong error"


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

    1. Create a link marshaler for an object with specific target media type.
    2. Marshal link's target media type.
    3. Check the marshaled target media type.
    """
    TargetMediaTypeLink = namedtuple("TargetMediaTypeLink", "target_media_type")
    marshaler = LinkMarshaler(link=TargetMediaTypeLink(target_media_type=target_media_type))
    actual_target_media_type = marshaler.marshal_target_media_type()
    assert actual_target_media_type == expected_target_media_type, "Wrong target media type"


def test_marshal():
    """Test that link data is properly marshaled.

    1. Create a link.
    2. Create a link marshaler for the link.
    3. Replace marshaler methods so that they return predefined data.
    4. Marshal the link.
    5. Check the marshaled data.
    """
    marshaler = LinkMarshaler(Link(relations=["self"], target="/link"))
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
