"""Test cases for marshal_entity method of JSON marshaler."""

import json

import pytest

from lila.core.link import Link, EmbeddedLink
from lila.core.action import Action
from lila.core.entity import Entity, EmbeddedRepresentation
from lila.serialization.json.marshaler import JSONMarshaler


def test_missing_classes():
    """Test that ValueError is raised if an entity does not have classes attribute.

    1. Create a json marshaller.
    2. Try to call marshal_entity for an object without classes attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingClassesEntity(Entity):
        @property
        def classes(self):
            raise AttributeError()

    entity = _MissingClassesEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to get entity's classes", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if an entity has a non-iterable object as its classes.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object with non-iterable classes.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableClassesEntity(Entity):
        @property
        def classes(self):
            return None

    entity = _NonIterableClassesEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to iterate over entity's classes", "Wrong error"


@pytest.mark.parametrize(
    argnames="classes,expected_classes",
    argvalues=[
        ([], []),
        (["entity class"], ["entity class"]),
        (
            ["first entity class", "second entity class"],
            ["first entity class", "second entity class"],
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
    2. Marshal an entity with specific classes.
    3. Check a key with the classes in the marshaled data.
    """
    class _FixedClassesEntity(Entity):
        @property
        def classes(self):
            return classes

    entity = _FixedClassesEntity()

    entity_data = JSONMarshaler().marshal_entity(entity=entity)
    assert "class" in entity_data, "Marshaled data does not have 'class' key"
    assert entity_data["class"] == expected_classes, "Wrong classes"


def test_missing_properties():
    """Test that ValueError is raised if an entity does not have properties attribute.

    1. Create a json marshaller.
    2. Try to call marshal_entity for an object without properties attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingPropertiesEntity(Entity):
        @property
        def properties(self):
            raise AttributeError()

    entity = _MissingPropertiesEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to get entity's properties", "Wrong error"


def test_invalid_properties():
    """Test that ValueError is raised if entity's properties are not valid json object.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object with non-iterable classes.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _InvalidJSONPropertiesEntity(Entity):
        @property
        def properties(self):
            return object()

    entity = _InvalidJSONPropertiesEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to marshal entity's properties", "Wrong error"


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
    2. Marshal an entity with specific properties.
    3. Check a key with the properties in the marshaled data.
    4. Check the properties by dumping them into JSON with sorted keys.
    """
    class _FixedPropertiesEntity(Entity):
        @property
        def properties(self):
            return properties

    entity = _FixedPropertiesEntity()

    entity_data = JSONMarshaler().marshal_entity(entity=entity)
    assert "properties" in entity_data, "Marshaled data does not have 'properties' key"
    actual_properties = json.dumps(entity_data["properties"], sort_keys=True)
    expected_properties = json.dumps(properties, sort_keys=True)
    assert actual_properties == expected_properties, "Wrong properties"


def test_missing_sub_entities():
    """Test that ValueError is raised if an entity does not have entities attribute.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object without entities attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingSubEntitiesEntity(Entity):
        @property
        def entities(self):
            raise AttributeError()

    entity = _MissingSubEntitiesEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to get sub entities of the entity", "Wrong error"


def test_non_iterable_sub_entities():
    """Test that ValueError is raised if entity has a non-iterable object as its sub entities.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object with non-iterable sub entities.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableSubEntitiesEntity(Entity):
        @property
        def entities(self):
            return None

    entity = _NonIterableSubEntitiesEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to iterate over sub entities of the entity", (
        "Wrong error"
    )


def test_non_marshalable_sub_entities(non_marshalable_sub_entity):
    """Test that ValueError is raised if one of sub entities of the entity is not marshallable.

    1. Create a json marshaller.
    2. Try to call marshal_entity for an object with entities that are not marshalable.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonMarshalableSubEntitiesEntity(Entity):
        @property
        def entities(self):
            return [non_marshalable_sub_entity]

    entity = _NonMarshalableSubEntitiesEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to marshal sub entities of the entity", "Wrong error"


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
    2. Create an entity with specific sub entities.
    3. Replace marshal_embedded_link and marshal_embedded_representation of the marshaler so that
       it returns fake data.
    4. Marshal the entity.
    5. Check a key with the sub entities (fake data) in the marshaled data.
    """
    class _FixedSubEntitiesEntity(Entity):
        @property
        def entities(self):
            return sub_entities

    entity = _FixedSubEntitiesEntity()

    marshaler = JSONMarshaler()

    def _fake_marshal_embedded_link(embedded_link):
        return sub_entities.index(embedded_link)

    marshaler.marshal_embedded_link = _fake_marshal_embedded_link

    def _fake_marshal_embedded_representation(embedded_representation):
        return sub_entities.index(embedded_representation)

    marshaler.marshal_embedded_representation = _fake_marshal_embedded_representation

    entity_data = marshaler.marshal_entity(entity=entity)
    assert "entities" in entity_data, "Marshaled data does not have 'entities' key"
    assert entity_data["entities"] == list(range(len(sub_entities))), "Wrong entities"


def test_missing_links():
    """Test that ValueError is raised if an entity does not have links attribute.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object without links attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingLinksEntity(Entity):
        @property
        def links(self):
            raise AttributeError()

    entity = _MissingLinksEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to get entity's links", "Wrong error"


