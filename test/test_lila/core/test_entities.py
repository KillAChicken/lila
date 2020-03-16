"""Test cases for Siren entities."""

import pytest

from lila.core.entity import Entity, EmbeddedRepresentation
from lila.core.link import Link, EmbeddedLink
from lila.core.action import Action


@pytest.mark.parametrize(
    argnames="title, expected_title",
    argvalues=[
        ("entity title", "entity title"),
        (None, None),
        (58892, "58892"),
    ],
    ids=[
        "String",
        "None",
        "Integer",
    ],
)
def test_title(title, expected_title):
    """Check title of an entity.

    1. Create an entity with different titles.
    2. Get title of the entity.
    3. Check the title.
    """
    entity = Entity(title=title)
    assert entity.title == expected_title, "Wrong title"


def test_default_title():
    """Check default title of an entity.

    1. Create an entity without specifying a title.
    2. Check the title of the entity.
    """
    entity = Entity()
    assert entity.title is None, "Wrong title"


@pytest.mark.parametrize(
    argnames="classes, expected_classes",
    argvalues=[
        (["entity-class1", "entity-class2"], ("entity-class1", "entity-class2")),
        ([], ()),
    ],
    ids=[
        "Happy path",
        "Empty list",
    ],
)
def test_classes(classes, expected_classes):
    """Check classes of an entity.

    1. Create an entity with different classes.
    2. Get classes of the entity.
    3. Check the entity.
    """
    entity = Entity(classes=classes)
    assert entity.classes == expected_classes, "Wrong classes"


def test_default_classes():
    """Check default classes of an entity.

    1. Create an entity without specifying classes.
    2. Check classes of the entity.
    """
    entity = Entity()
    assert entity.classes == (), "Wrong classes"


def test_invalid_classes():
    """Check that ValueError is raised if invalid classes are passed.

    1. Try to create an entity with non-iterable classes.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        Entity(classes=1)

    assert error_info.value.args[0] == "Classes must be iterable with string values"


@pytest.mark.parametrize(
    argnames="properties, expected_properties",
    argvalues=[
        ({"key1": "value1", "key2": "value2"}, {"key1": "value1", "key2": "value2"}),
        ([("key1", "value1"), ("key2", "value2")], {"key1": "value1", "key2": "value2"}),
        ({None: None}, {"None": None}),
        ({"iterable": ("value1", {"key": "value"})}, {"iterable": ["value1", {"key": "value"}]}),
    ],
    ids=[
        "Simple dictionary",
        "Iterable with items",
        "None key and value",
        "Nested structure",
    ],
)
def test_properties(properties, expected_properties):
    """Check properties of an entity.

    1. Create an entity with different properties.
    2. Get properties of the entity.
    3. Check the properties.
    4. Change the retrieved dictionary.
    5. Get properties of the entity again.
    6. Check that properties have not been updated.
    """
    entity = Entity(properties=properties)
    actual_properties = entity.properties
    assert actual_properties == expected_properties, "Wrong properties"

    actual_properties["new-key"] = "new value"
    assert entity.properties == expected_properties, "Wrong properies"


def test_default_properties():
    """Check default properties of an entity.

    1. Create an entity without specifying properties.
    2. Get properties of the entity.
    3. Check the properties.
    4. Change the retrieved dictionary.
    5. Get properties of the entity again.
    6. Check that properties have not been updated.
    """
    entity = Entity()
    actual_properties = entity.properties
    assert actual_properties == {}, "Wrong properties"

    actual_properties["new-key"] = "new value"
    assert entity.properties == {}, "Wrong properies"


@pytest.mark.parametrize(
    argnames="properties, error_message",
    argvalues=[
        (None, "Can't create dictionary from properties"),
        ({"key": object()}, "Unsupported value for property 'key'"),
    ],
    ids=[
        "Invalid dictionary",
        "Invalid value",
    ],
)
def test_invalid_properties(properties, error_message):
    """Check that ValueError is raised if invalid properties are passed.

    1. Try to create an entity with invalid properties.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        Entity(properties=properties)

    assert error_info.value.args[0] == error_message, "Wrong error message"


@pytest.mark.parametrize(
    argnames="links",
    argvalues=[
        [],
        [Link(relations=["next"], target="/single-link")],
        [
            Link(relations=["next"], target="/first-link"),
            Link(relations="previous", target="/second-link"),
        ],
    ],
    ids=[
        "Without links",
        "Single",
        "Several",
    ],
)
def test_links(links):
    """Check links of an entity.

    1. Create an entity with different number of links.
    2. Get links of the entity.
    3. Check the links.
    """
    entity = Entity(links=links)
    assert entity.links == tuple(links), "Wrong links"


