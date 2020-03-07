"""Test cases for a marshaler class for an entity."""

import json
from collections import namedtuple

import pytest

from lila.core.link import Link, EmbeddedLink
from lila.core.action import Action
from lila.core.entity import Entity, EmbeddedRepresentation
from lila.serialization.json.marshaler import JSONMarshaler
from lila.serialization.json.entity import EntityMarshaler


def test_missing_classes():
    """Test that ValueError is raised if an entity does not have classes attribute.

    1. Create an entity marshaler for an object without classes attribute.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_classes()

    assert error_info.value.args[0] == "Failed to get entity's classes", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if an entity provides a non-iterable object as its classes.

    1. Create an entity marshaler for an object with non-iterable classes.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    ClassesEntity = namedtuple("ClassesEntity", "classes")
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=ClassesEntity(classes=None))
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_classes()

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

    1. Create an entity marshaler for an object with specific classes.
    2. Marshal classes.
    3. Check the marshaled classes.
    """
    ClassesEntity = namedtuple("ClassesEntity", "classes")
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=ClassesEntity(classes=classes))

    actual_classes = marshaler.marshal_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_missing_properties():
    """Test that ValueError is raised if an entity does not have properties attribute.

    1. Create an entity marshaler for an object without properties attribute.
    2. Try to call marshal_properties method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_properties()

    assert error_info.value.args[0] == "Failed to get entity's properties", "Wrong error"


def test_invalid_properties():
    """Test that ValueError is raised if entity's properties are not valid json object.

    1. Create an entity marshaler for an object with invalid json object as its properties.
    2. Try to call marshal_properties method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    PropertiesEntity = namedtuple("PropertiesEntity", "properties")
    marshaler = EntityMarshaler(
        marshaler=JSONMarshaler(),
        entity=PropertiesEntity(properties=object()),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_properties()

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

    1. Create an entity marshaler for an object with specific properties.
    2. Marshal properties.
    3. Check the marshaled properties.
    """
    PropertiesEntity = namedtuple("PropertiesEntity", "properties")
    marshaler = EntityMarshaler(
        marshaler=JSONMarshaler(),
        entity=PropertiesEntity(properties=properties),
        )
    actual_properties = json.dumps(marshaler.marshal_properties(), sort_keys=True)
    expected_properties = json.dumps(properties, sort_keys=True)
    assert actual_properties == expected_properties, "Wrong properties"


def test_missing_sub_entities():
    """Test that ValueError is raised if an entity does not have entities attribute.

    1. Create an entity marshaler for an object without entities attribute.
    2. Try to call marshal_entities method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_entities()

    assert error_info.value.args[0] == "Failed to get sub entities of the entity", "Wrong error"


def test_non_iterable_sub_entities():
    """Test that ValueError is raised if an entity has a non-iterable object as its sub-entities.

    1. Create an entity marshaler for an object with non-iterable sub-entities.
    2. Try to call marshal_entities method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    SubEntitiesEntity = namedtuple("SubEntitiesEntity", "entities")
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=SubEntitiesEntity(entities=None))
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_entities()

    assert error_info.value.args[0] == "Failed to iterate over sub entities of the entity", (
        "Wrong error"
    )


@pytest.mark.parametrize(
    argnames="sub_entity",
    argvalues=[
        EmbeddedLink(target="/embedded/link", relations=["relation"]),
        EmbeddedRepresentation(relations=["relation"]),
        ],
    ids=[
        "Link",
        "Representation",
        ],
    )
def test_non_marshalable_sub_entities(sub_entity):
    """Test that ValueError is raised if one of sub-entities of the entity is not marshallable.

    1. Create json marshaler that raises exception when either marshal_embedded_link or
       marshal_embedded_representation is called.
    2. Create an entity marshaler.
    3. Try to call marshal_entities method.
    4. Check that ValueError is raised.
    5. Check the error message.
    """
    class _SubEntityErrorMarshaler(JSONMarshaler):
        def marshal_embedded_link(self, embedded_link):
            raise Exception()

        def marshal_embedded_representation(self, embedded_representation):
            raise Exception()

    SubEntitiesEntity = namedtuple("SubEntitiesEntity", "entities")
    marshaler = EntityMarshaler(
        marshaler=_SubEntityErrorMarshaler(),
        entity=SubEntitiesEntity(entities=[sub_entity]),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_entities()

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
    """Test that sub-entities are properly marshaled.

    1. Create an entity marshaler.
    2. Replace marshal_embedded_link and marshal_embedded_representation of the marshaler
       so that it returns fake data.
    3. Marshal sub-entities.
    4. Check the marshaled sub-entities.
    """
    json_marshaler = JSONMarshaler()
    json_marshaler.marshal_embedded_link = sub_entities.index
    json_marshaler.marshal_embedded_representation = sub_entities.index

    SubEntitiesEntity = namedtuple("SubEntitiesEntity", "entities")
    marshaler = EntityMarshaler(
        marshaler=json_marshaler,
        entity=SubEntitiesEntity(entities=sub_entities),
        )

    actual_data = marshaler.marshal_entities()
    assert actual_data == list(range(len(sub_entities))), "Wrong entities"


def test_missing_links():
    """Test that ValueError is raised if an entity does not have links attribute.

    1. Create an entity marshaler for an object without links attribute.
    2. Try to call marshal_links method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_links()

    assert error_info.value.args[0] == "Failed to get entity's links", "Wrong error"


def test_non_iterable_links():
    """Test that ValueError is raised if an entity provides a non-iterable object as its links.

    1. Create an entity marshaler for an object with non-iterable links.
    2. Try to call marshal_links method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    LinksEntity = namedtuple("LinksEntity", "links")
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=LinksEntity(links=None))
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_links()

    assert error_info.value.args[0] == "Failed to iterate over entity's links", "Wrong error"


def test_non_marshalable_links():
    """Test that ValueError is raised if one of links of the entity is not marshallable.

    1. Create json marshaler that raises exception when marshal_link method is called.
    2. Create an entity marshaler.
    3. Try to call marshal_links method.
    4. Check that ValueError is raised.
    5. Check the error message.
    """
    class _LinkErrorMarshaler(JSONMarshaler):
        def marshal_link(self, link):
            raise Exception()

    LinksEntity = namedtuple("LinksEntity", "links")

    links = [Link(relations=["first"], target="/first")]
    marshaler = EntityMarshaler(marshaler=_LinkErrorMarshaler(), entity=LinksEntity(links=links))
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_links()

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

    1. Create an entity marshaler.
    2. Replace marshal_link of the marshaler so that it returns fake data.
    3. Marshal links.
    4. Check the marshaled links.
    """
    json_marshaler = JSONMarshaler()
    json_marshaler.marshal_link = links.index

    LinksEntity = namedtuple("LinksEntity", "links")
    marshaler = EntityMarshaler(marshaler=json_marshaler, entity=LinksEntity(links=links))

    actual_data = marshaler.marshal_links()
    assert actual_data == list(range(len(links))), "Wrong links"


def test_missing_actions():
    """Test that ValueError is raised if an entity does not have actions attribute.

    1. Create an entity marshaler for an object without actions attribute.
    2. Try to call marshal_actions method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_actions()

    assert error_info.value.args[0] == "Failed to get entity's actions", "Wrong error"


def test_non_iterable_actions():
    """Test that ValueError is raised if an entity provides a non-iterable object as its actions.

    1. Create an entity marshaler for an object with non-iterable actions.
    2. Try to call marshal_actions method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    ActionsEntity = namedtuple("ActionsEntity", "actions")
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=ActionsEntity(actions=None))
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_actions()

    assert error_info.value.args[0] == "Failed to iterate over entity's actions", "Wrong error"


