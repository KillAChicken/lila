"""Test cases for marshal_embedded_representation method of JSON marshaler."""

import json

import pytest

from lila.core.link import Link, EmbeddedLink
from lila.core.action import Action
from lila.core.entity import EmbeddedRepresentation
from lila.serialization.json.marshaler import JSONMarshaler


def test_missing_relations():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation does not have relations attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation for an object without relations attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _MissingRelationsEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def relations(self):
            raise AttributeError()

    representation = _MissingRelationsEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    assert error_info.value.args[0] == "Failed to get relations of the embedded representation", (
        "Wrong error"
        )


def test_non_iterable_relations():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation has a non-iterable object as relations.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object with non-iterable relations.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _NonIterableRelationsEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def relations(self):
            return None

    representation = _NonIterableRelationsEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    expected_message = "Failed to iterate over relations of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


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
    2. Marshal an embedded representation with specific relations.
    3. Check a key with the relations in the marshaled data.
    """
    class _FixedRelationsEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def relations(self):
            return relations

    representation = _FixedRelationsEmbeddedRepresentation(relations=["self"])

    representation_data = JSONMarshaler().marshal_embedded_representation(
        embedded_representation=representation,
        )
    assert "rel" in representation_data, "Marshaled data does not have 'rel' key"
    assert representation_data["rel"] == expected_relations, "Wrong relations"


def test_missing_classes():
    """Test that ValueError is raised if an embedded representation does not have classes attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation for an object without classes attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingClassesEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def classes(self):
            raise AttributeError()

    representation = _MissingClassesEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    assert error_info.value.args[0] == "Failed to get classes of the embedded representation", (
        "Wrong error"
        )


def test_non_iterable_classes():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation has a non-iterable object as its classes.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object with non-iterable classes.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _NonIterableClassesEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def classes(self):
            return None

    representation = _NonIterableClassesEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    expected_message = "Failed to iterate over classes of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


