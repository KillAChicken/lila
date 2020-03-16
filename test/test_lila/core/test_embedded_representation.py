"""Test cases for Siren embedded representation."""

import pytest

from lila.core.entity import Entity, EmbeddedRepresentation
from lila.core.link import Link, EmbeddedLink
from lila.core.action import Action


DEFAULT_RELATIONS = ("subentity", )


@pytest.mark.parametrize(
    argnames="relations, expected_relations",
    argvalues=[
        (["subentity", "representation"], ("subentity", "representation")),
    ],
    ids=[
        "Happy path",
    ],
)
def test_relations(relations, expected_relations):
    """Test relations of an embedded representation.

    1. Create an embedded representation with different relations.
    2. Get relations.
    3. Check the relations.
    """
    representation = EmbeddedRepresentation(relations=relations)
    assert representation.relations == expected_relations, "Wrong relations"


def test_invalid_relations():
    """Check that ValueError is raised if invalid relations are passed.

    1. Try to create an embedded representation with non-iterable relations.
    2. Check that ValueError is raised.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedRepresentation(relations=None)

    assert error_info.value.args[0] == "Relations must be iterable with string values"


def test_missing_relations():
    """Check that ValueError is raised if relations list is empty.

    1. Try to create an embedded representation with empty list of relations.
    2. Check that ValueError is raised.
    3. Check error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedRepresentation(relations=[])

    expected_message = "No relations are passed to create an embedded representation"
    assert error_info.value.args[0] == expected_message, "Wrong error message"


@pytest.mark.parametrize(
    argnames="title, expected_title",
    argvalues=[
        ("representation title", "representation title"),
        (None, None),
        (3893, "3893"),
    ],
    ids=[
        "String",
        "None",
        "Integer",
    ],
)
def test_title(title, expected_title):
    """Check title of an embedded representation.

    1. Create an embedded representation with different titles.
    2. Get title of the representation.
    3. Check the title.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS, title=title)
    assert representation.title == expected_title, "Wrong title"


def test_default_title():
    """Check default title of an embedded representation.

    1. Create an embedded representation without specifying a title.
    2. Check the title of the representation.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS)
    assert representation.title is None, "Wrong title"


@pytest.mark.parametrize(
    argnames="classes, expected_classes",
    argvalues=[
        (["representation1", "representation2"], ("representation1", "representation2")),
        ([], ()),
    ],
    ids=[
        "Happy path",
        "Empty list",
    ],
)
def test_classes(classes, expected_classes):
    """Check classes of an embedded representation.

    1. Create an embedded representation with different classes.
    2. Get classes of the representation.
    3. Check the classes.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS, classes=classes)
    assert representation.classes == expected_classes, "Wrong classes"


def test_default_classes():
    """Check default classes of an embedded representation.

    1. Create an embedded representation without specifying classes.
    2. Check classes of the representation.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS)
    assert representation.classes == (), "Wrong classes"


def test_invalid_classes():
    """Check that ValueError is raised if invalid classes are passed.

    1. Try to create an embedded representation with non-iterable classes.
    2. Check that ValueError is raised.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedRepresentation(relations=DEFAULT_RELATIONS, classes=1)

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
    """Check properties of an embedded representation.

    1. Create an embedded representation with different properties.
    2. Get properties of the representation.
    3. Check the properties.
    4. Change the retrieved dictionary.
    5. Get properties of the representation again.
    6. Check that properties have not been updated.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS, properties=properties)
    actual_properties = representation.properties
    assert actual_properties == expected_properties, "Wrong properties"

    actual_properties["new-key"] = "new value"
    assert representation.properties == expected_properties, "Wrong properies"


def test_default_properties():
    """Check default properties of an embedded representation.

    1. Create an embedded representation without specifying properties.
    2. Get properties of the representation.
    3. Check the properties.
    4. Change the retrieved dictionary.
    5. Get properties of the representation again.
    6. Check that properties have not been updated.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS)
    actual_properties = representation.properties
    assert actual_properties == {}, "Wrong properties"

    actual_properties["new-key"] = "new value"
    assert representation.properties == {}, "Wrong properies"


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

    1. Try to create an embedded representation with invalid properties.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedRepresentation(relations=DEFAULT_RELATIONS, properties=properties)

    assert error_info.value.args[0] == error_message, "Wrong error message"


@pytest.mark.parametrize(
    argnames="links",
    argvalues=[
        [],
        [Link(relations=["first"], target="/single-link")],
        [
            Link(relations=["first"], target="/first-link"),
            Link(relations="last", target="/second-link"),
        ],
    ],
    ids=[
        "Without links",
        "Single",
        "Several",
    ],
)
def test_links(links):
    """Check links of an embedded representation.

    1. Create an embedded representation with different number of links.
    2. Get links of the representation.
    3. Check the links.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS, links=links)
    assert representation.links == tuple(links), "Wrong links"