def test_non_iterable_links():
    """Test that ValueError is raised if entity has a non-iterable object as its links.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object with non-iterable links.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableLinksEntity(Entity):
        @property
        def links(self):
            return None

    entity = _NonIterableLinksEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to iterate over entity's links", "Wrong error"


def test_non_marshalable_links():
    """Test that ValueError is raised if one of links of the entity is not marshallable.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object with links that are not marshalable.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonMarshalableLinksEntity(Entity):
        @property
        def links(self):
            return [
                Link(relations=["first"], target="/first"),
                None,
                Link(relations=["last"], target="/last"),
                ]

    entity = _NonMarshalableLinksEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to marshal entity's links", "Wrong error"


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
    3. Marshal an entity with specific links.
    4. Check a key with the links (fake data) in the marshaled data.
    """
    class _FixedLinksEntity(Entity):
        @property
        def links(self):
            return links

    entity = _FixedLinksEntity()

    marshaler = JSONMarshaler()
    marshaler.marshal_link = links.index

    entity_data = marshaler.marshal_entity(entity=entity)
    assert "links" in entity_data, "Marshaled data does not have 'links' key"
    assert entity_data["links"] == list(range(len(links))), "Wrong links"


def test_missing_actions():
    """Test that ValueError is raised if an entity does not have actions attribute.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object without actions attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingActionsEntity(Entity):
        @property
        def actions(self):
            raise AttributeError()

    entity = _MissingActionsEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to get entity's actions", "Wrong error"


def test_non_iterable_actions():
    """Test that ValueError is raised if entity has a non-iterable object as its actions.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object with non-iterable actions.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonIterableActionsEntity(Entity):
        @property
        def actions(self):
            return None

    entity = _NonIterableActionsEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to iterate over entity's actions", "Wrong error"


def test_non_marshalable_actions():
    """Test that ValueError is raised if one of actions of the entity is not marshallable.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object with actions that are not marshalable.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _NonMarshalableActionsEntity(Entity):
        @property
        def actions(self):
            return [
                Action(name="first", target="/first"),
                None,
                Action(name="last", target="/last"),
                ]

    entity = _NonMarshalableActionsEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to marshal entity's actions", "Wrong error"


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
    3. Marshal an entity with specific actions.
    4. Check a key with the actions (fake data) in the marshaled data.
    """
    class _FixedActionsEntity(Entity):
        @property
        def actions(self):
            return actions

    entity = _FixedActionsEntity()

    marshaler = JSONMarshaler()
    marshaler.marshal_action = actions.index

    entity_data = marshaler.marshal_entity(entity=entity)
    assert "actions" in entity_data, "Marshaled data does not have 'actions' key"
    assert entity_data["actions"] == list(range(len(actions))), "Wrong actions"


def test_missing_title():
    """Test that ValueError is raised if an entity does not have title attribute.

    1. Create a json marshaller.
    2. Try to call marshal_entity method for an object without title attribute.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _MissingTitleEntity(Entity):
        @property
        def title(self):
            raise AttributeError()

    entity = _MissingTitleEntity()

    with pytest.raises(ValueError) as error_info:
        JSONMarshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Failed to get entity's title", "Wrong error"


@pytest.mark.parametrize(
    argnames="title,expected_title",
    argvalues=[
        ("entity title", "entity title"),
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
    2. Marshal an entity with a specific title.
    3. Check a key with the title in the marshaled data.
    """
    class _FixedTitleEntity(Entity):
        @property
        def title(self):
            return title

    entity = _FixedTitleEntity()

    entity_data = JSONMarshaler().marshal_entity(entity=entity)
    assert "title" in entity_data, "Marshaled data does not have 'title' key"
    assert entity_data["title"] == expected_title, "Wrong title"