@pytest.mark.parametrize(
    argnames="classes,expected_classes",
    argvalues=[
        ([], []),
        (["representation class"], ["representation class"]),
        (
            ["first representation class", "second representation class"],
            ["first representation class", "second representation class"],
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
    2. Marshal an embedded representation with specific classes.
    3. Check a key with the classes in the marshaled data.
    """
    class _FixedClassesEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def classes(self):
            return classes

    representation = _FixedClassesEmbeddedRepresentation(relations=["self"])

    representation_data = JSONMarshaler().marshal_embedded_representation(
        embedded_representation=representation,
        )
    assert "class" in representation_data, "Marshaled data does not have 'class' key"
    assert representation_data["class"] == expected_classes, "Wrong classes"


def test_missing_properties():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation does not have properties attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation for an object without properties attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _MissingPropertiesEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def properties(self):
            raise AttributeError()

    representation = _MissingPropertiesEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    assert error_info.value.args[0] == "Failed to get properties of the embedded representation", (
        "Wrong error"
        )


def test_invalid_properties():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if properties of an embedded representation are not valid json object.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object with non-iterable classes.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _InvalidJSONPropertiesEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def properties(self):
            return object()

    representation = _InvalidJSONPropertiesEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    expected_message = "Failed to marshal properties of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


@pytest.mark.parametrize(
    argnames="properties",
    argvalues=[
        None,
        {
            "key": 1,
            "list": [1, 2, 3],
            "dict": {"key": "value"},
            },
        ],
    ids=[
        "None",
        "Nested json",
        ],
    )
def test_properties(properties):
    """Test that properties are properly marshaled.

    1. Create a json marshaler.
    2. Marshal an embedded representation with specific properties.
    3. Check a key with the properties in the marshaled data.
    4. Check the properties by dumping them into JSON with sorted keys.
    """
    class _FixedPropertiesEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def properties(self):
            return properties

    representation = _FixedPropertiesEmbeddedRepresentation(relations=["self"])

    representation_data = JSONMarshaler().marshal_embedded_representation(
        embedded_representation=representation,
        )
    assert "properties" in representation_data, "Marshaled data does not have 'properties' key"
    actual_properties = json.dumps(representation_data["properties"], sort_keys=True)
    expected_properties = json.dumps(properties, sort_keys=True)
    assert actual_properties == expected_properties, "Wrong properties"


def test_missing_sub_entities():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation does not have entities attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object without entities attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _MissingEntitiesEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def entities(self):
            raise AttributeError()

    representation = _MissingEntitiesEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    expected_message = "Failed to get sub entities of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_non_iterable_sub_entities():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if embedded representation has a non-iterable object as its entities.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object with non-iterable entities.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _NonIterableEntitiesEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def entities(self):
            return None

    representation = _NonIterableEntitiesEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    expected_message = "Failed to iterate over sub entities of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_non_marshalable_sub_entities(non_marshalable_sub_entity):
    # pylint: disable=line-too-long
    """Test that ValueError is raised if one of sub entities of the embedded representation is not marshallable.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object with entities that are not marshalable.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _NonMarshalableEntitiesEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def entities(self):
            return [non_marshalable_sub_entity]

    representation = _NonMarshalableEntitiesEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    expected_message = "Failed to marshal sub entities of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


@pytest.mark.parametrize(
    argnames="sub_entities",
    argvalues=[
        [],
        [EmbeddedLink(target="/single", relations=["self"])],
        [EmbeddedRepresentation(relations=["self"])],
        [
            EmbeddedLink(target="/prev", relations=["prev"]),
            EmbeddedLink(target="/next", relations=["next"]),
            ],
        [
            EmbeddedRepresentation(relations=["parent"]),
            EmbeddedRepresentation(relations=["child"]),
            ],
        [
            EmbeddedRepresentation(relations=["first"]),
            EmbeddedLink(target="/second", relations=["second"]),
            EmbeddedRepresentation(relations=["third"]),
            EmbeddedLink(target="/forth", relations=["forth"]),
            ],
        ],
    ids=[
        "Empty list",
        "Single link",
        "Single representation",
        "Only links",
        "Only representations",
        "Both links and representations",
        ],
    )
def test_sub_entities(sub_entities):
    """Test that sub entities are properly marshaled.

    1. Create a json marshaler.
    2. Create an embedded representation with specific sub entities.
    3. Replace marshal_embedded_link of the marshaler so that it returns fake data.
    4. Replace marshal_embedded_representation of the the marshaller so that it return fake data
       except one specific embedded representation.
    5. Marshal the embedded representation.
    6. Check a key with the sub entities (fake data) in the marshaled data.
    """
    class _FixedEntitiesEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def entities(self):
            return sub_entities

    representation = _FixedEntitiesEmbeddedRepresentation(relations=["self"])

    marshaler = JSONMarshaler()

    def _fake_marshal_embedded_link(embedded_link):
        return sub_entities.index(embedded_link)

    marshaler.marshal_embedded_link = _fake_marshal_embedded_link

    default_marshal_embedded_representation = marshaler.marshal_embedded_representation

    def _fake_marshal_embedded_representation(embedded_representation):
        if embedded_representation is not representation:
            return sub_entities.index(embedded_representation)

        return default_marshal_embedded_representation(embedded_representation)

    marshaler.marshal_embedded_representation = _fake_marshal_embedded_representation

    representation_data = marshaler.marshal_embedded_representation(
        embedded_representation=representation,
        )
    assert "entities" in representation_data, "Marshaled data does not have 'entities' key"
    assert representation_data["entities"] == list(range(len(sub_entities))), "Wrong entities"


def test_missing_links():
    """Test that ValueError is raised if an embedded representation does not have links attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object without links attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingLinksEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def links(self):
            raise AttributeError()

    representation = _MissingLinksEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    assert error_info.value.args[0] == "Failed to get links of the embedded representation", (
        "Wrong error"
        )


def test_non_iterable_links():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if embedded representation has a non-iterable object as its links.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object with non-iterable links.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _NonIterableLinksEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def links(self):
            return None

    representation = _NonIterableLinksEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    expected_message = "Failed to iterate over links of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_non_marshalable_links():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if one of links of the embedded representation is not marshallable.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object with links that are not marshalable.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _NonMarshalableLinksEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def links(self):
            return [
                Link(relations=["first"], target="/first"),
                None,
                Link(relations=["last"], target="/last"),
                ]

    representation = _NonMarshalableLinksEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    assert error_info.value.args[0] == "Failed to marshal links of the embedded representation", (
        "Wrong error"
        )


@pytest.mark.parametrize(
    argnames="links",
    argvalues=[
        [],
        [Link(target="/single", relations=["self"])],
        [Link(target="/prev", relations=["prev"]), Link(target="/next", relations=["next"])],
        ],
    ids=[
        "Empty list",
        "Single link",
        "Multiple links",
        ],
    )
def test_links(links):
    """Test that links are properly marshaled.

    1. Create a json marshaler.
    2. Replace marshal_link of the marshaler so that it returns fake data.
    3. Marshal an embedded representation with specific links.
    4. Check a key with the links (fake data) in the marshaled data.
    """
    class _FixedLinksEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def links(self):
            return links

    representation = _FixedLinksEmbeddedRepresentation(relations=["self"])

    marshaler = JSONMarshaler()
    marshaler.marshal_link = links.index

    representation_data = marshaler.marshal_embedded_representation(
        embedded_representation=representation,
        )
    assert "links" in representation_data, "Marshaled data does not have 'links' key"
    assert representation_data["links"] == list(range(len(links))), "Wrong links"


def test_missing_actions():
    """Test that ValueError is raised if an embedded representation does not have actions attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object without actions attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingActionsEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def actions(self):
            raise AttributeError()

    representation = _MissingActionsEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    assert error_info.value.args[0] == "Failed to get actions of the embedded representation", (
        "Wrong error"
        )


def test_non_iterable_actions():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if embedded representation has a non-iterable object as its actions.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object with non-iterable actions.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _NonIterableActionsEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def actions(self):
            return None

    representation = _NonIterableActionsEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    expected_message = "Failed to iterate over actions of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_non_marshalable_actions():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if one of actions of the embedded representation is not marshallable.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object with actions that are not marshalable.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _NonMarshalableActionsEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def actions(self):
            return [
                Action(name="first", target="/first"),
                None,
                Action(name="last", target="/last"),
                ]

    representation = _NonMarshalableActionsEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    assert error_info.value.args[0] == "Failed to marshal actions of the embedded representation", (
        "Wrong error"
        )


@pytest.mark.parametrize(
    argnames="actions",
    argvalues=[
        [],
        [Action(name="single", target="/single")],
        [Action(name="first", target="/first"), Action(name="second", target="/second")],
        ],
    ids=[
        "Empty list",
        "Single action",
        "Multiple actions",
        ],
    )
def test_actions(actions):
    """Test that actions are properly marshaled.

    1. Create a json marshaler.
    2. Replace marshal_action of the marshaler so that it returns fake data.
    3. Marshal an embedded representation with specific actions.
    4. Check a key with the actions (fake data) in the marshaled data.
    """
    class _FixedActionsEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def actions(self):
            return actions

    representation = _FixedActionsEmbeddedRepresentation(relations=["self"])

    marshaler = JSONMarshaler()
    marshaler.marshal_action = actions.index

    representation_data = marshaler.marshal_embedded_representation(
        embedded_representation=representation,
        )
    assert "actions" in representation_data, "Marshaled data does not have 'actions' key"
    assert representation_data["actions"] == list(range(len(actions))), "Wrong actions"


def test_missing_title():
    """Test that ValueError is raised if an embedded representation does not have title attribute.

    1. Create a json marshaller.
    2. Try to call marshal_embedded_representation method for an object without title attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTitleEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def title(self):
            raise AttributeError()

    representation = _MissingTitleEmbeddedRepresentation(relations=["self"])

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_embedded_representation(embedded_representation=representation)

    assert error_info.value.args[0] == "Failed to get title of the embedded representation", (
        "Wrong error"
        )


@pytest.mark.parametrize(
    argnames="title,expected_title",
    argvalues=[
        ("representation title", "representation title"),
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
    2. Marshal an embedded representation with a specific title.
    3. Check a key with the title in the marshaled data.
    """
    class _FixedTitleEmbeddedRepresentation(EmbeddedRepresentation):
        @property
        def title(self):
            return title

    representation = _FixedTitleEmbeddedRepresentation(relations=["self"])

    representation_data = JSONMarshaler().marshal_embedded_representation(
        embedded_representation=representation,
        )
    assert "title" in representation_data, "Marshaled data does not have 'title' key"
    assert representation_data["title"] == expected_title, "Wrong title"