def test_default_links():
    """Check default set of links of an entity.

    1. Create an entity without specifying links.
    2. Get links of the entity.
    3. Check the links.
    """
    entity = Entity()
    assert entity.links == (), "Wrong links"


@pytest.mark.parametrize(
    argnames="links",
    argvalues=[
        [None, Link(relations=["self"], target="/link")],
        [
            Link(relations=["next"], target="/first-link"),
            "/second-link",
            Link(relations=["previous"], target="/third-link"),
        ],
    ],
    ids=[
        "First link",
        "Link in the middle",
    ],
)
def test_incompatible_links(links):
    """Check that ValueError is raised if at least one of the links is of incompatible type.

    1. Try to create an entity with incompatible link type.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        Entity(links=links)

    assert error_info.value.args[0] == "Some of the links are of incompatible type"


@pytest.mark.parametrize(
    argnames="actions",
    argvalues=[
        [],
        [Action(name="single", target="/single-action")],
        [
            Action(name="first", target="/first-action"),
            Action(name="second", target="/second-action"),
        ],
    ],
    ids=[
        "Without actions",
        "Single",
        "Several",
    ],
)
def test_actions(actions):
    """Check actions of an entity.

    1. Create an entity with different number of actions.
    2. Get actions of the entity.
    3. Check the actions.
    """
    entity = Entity(actions=actions)
    assert entity.actions == tuple(actions), "Wrong actions"


def test_default_actions():
    """Check default set of actions of an entity.

    1. Create an entity without specifying actions.
    2. Get actions of the entity.
    3. Check the actions.
    """
    entity = Entity()
    assert entity.actions == (), "Wrong actions"


@pytest.mark.parametrize(
    argnames="actions",
    argvalues=[
        [None, Action(name="action", target="/action")],
        [
            Action(name="first", target="/first-action"),
            "/second-action",
            Action(name="third", target="/third-link"),
        ],
    ],
    ids=[
        "First action",
        "Action in the middle",
    ],
)
def test_incompatible_actions(actions):
    """Check that ValueError is raised if at least one of the actions is of incompatible type.

    1. Try to create an entity with incompatible action type.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        Entity(actions=actions)

    assert error_info.value.args[0] == "Some of the actions are of incompatible type"


def test_duplicated_action_names():
    """Check that ValueError is raised if some of the actions have the same name.

    1. Create 2 actions with the same name.
    1. Try to create an entity with the created actions.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    actions = [
        Action(name="duplicate", target="/first", title="First action with non-unique name"),
        Action(name="unique", target="/second", title="Action with unique name"),
        Action(name="duplicate", target="/third", title="Second action with non-unique name"),
        ]

    with pytest.raises(ValueError) as error_info:
        Entity(actions=actions)

    assert error_info.value.args[0] == "Some of the actions have the same name", "Wrong error"


@pytest.mark.parametrize(
    argnames="entities",
    argvalues=[
        [],
        [EmbeddedLink(relations=["self"], target="/self")],
        [EmbeddedRepresentation(relations=["self"])],
        [
            EmbeddedLink(relations=["first"], target="/first"),
            EmbeddedRepresentation(relations=["second"]),
            EmbeddedLink(relations=["third"], target="/third"),
            EmbeddedRepresentation(relations=["forth"]),
        ],
    ],
    ids=[
        "Without entities",
        "Single embedded link",
        "Single embedded representation",
        "Several enitities of different types",
    ],
)
def test_subentities(entities):
    """Check subentities of an entity.

    1. Create an entity with different sets of subentities.
    2. Get subentities of the entity.
    3. Check the subentities.
    """
    entity = Entity(entities=entities)
    assert entity.entities == tuple(entities), "Wrong subentities"


def test_default_subentities():
    """Check default set of subentities of an entity.

    1. Create an entity without specifying subentities.
    2. Get subentities of the entity.
    3. Check the subentities.
    """
    entity = Entity()
    assert entity.entities == (), "Wrong subentities"


@pytest.mark.parametrize(
    argnames="entities",
    argvalues=[
        [None, EmbeddedLink(relations=["self"], target="/self")],
        [
            EmbeddedLink(relations="first", target="/first-link"),
            "second",
            EmbeddedRepresentation(relations=["third"]),
        ],
        [Entity()],
    ],
    ids=[
        "First subentity",
        "Subentity in the middle",
        "Entity class",
    ],
)
def test_incompatible_subentities(entities):
    """Check that ValueError is raised if at least one of the entities is of incompatible type.

    1. Try to create an entity with incompatible type of subentity.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        Entity(entities=entities)

    assert error_info.value.args[0] == "Some of the entities are of incompatible type"