def test_non_marshalable_actions():
    """Test that ValueError is raised if one of actions of the entity is not marshallable.

    1. Create an entity marshaler for an object with an action that can't be marshaled.
    2. Try to call marshal_actions method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    class _ActionErrorMarshaler(JSONMarshaler):
        def marshal_action(self, action):
            raise Exception()

    ActionsEntity = namedtuple("ActionsEntity", "actions")

    actions = [Action(name="action", target="/action")]
    marshaler = EntityMarshaler(
        marshaler=_ActionErrorMarshaler(),
        entity=ActionsEntity(actions=actions),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_actions()

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

    1. Create an entity marshaler.
    2. Replace marshal_action of the marshaler so that it returns fake data.
    3. Marshal actions.
    4. Check the marshaled actions.
    """
    json_marshaler = JSONMarshaler()
    json_marshaler.marshal_action = actions.index

    ActionsEntity = namedtuple("ActionsEntity", "actions")
    marshaler = EntityMarshaler(marshaler=json_marshaler, entity=ActionsEntity(actions=actions))

    actual_data = marshaler.marshal_actions()
    assert actual_data == list(range(len(actions))), "Wrong actions"


def test_missing_title():
    """Test that ValueError is raised if an entity does not have title attribute.

    1. Create an entity marshaler for an object without title attribute.
    2. Try to call marshal_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_title()

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

    1. Create an entity marshaler for an object with specific title.
    2. Marshal title.
    3. Check the marshaled title.
    """
    TitleEntity = namedtuple("TitleEntity", "title")
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=TitleEntity(title=title))

    actual_title = marshaler.marshal_title()
    assert actual_title == expected_title, "Wrong title"


def test_marshal():
    """Test that entity data is properly marshaled.

    1. Create an entity.
    2. Create an entity marshaler for the entity.
    3. Replace marshaler methods so that they return predefined data.
    4. Marshal the entity.
    5. Check the marshaled data.
    """
    marshaler = EntityMarshaler(marshaler=JSONMarshaler(), entity=Entity())
    marshaler.marshal_classes = lambda: "marshal_classes"
    marshaler.marshal_properties = lambda: "marshal_properties"
    marshaler.marshal_entities = lambda: "marshal_entities"
    marshaler.marshal_links = lambda: "marshal_links"
    marshaler.marshal_actions = lambda: "marshal_actions"
    marshaler.marshal_title = lambda: "marshal_title"

    actual_data = marshaler.marshal()
    expected_data = {
        "class": "marshal_classes",
        "properties": "marshal_properties",
        "entities": "marshal_entities",
        "links": "marshal_links",
        "actions": "marshal_actions",
        "title": "marshal_title",
        }
    assert actual_data == expected_data, "Entity is not properly marshaled"