def test_default_links():
    """Check default set of links of an embedded representation.

    1. Create an embedded representation without specifying links.
    2. Get links of the representation.
    3. Check the links.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS)
    assert representation.links == (), "Wrong links"


@pytest.mark.parametrize(
    argnames="links",
    argvalues=[
        [None, Link(relations=["home"], target="/link")],
        [
            Link(relations=["first"], target="/first-link"),
            "/second-link",
            Link(relations=["last"], target="/third-link"),
        ],
    ],
    ids=[
        "First link",
        "Link in the middle",
    ],
)
def test_incompatible_links(links):
    """Check that ValueError is raised if at least one of the links is of incompatible type.

    1. Try to create an embedded representation with incompatible link type.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedRepresentation(relations=DEFAULT_RELATIONS, links=links)

    assert error_info.value.args[0] == "Some of the links are of incompatible type"


@pytest.mark.parametrize(
    argnames="actions",
    argvalues=[
        [],
        [Action(name="action", target="/single-action")],
        [
            Action(name="one", target="/first-action"),
            Action(name="two", target="/second-action"),
        ],
    ],
    ids=[
        "Without actions",
        "Single",
        "Several",
    ],
)
def test_actions(actions):
    """Check actions of an embedded representation.

    1. Create an embedded representation with different number of actions.
    2. Get actions of the representation.
    3. Check the actions.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS, actions=actions)
    assert representation.actions == tuple(actions), "Wrong actions"


def test_default_actions():
    """Check default set of actions of an embedded representation.

    1. Create an embedded representation without specifying actions.
    2. Get actions of the representation.
    3. Check the actions.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS)
    assert representation.actions == (), "Wrong actions"


@pytest.mark.parametrize(
    argnames="actions",
    argvalues=[
        [None, Action(name="single", target="/action")],
        [
            Action(name="one", target="/first-action"),
            "/second-action",
            Action(name="three", target="/third-link"),
        ],
    ],
    ids=[
        "First action",
        "Action in the middle",
    ],
)
def test_incompatible_actions(actions):
    """Check that ValueError is raised if at least one of the actions is of incompatible type.

    1. Try to create an embedded representation with incompatible action type.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedRepresentation(relations=DEFAULT_RELATIONS, actions=actions)

    assert error_info.value.args[0] == "Some of the actions are of incompatible type"


def test_duplicated_action_names():
    """Check that ValueError is raised if some of the actions have the same name.

    1. Create 2 actions with the same name.
    1. Try to create an embedded representation with the created actions.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    actions = [
        Action(name="duplicate", target="/first", title="First action with non-unique name"),
        Action(name="unique", target="/second", title="Action with unique name"),
        Action(name="duplicate", target="/third", title="Second action with non-unique name"),
        ]

    with pytest.raises(ValueError) as error_info:
        EmbeddedRepresentation(relations=DEFAULT_RELATIONS, actions=actions)

    assert error_info.value.args[0] == "Some of the actions have the same name", "Wrong error"


@pytest.mark.parametrize(
    argnames="entities",
    argvalues=[
        [],
        [EmbeddedLink(relations=["self"], target="/self")],
        [
            EmbeddedRepresentation(
                relations=["self"],
                entities=[EmbeddedRepresentation(relations=["self"])],
            ),
        ],
        [
            EmbeddedRepresentation(relations=["first"]),
            EmbeddedLink(relations=["second"], target="/second"),
            EmbeddedRepresentation(relations=["third"]),
            EmbeddedLink(relations=["forth"], target="/forth"),
        ],
    ],
    ids=[
        "Without entities",
        "Single embedded link",
        "Single embedded representation with subentities",
        "Several enitities of different types",
    ],
)
def test_subentities(entities):
    """Check subentities of an embedded representation.

    1. Create an embedded representation with different sets of subentities.
    2. Get subentities of the representation.
    3. Check the subentities.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS, entities=entities)
    assert representation.entities == tuple(entities), "Wrong subentities"


def test_default_subentities():
    """Check default set of subentities of an embedded representation.

    1. Create an embedded representation without specifying subentities.
    2. Get subentities of the representation.
    3. Check the subentities.
    """
    representation = EmbeddedRepresentation(relations=DEFAULT_RELATIONS)
    assert representation.entities == (), "Wrong subentities"


@pytest.mark.parametrize(
    argnames="entities",
    argvalues=[
        [None, EmbeddedRepresentation(relations=["self"])],
        [
            EmbeddedRepresentation(relations=["first"]),
            "second",
            EmbeddedLink(relations="third", target="/third-link"),
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

    1. Try to create an embedded representation with incompatible type of subentity.
    2. Check that ValueError is raised.
    3. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedRepresentation(relations=DEFAULT_RELATIONS, entities=entities)

    assert error_info.value.args[0] == "Some of the entities are of incompatible type"
