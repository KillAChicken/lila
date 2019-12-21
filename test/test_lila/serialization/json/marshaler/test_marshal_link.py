"""Test cases for marshal_link method of JSON marshaler."""

import pytest

from lila.core.link import Link
from lila.serialization.json.marshaler import JSONMarshaler


def test_missing_relations():
    """Test that ValueError is raised if a link does not have relations attribute.

    1. Create a json marshaller.
    2. Try to call marshal_link for an object without relations attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingRelationsLink(Link):
        @property
        def relations(self):
            raise AttributeError()

    link = _MissingRelationsLink(relations=["self"], target="/no/relations")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_link(link=link)

    assert error_info.value.args[0] == "Failed to get link's relations", "Wrong error"


def test_non_iterable_relations():
    """Test that ValueError is raised if link provides a non-iterable object as its relations.

    1. Create a json marshaller.
    2. Try to call marshal_link method for an object with non-iterable relations.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableRelationsLink(Link):
        @property
        def relations(self):
            return None

    link = _NonIterableRelationsLink(relations=["self"], target="/relations-are-not-iterable")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_link(link=link)

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

    1. Create a json marshaler.
    2. Marshal a link with specific relations.
    3. Check a key with the relations in the marshaled data.
    """
    class _FixedRelationsLink(Link):
        @property
        def relations(self):
            return relations

    link = _FixedRelationsLink(relations=["self"], target="/test/relations")

    link_data = JSONMarshaler().marshal_link(link=link)
    assert "rel" in link_data, "Marshaled data does not have 'rel' key"
    assert link_data["rel"] == expected_relations, "Wrong relations"


def test_missing_classes():
    """Test that ValueError is raised if a link does not have classes attribute.

    1. Create a json marshaller.
    2. Try to call marshal_link for an object without classes attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingClassesLink(Link):
        @property
        def classes(self):
            raise AttributeError()

    link = _MissingClassesLink(relations=["self"], target="/no/classes")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_link(link=link)

    assert error_info.value.args[0] == "Failed to get link's classes", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if link provides a non-iterable object as its classes.

    1. Create a json marshaller.
    2. Try to call marshal_link method for an object with non-iterable classes.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableClassesLink(Link):
        @property
        def classes(self):
            return None

    link = _NonIterableClassesLink(relations=["self"], target="/classes-are-not-iterable")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_link(link=link)

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

    1. Create a json marshaler.
    2. Marshal a link with specific classes.
    3. Check a key with the classes in the marshaled data.
    """
    class _FixedClassesLink(Link):
        @property
        def classes(self):
            return classes

    link = _FixedClassesLink(relations=["self"], target="/test/classes")

    link_data = JSONMarshaler().marshal_link(link=link)
    assert "class" in link_data, "Marshaled data does not have 'class' key"
    assert link_data["class"] == expected_classes, "Wrong classes"


def test_missing_target():
    """Test that ValueError is raised if a link does not have target attribute.

    1. Create a json marshaller.
    2. Try to call marshal_link method for an object without target attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTargetLink(Link):
        @property
        def target(self):
            raise AttributeError()

    link = _MissingTargetLink(relations=["self"], target="/no/target")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_link(link=link)

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

    1. Create a json marshaler.
    2. Marshal a link with a specific target.
    3. Check a key with the target in the marshaled data.
    """
    class _FixedTargetLink(Link):
        @property
        def target(self):
            return target

    link = _FixedTargetLink(relations=["self"], target="/fixed/target")

    link_data = JSONMarshaler().marshal_link(link=link)
    assert "href" in link_data, "Marshaled data does not have 'href' key"
    assert link_data["href"] == expected_target, "Wrong target"


def test_missing_title():
    """Test that ValueError is raised if a link does not have title attribute.

    1. Create a json marshaller.
    2. Try to call marshal_link method for an object without title attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTitleLink(Link):
        @property
        def title(self):
            raise AttributeError()

    link = _MissingTitleLink(relations=["self"], target="/no/title")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_link(link=link)

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

    1. Create a json marshaler.
    2. Marshal a link with a specific title.
    3. Check a key with the title in the marshaled data.
    """
    class _FixedTitleLink(Link):
        @property
        def title(self):
            return title

    link = _FixedTitleLink(relations=["self"], target="/fixed-title")

    link_data = JSONMarshaler().marshal_link(link=link)
    assert "title" in link_data, "Marshaled data does not have 'title' key"
    assert link_data["title"] == expected_title, "Wrong title"


def test_missing_target_media_type():
    """Test that ValueError is raised if a link does not have target media type attribute.

    1. Create a json marshaller.
    2. Try to call marshal_link method for an object without target media type attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTargetMediaTypeLink(Link):
        @property
        def target_media_type(self):
            raise AttributeError()

    link = _MissingTargetMediaTypeLink(relations=["self"], target="/no/target/media/type")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_link(link=link)

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

    1. Create a json marshaler.
    2. Marshal a link with a specific target media type.
    3. Check a key with the target media type in the marshaled data.
    """
    class _FixedTargetMediaTypeLink(Link):
        @property
        def target_media_type(self):
            return target_media_type

    link = _FixedTargetMediaTypeLink(relations=["self"], target="/fixed-target-media-type")

    link_data = JSONMarshaler().marshal_link(link=link)
    assert "type" in link_data, "Marshaled data does not have 'type' key"
    assert link_data["type"] == expected_target_media_type, "Wrong target media type"
