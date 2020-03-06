"""Test cases for a marshaler class for an embedded representation."""

import json
from collections import namedtuple

import pytest

from lila.core.link import Link, EmbeddedLink
from lila.core.action import Action
from lila.core.entity import EmbeddedRepresentation
from lila.serialization.json.marshaler import JSONMarshaler
from lila.serialization.json.entity import (
    EmbeddedRepresentationMarshaler as RepresentationMarshaler,
    )


def test_missing_relations():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation does not have relations attribute.

    1. Create an embedded representation marshaler for an object without relations attribute.
    2. Try to call marshal_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    marshaler = RepresentationMarshaler(marshaler=JSONMarshaler(), embedded_representation=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_relations()

    assert error_info.value.args[0] == "Failed to get relations of the embedded representation", (
        "Wrong error"
        )


def test_non_iterable_relations():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation has a non-iterable object as its relations.

    1. Create an embedded representation marshaler for an object with non-iterable relations.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    RelationsRepresentation = namedtuple("RelationsRepresentation", "relations")
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=RelationsRepresentation(relations=None),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_relations()

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

    1. Create an embedded representation marshaler for an object with specific relations.
    2. Marshal relations.
    3. Check the marshaled relations.
    """
    RelationsRepresentation = namedtuple("RelationsRepresentation", "relations")
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=RelationsRepresentation(relations=relations),
        )

    actual_relations = marshaler.marshal_relations()
    assert actual_relations == expected_relations, "Wrong relations"


def test_missing_classes():
    """Test that ValueError is raised if an embedded representation does not have classes attribute.

    1. Create an embedded representation marshaler for an object without classes attribute.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = RepresentationMarshaler(marshaler=JSONMarshaler(), embedded_representation=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_classes()

    assert error_info.value.args[0] == "Failed to get classes of the embedded representation", (
        "Wrong error"
        )


def test_non_iterable_classes():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation has a non-iterable object as its classes.

    1. Create an embedded representation marshaler for an object with non-iterable classes.
    2. Try to call marshal_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    ClassesRepresentation = namedtuple("ClassesRepresentation", "classes")
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=ClassesRepresentation(classes=None),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_classes()

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

    1. Create an embedded representation marshaler for an object with specific classes.
    2. Marshal classes.
    3. Check the marshaled classes.
    """
    ClassesRepresentation = namedtuple("ClassesRepresentation", "classes")
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=ClassesRepresentation(classes=classes),
        )

    actual_classes = marshaler.marshal_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_missing_properties():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation does not have properties attribute.

    1. Create an embedded representation marshaler for an object without properties attribute.
    2. Try to call marshal_properties method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=object(),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_properties()

    expected_message = "Failed to get properties of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_invalid_properties():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if properties of an embedded representaion are not valid json object.

    1. Create an embedded representation marshaler for an object with invalid json object as
       its properties.
    2. Try to call marshal_properties method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    PropertiesRepresentation = namedtuple("PropertiesRepresentation", "properties")
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=PropertiesRepresentation(properties=object()),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_properties()

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

    1. Create an embedded representation marshaler for an object with specific properties.
    2. Marshal properties.
    3. Check the marshaled properties.
    """
    PropertiesRepresentation = namedtuple("PropertiesRepresentation", "properties")
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=PropertiesRepresentation(properties=properties),
        )
    actual_properties = json.dumps(marshaler.marshal_properties(), sort_keys=True)
    expected_properties = json.dumps(properties, sort_keys=True)
    assert actual_properties == expected_properties, "Wrong properties"


def test_missing_sub_entities():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation does not have entities attribute.

    1. Create an embedded representation marshaler for an object without entities attribute.
    2. Try to call marshal_entities method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    marshaler = RepresentationMarshaler(marshaler=JSONMarshaler(), embedded_representation=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_entities()

    expected_message = "Failed to get sub entities of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_non_iterable_sub_entities():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation has a non-iterable object as its sub-entities.

    1. Create an embedded representation marshaler for an object with non-iterable sub-entities.
    2. Try to call marshal_entities method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    SubEntitiesRepresentation = namedtuple("SubEntitiesRepresentation", "entities")
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=SubEntitiesRepresentation(entities=None),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_entities()

    expected_message = "Failed to iterate over sub entities of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


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
    # pylint: disable=line-too-long
    """Test that ValueError is raised if one of sub-entities of the embedded representation is not marshallable.

    1. Create json marshaler that raises exception when either marshal_embedded_link or
       marshal_embedded_representation is called.
    2. Create an embedded representation marshaler.
    3. Try to call marshal_entities method.
    4. Check that ValueError is raised.
    5. Check the error message.
    """
    # pylint: enable=line-too-long
    class _SubEntityErrorMarshaler(JSONMarshaler):
        def marshal_embedded_link(self, embedded_link):
            raise Exception()

        def marshal_embedded_representation(self, embedded_representation):
            raise Exception()

    SubEntitiesRepresentation = namedtuple("SubEntitiesRepresentation", "entities")
    marshaler = RepresentationMarshaler(
        marshaler=_SubEntityErrorMarshaler(),
        embedded_representation=SubEntitiesRepresentation(entities=[sub_entity]),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_entities()

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
    """Test that sub-entities are properly marshaled.

    1. Create an embedded representation marshaler.
    2. Replace marshal_embedded_link and marshal_embedded_representation of the marshaler
       so that it returns fake data.
    3. Marshal sub-entities.
    4. Check the marshaled sub-entities.
    """
    json_marshaler = JSONMarshaler()
    json_marshaler.marshal_embedded_link = sub_entities.index
    json_marshaler.marshal_embedded_representation = sub_entities.index

    SubEntitiesRepresentation = namedtuple("SubEntitiesRepresentation", "entities")
    marshaler = RepresentationMarshaler(
        marshaler=json_marshaler,
        embedded_representation=SubEntitiesRepresentation(entities=sub_entities),
        )

    actual_data = marshaler.marshal_entities()
    assert actual_data == list(range(len(sub_entities))), "Wrong entities"


def test_missing_links():
    """Test that ValueError is raised if an embedded representation does not have links attribute.

    1. Create an embedded representation marshaler for an object without links attribute.
    2. Try to call marshal_links method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = RepresentationMarshaler(marshaler=JSONMarshaler(), embedded_representation=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_links()

    expected_message = "Failed to get links of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_non_iterable_links():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation has a non-iterable object as its links.

    1. Create an embedded representation marshaler for an object with non-iterable links.
    2. Try to call marshal_links method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    LinksRepresentation = namedtuple("LinksRepresentation", "links")
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=LinksRepresentation(links=None),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_links()

    expected_message = "Failed to iterate over links of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_non_marshalable_links():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if one of links of the embedded representation is not marshallable.

    1. Create json marshaler that raises exception when marshal_link method is called.
    2. Create an embedded representation marshaler.
    3. Try to call marshal_links method.
    4. Check that ValueError is raised.
    5. Check the error message.
    """
    # pylint: enable=line-too-long
    class _LinkErrorMarshaler(JSONMarshaler):
        def marshal_link(self, link):
            raise Exception()

    LinksRepresentation = namedtuple("LinksRepresentation", "links")

    links = [Link(relations=["first"], target="/first")]
    marshaler = RepresentationMarshaler(
        marshaler=_LinkErrorMarshaler(),
        embedded_representation=LinksRepresentation(links=links),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_links()

    expected_message = "Failed to marshal links of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


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

    1. Create an embedded representation marshaler.
    2. Replace marshal_link of the marshaler so that it returns fake data.
    3. Marshal links.
    4. Check the marshaled links.
    """
    json_marshaler = JSONMarshaler()
    json_marshaler.marshal_link = links.index

    LinksRepresentation = namedtuple("LinksRepresentation", "links")
    marshaler = RepresentationMarshaler(
        marshaler=json_marshaler,
        embedded_representation=LinksRepresentation(links=links),
        )

    actual_data = marshaler.marshal_links()
    assert actual_data == list(range(len(links))), "Wrong links"


def test_missing_actions():
    """Test that ValueError is raised if an embedded representation does not have actions attribute.

    1. Create an embedded representation marshaler for an object without actions attribute.
    2. Try to call marshal_actions method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = RepresentationMarshaler(marshaler=JSONMarshaler(), embedded_representation=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_actions()

    expected_error = "Failed to get actions of the embedded representation"
    assert error_info.value.args[0] == expected_error, "Wrong error"


def test_non_iterable_actions():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if an embedded representation has a non-iterable object as its actions.

    1. Create an embedded representation marshaler for an object with non-iterable actions.
    2. Try to call marshal_actions method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    ActionsRepresentation = namedtuple("ActionsRepresentation", "actions")
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=ActionsRepresentation(actions=None),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_actions()

    expected_message = "Failed to iterate over actions of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_non_marshalable_actions():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if one of actions of the embedded representation is not marshallable.

    1. Create an embedded representation marshaler for an object with an action that
       can't be marshaled.
    2. Try to call marshal_actions method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    class _ActionErrorMarshaler(JSONMarshaler):
        def marshal_action(self, action):
            raise Exception()

    ActionsRepresentation = namedtuple("ActionsRepresentation", "actions")

    actions = [Action(name="action", target="/action")]
    marshaler = RepresentationMarshaler(
        marshaler=_ActionErrorMarshaler(),
        embedded_representation=ActionsRepresentation(actions=actions),
        )
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_actions()

    expected_message = "Failed to marshal actions of the embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error"


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

    1. Create an embedded representation marshaler.
    2. Replace marshal_action of the marshaler so that it returns fake data.
    3. Marshal actions.
    4. Check the marshaled actions.
    """
    json_marshaler = JSONMarshaler()
    json_marshaler.marshal_action = actions.index

    ActionsRepresentation = namedtuple("ActionsRepresentation", "actions")
    marshaler = RepresentationMarshaler(
        marshaler=json_marshaler,
        embedded_representation=ActionsRepresentation(actions=actions),
        )

    actual_data = marshaler.marshal_actions()
    assert actual_data == list(range(len(actions))), "Wrong actions"


def test_missing_title():
    """Test that ValueError is raised if an embedded representation does not have title attribute.

    1. Create an embedded representation marshaler for an object without title attribute.
    2. Try to call marshal_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    marshaler = RepresentationMarshaler(marshaler=JSONMarshaler(), embedded_representation=object())
    with pytest.raises(ValueError) as error_info:
        marshaler.marshal_title()

    expected_error = "Failed to get title of the embedded representation"
    assert error_info.value.args[0] == expected_error, "Wrong error"


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

    1. Create an embedded representation marshaler for an object with specific title.
    2. Marshal title.
    3. Check the marshaled title.
    """
    TitleRepresentation = namedtuple("TitleRepresentation", "title")
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=TitleRepresentation(title=title),
        )

    actual_title = marshaler.marshal_title()
    assert actual_title == expected_title, "Wrong title"


def test_marshal():
    """Test that data of an embedded representation is properly marshaled.

    1. Create an embedded representation.
    2. Create an embedded representation marshaler for the representation.
    3. Replace marshaler methods so that they return predefined data.
    4. Marshal the representation.
    5. Check the marshaled data.
    """
    marshaler = RepresentationMarshaler(
        marshaler=JSONMarshaler(),
        embedded_representation=EmbeddedRepresentation(relations=["self"]),
        )
    marshaler.marshal_relations = lambda: "marshal_relations"
    marshaler.marshal_classes = lambda: "marshal_classes"
    marshaler.marshal_properties = lambda: "marshal_properties"
    marshaler.marshal_entities = lambda: "marshal_entities"
    marshaler.marshal_links = lambda: "marshal_links"
    marshaler.marshal_actions = lambda: "marshal_actions"
    marshaler.marshal_title = lambda: "marshal_title"

    actual_data = marshaler.marshal()
    expected_data = {
        "rel": "marshal_relations",
        "class": "marshal_classes",
        "properties": "marshal_properties",
        "entities": "marshal_entities",
        "links": "marshal_links",
        "actions": "marshal_actions",
        "title": "marshal_title",
        }
    assert actual_data == expected_data, "Embedded represenation is not properly marshaled"
