"""Test cases for marshal_embedded_link method of JSON marshaler."""

import pytest

from lila.core.link import EmbeddedLink
from lila.serialization.json.marshaler import JSONMarshaler


def test_missing_relations():
    """Test that ValueError is raised if an embedded link does not have relations attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_link for an object without relations attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingRelationsEmbeddedLink(EmbeddedLink):
        @property
        def relations(self):
            raise AttributeError()

    link = _MissingRelationsEmbeddedLink(relations=["self"], target="/no/relations")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_link(embedded_link=link)

    assert error_info.value.args[0] == "Failed to get relations of the embedded link", "Wrong error"


def test_non_iterable_relations():
    """Test that ValueError is raised if an embedded link has a non-iterable object as relations.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_link method for an object with non-iterable relations.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableRelationsEmbeddedLink(EmbeddedLink):
        @property
        def relations(self):
            return None

    link = _NonIterableRelationsEmbeddedLink(
        relations=["self"],
        target="/relations-are-not-iterable",
    )

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_link(embedded_link=link)

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

    1. Create a json marshaler.
    2. Marshal an embedded link with specific relations.
    3. Check a key with the relations in the marshaled data.
    """
    class _FixedRelationsEmbeddedLink(EmbeddedLink):
        @property
        def relations(self):
            return relations

    link = _FixedRelationsEmbeddedLink(relations=["self"], target="/test/relations")

    link_data = JSONMarshaler().marshal_embedded_link(embedded_link=link)
    assert "rel" in link_data, "Marshaled data does not have 'rel' key"
    assert link_data["rel"] == expected_relations, "Wrong relations"


def test_missing_classes():
    """Test that ValueError is raised if an embedded link does not have classes attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_link for an object without classes attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingClassesEmbeddedLink(EmbeddedLink):
        @property
        def classes(self):
            raise AttributeError()

    link = _MissingClassesEmbeddedLink(relations=["self"], target="/no/classes")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_link(embedded_link=link)

    assert error_info.value.args[0] == "Failed to get classes of the embedded link", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if an embedded link has a non-iterable object as its classes.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_link method for an object with non-iterable classes.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableClassesEmbeddedLink(EmbeddedLink):
        @property
        def classes(self):
            return None

    link = _NonIterableClassesEmbeddedLink(relations=["self"], target="/classes-are-not-iterable")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_link(embedded_link=link)

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

    1. Create a json marshaler.
    2. Marshal an embedded link with specific classes.
    3. Check a key with the classes in the marshaled data.
    """
    class _FixedClassesEmbeddedLink(EmbeddedLink):
        @property
        def classes(self):
            return classes

    link = _FixedClassesEmbeddedLink(relations=["self"], target="/test/classes")

    link_data = JSONMarshaler().marshal_embedded_link(embedded_link=link)
    assert "class" in link_data, "Marshaled data does not have 'class' key"
    assert link_data["class"] == expected_classes, "Wrong classes"


def test_missing_target():
    """Test that ValueError is raised if an embedded link does not have target attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_link method for an object without target attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTargetEmbeddedLink(EmbeddedLink):
        @property
        def target(self):
            raise AttributeError()

    link = _MissingTargetEmbeddedLink(relations=["self"], target="/no/target")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_link(embedded_link=link)

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

    1. Create a json marshaler.
    2. Marshal an embedded link with a specific target.
    3. Check a key with the target in the marshaled data.
    """
    class _FixedTargetEmbeddedLink(EmbeddedLink):
        @property
        def target(self):
            return target

    link = _FixedTargetEmbeddedLink(relations=["self"], target="/fixed/target")

    link_data = JSONMarshaler().marshal_embedded_link(embedded_link=link)
    assert "href" in link_data, "Marshaled data does not have 'href' key"
    assert link_data["href"] == expected_target, "Wrong target"


def test_missing_title():
    """Test that ValueError is raised if an embedded link does not have title attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_link method for an object without title attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTitleEmbeddedLink(EmbeddedLink):
        @property
        def title(self):
            raise AttributeError()

    link = _MissingTitleEmbeddedLink(relations=["self"], target="/no/title")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_link(embedded_link=link)

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

    1. Create a json marshaler.
    2. Marshal an embedded link with a specific title.
    3. Check a key with the title in the marshaled data.
    """
    class _FixedTitleEmbeddedLink(EmbeddedLink):
        @property
        def title(self):
            return title

    link = _FixedTitleEmbeddedLink(relations=["self"], target="/fixed-title")

    link_data = JSONMarshaler().marshal_embedded_link(embedded_link=link)
    assert "title" in link_data, "Marshaled data does not have 'title' key"
    assert link_data["title"] == expected_title, "Wrong title"


def test_missing_target_media_type():
    """Test that ValueError is raised if an embedded link does not have target media type attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_link method for an object without target media type attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTargetMediaTypeEmbeddedLink(EmbeddedLink):
        @property
        def target_media_type(self):
            raise AttributeError()

    link = _MissingTargetMediaTypeEmbeddedLink(relations=["self"], target="/no/target/media/type")

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_link(embedded_link=link)

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

    1. Create a json marshaler.
    2. Marshal an embedded link with a specific target media type.
    3. Check a key with the target media type in the marshaled data.
    """
    class _FixedTargetMediaTypeEmbeddedLink(EmbeddedLink):
        @property
        def target_media_type(self):
            return target_media_type

    link = _FixedTargetMediaTypeEmbeddedLink(relations=["self"], target="/fixed-target-media-type")

    link_data = JSONMarshaler().marshal_embedded_link(embedded_link=link)
    assert "type" in link_data, "Marshaled data does not have 'type' key"
    assert link_data["type"] == expected_target_media_type, "Wrong target media type"
