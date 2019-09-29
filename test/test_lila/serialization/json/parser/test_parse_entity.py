"""Test cases for parse_entity method of JSON parser."""

from copy import deepcopy

import pytest

from lila.core.link import Link, EmbeddedLink
from lila.core.action import Action
from lila.core.entity import Entity, EmbeddedRepresentation
from lila.serialization.json.parser import JSONParser


def test_invalid_json():
    """Test that ValueError is raised if input data are not a valid JSON object.

    1. Create a json parser.
    2. Try to call parse_entity method with object() as data.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_entity(data=object())

    assert error_info.value.args[0] == "Specified data are not a valid JSON object", "Wrong error"


@pytest.mark.parametrize(
    argnames="classes",
    argvalues=[
        ("class1", "class2"),
        (),
        ],
    ids=[
        "Simple",
        "Empty",
        ],
    )
def test_classes(json_data_factory, classes):
    """Test that classes are properly parsed.

    1. Create a json parser.
    2. Parse an entity from a dictionary with specific classes.
    3. Check classes of the parsed entity.
    """
    entity_data = json_data_factory.create_entity_data(classes=classes)
    entity = JSONParser().parse_entity(entity_data)

    assert entity.classes == tuple(classes), "Wrong classes"


def test_missing_classes(json_data_factory):
    """Test that entity can be parsed if classes are not specified.

    1. Create a json parser.
    2. Parse an entity from a dictionary without 'class' key.
    3. Check that parsed entity has empty list of classes.
    """
    entity_data = json_data_factory.create_entity_data(classes=["class"])
    entity_data.pop("class", None)
    entity = JSONParser().parse_entity(entity_data)

    assert entity.classes == (), "Wrong classes"


@pytest.mark.parametrize(
    argnames="properties",
    argvalues=[
        {"key": "value"},
        {"key": {"nested key": "nested value"}},
        (("key1", "value2"), ("key2", "value2")),
        ],
    ids=[
        "Simple dictionary",
        "Nested dictionary",
        "Items iterable",
        ],
    )
def test_properties(json_data_factory, properties):
    """Test that properties are properly parsed.

    1. Create a json parser.
    2. Parse an entity from a dictionary with specific properties.
    3. Check properties of the parsed entity.
    """
    entity_data = json_data_factory.create_entity_data(properties=properties)
    entity = JSONParser().parse_entity(entity_data)

    assert entity.properties == dict(properties), "Wrong properties"


def test_missing_properties(json_data_factory):
    """Test that entity can be parsed if properties are not specified.

    1. Create a json parser.
    2. Parse an entity from a dictionary without 'properties' key.
    3. Check that parsed entity has empty dictionary as properties.
    """
    entity_data = json_data_factory.create_entity_data(properties={"key": "value"})
    entity_data.pop("properties", None)
    entity = JSONParser().parse_entity(entity_data)

    assert entity.properties == {}, "Wrong properties"


@pytest.mark.parametrize(
    argnames="sub_entities",
    argvalues=[
        (),
        (EmbeddedLink(relations=["self"], target="/target"), ),
        (
            EmbeddedLink(relations=["next"], target="/next"),
            EmbeddedLink(relations=["prev"], target="/previous"),
            ),
        (EmbeddedRepresentation(relations=["self"]), ),
        (EmbeddedRepresentation(relations=["next"]), EmbeddedRepresentation(relations=["prev"])),
        (
            EmbeddedLink(relations=["first"], target="/first"),
            EmbeddedRepresentation(relations=["self"]),
            EmbeddedLink(relations=["last"], target="/last"),
            ),
        ],
    ids=[
        "Without sub entities",
        "One embedded link",
        "Several embedded links",
        "One embedded representation",
        "Several embedded representations",
        "Both embedded links and representations",
        ],
    )
def test_sub_entities(json_data_factory, sub_entities):
    """Test that sub entities are properly parsed.

    1. Create a json parser.
    2. Decorate parse_embedded_link and parse_embedded_representation methods of the parser so that
       passed data and parsed sub entities are stored.
    3. Parse an entity from a dictionary with specific sub entities.
    4. Check that passed sub entities data are taken from the entity data.
    5. Check that sub entities of the entity are the parsed sub entities.
    """
    entity_data = json_data_factory.create_entity_data(entities=sub_entities)
    parser = JSONParser()

    passed_sub_entities_data = []
    parsed_sub_entities = []

    parse_embedded_link = parser.parse_embedded_link

    def _decorated_parse_embedded_link(data):
        passed_sub_entities_data.append(deepcopy(data))
        parsed_embedded_link = parse_embedded_link(data)
        parsed_sub_entities.append(parsed_embedded_link)
        return parsed_embedded_link

    parser.parse_embedded_link = _decorated_parse_embedded_link

    parse_embedded_representation = parser.parse_embedded_representation

    def _decorated_parse_embedded_representation(data):
        passed_sub_entities_data.append(deepcopy(data))
        parsed_embedded_representation = parse_embedded_representation(data)
        parsed_sub_entities.append(parsed_embedded_representation)
        return parsed_embedded_representation

    parser.parse_embedded_representation = _decorated_parse_embedded_representation

    # use deepcopy to catch a case when the passed entity data is accidentally changed
    entity = parser.parse_entity(deepcopy(entity_data))

    assert passed_sub_entities_data == entity_data["entities"], (
        "Wrong data is passed to either parse_embedded_link or parse_embedded_representation method"
        )
    assert entity.entities == tuple(parsed_sub_entities), "Wrong sub entities"


def test_missing_sub_entities(json_data_factory):
    """Test that entity can be parsed if sub entities are not specified.

    1. Create a json parser.
    2. Parse an entity from a dictionary without 'entities' key.
    3. Check that parsed entity has empty tuple of sub entities.
    """
    entity_data = json_data_factory.create_entity_data(
        entities=[EmbeddedRepresentation(relations=["relation"])],
        )
    entity_data.pop("entities", None)
    entity = JSONParser().parse_entity(entity_data)

    assert entity.entities == (), "Wrong sub entities"


@pytest.mark.parametrize(
    argnames="invalid_sub_entities_data",
    argvalues=[
        None,
        123,
        [{}],
        [{"href": "/target"}],
        [1],
        ],
    ids=[
        "None",
        "Non-iterable",
        "Invalid embedded representation",
        "Invalid embedded link",
        "Invalid type of data",
        ],
    )
def test_invalid_sub_entities(json_data_factory, invalid_sub_entities_data):
    """Test that ValueError is raised if sub entities data is invalid.

    1. Create a json parser.
    2. Try to parse an entity from a dictionary with invalid sub entities data.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    entity_data = json_data_factory.create_entity_data()
    entity_data["entities"] = invalid_sub_entities_data

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_entity(data=entity_data)

    assert error_info.value.args[0] == "Failed to parse sub entities of entity", "Wrong error"


@pytest.mark.parametrize(
    argnames="links",
    argvalues=[
        (),
        (Link(relations=["self"], target="/target"), ),
        (Link(relations=["next"], target="/next"), Link(relations=["prev"], target="/previous")),
        ],
    ids=[
        "Without links",
        "One link",
        "Several links",
        ],
    )
def test_links(json_data_factory, links):
    """Test that links are properly parsed.

    1. Create a json parser.
    2. Decorate parse_link method of the parser so that passed data and parsed links are stored.
    3. Parse an entity from a dictionary with specific links.
    4. Check that passed link data are taken from the entity data.
    5. Check that links of the entity are the parsed links.
    """
    entity_data = json_data_factory.create_entity_data(links=links)
    parser = JSONParser()

    parse_link = parser.parse_link

    passed_links_data = []
    parsed_links = []

    def _decorated_parse_link(data):
        passed_links_data.append(deepcopy(data))
        parsed_link = parse_link(data)
        parsed_links.append(parsed_link)
        return parsed_link

    parser.parse_link = _decorated_parse_link

    # use deepcopy to catch a case when the passed entity data is accidentally changed
    entity = parser.parse_entity(deepcopy(entity_data))

    assert passed_links_data == entity_data["links"], "Wrong data is passed to parse_link method"
    assert entity.links == tuple(parsed_links), "Wrong links"


def test_missing_links(json_data_factory):
    """Test that entity can be parsed if links are not specified.

    1. Create a json parser.
    2. Parse an entity from a dictionary without 'links' key.
    3. Check that parsed entity has empty tuple of links.
    """
    entity_data = json_data_factory.create_entity_data(
        links=[Link(relations=["relation"], target="/target")],
        )
    entity_data.pop("links", None)
    entity = JSONParser().parse_entity(entity_data)

    assert entity.links == (), "Wrong links"


@pytest.mark.parametrize(
    argnames="invalid_links_data",
    argvalues=[
        None,
        123,
        [{}],
        [1],
        ],
    ids=[
        "None",
        "Non-iterable",
        "Invalid link data",
        "Invalid type of data",
        ],
    )
def test_invalid_links(json_data_factory, invalid_links_data):
    """Test that ValueError is raised if links data is invalid.

    1. Create a json parser.
    2. Try to parse an entity from a dictionary with invalid links data.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    entity_data = json_data_factory.create_entity_data()
    entity_data["links"] = invalid_links_data

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_entity(data=entity_data)

    assert error_info.value.args[0] == "Failed to parse entity links", "Wrong error"


@pytest.mark.parametrize(
    argnames="actions",
    argvalues=[
        (),
        (Action(name="action", target="/target"), ),
        (Action(name="action1", target="/action1"), Action(name="action2", target="/action2")),
        ],
    ids=[
        "Without actions",
        "One action",
        "Several actions",
        ],
    )
def test_actions(json_data_factory, actions):
    """Test that actions are properly parsed.

    1. Create a json parser.
    2. Decorate parse_action method of the parser so that passed data and parsed actions are stored.
    3. Parse an entity from a dictionary with specific actions.
    4. Check that passed action data are taken from the entity data.
    5. Check that actions of the entity are the parsed actions.
    """
    entity_data = json_data_factory.create_entity_data(actions=actions)
    parser = JSONParser()

    parse_action = parser.parse_action

    passed_actions_data = []
    parsed_actions = []

    def _decorated_parse_action(data):
        passed_actions_data.append(deepcopy(data))
        parsed_action = parse_action(data)
        parsed_actions.append(parsed_action)
        return parsed_action

    parser.parse_action = _decorated_parse_action

    # use deepcopy to catch a case when the passed entity data is accidentally changed
    entity = parser.parse_entity(deepcopy(entity_data))

    assert passed_actions_data == entity_data["actions"], (
        "Wrong data is passed to parse_action method"
        )
    assert entity.actions == tuple(parsed_actions), "Wrong actions"


def test_missing_actions(json_data_factory):
    """Test that entity can be parsed if actions are not specified.

    1. Create a json parser.
    2. Parse an entity from a dictionary without 'actions' key.
    3. Check that parsed entity has empty tuple of actions.
    """
    entity_data = json_data_factory.create_entity_data(
        actions=[Action(name="name", target="/target")],
        )
    entity_data.pop("actions", None)
    entity = JSONParser().parse_entity(entity_data)

    assert entity.actions == (), "Wrong actions"


@pytest.mark.parametrize(
    argnames="invalid_actions_data",
    argvalues=[
        None,
        123,
        [{}],
        [1],
        ],
    ids=[
        "None",
        "Non-iterable",
        "Invalid action data",
        "Invalid type of data",
        ],
    )
def test_invalid_actions(json_data_factory, invalid_actions_data):
    """Test that ValueError is raised if actions data is invalid.

    1. Create a json parser.
    2. Try to parse an entity from a dictionary with invalid actions data.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    entity_data = json_data_factory.create_entity_data()
    entity_data["actions"] = invalid_actions_data

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_entity(data=entity_data)

    assert error_info.value.args[0] == "Failed to parse entity actions", "Wrong error"


@pytest.mark.parametrize(
    argnames="title",
    argvalues=[
        "simple title",
        u"Заголовок",
        "",
        None,
        ],
    ids=[
        "Simple",
        "Unicode",
        "Empty",
        "None",
        ],
    )
def test_title(json_data_factory, title):
    """Test that title is properly parsed.

    1. Create a json parser.
    2. Parse an entity from a dictionary with a specific title.
    3. Check the title of the parsed entity.
    """
    entity_data = json_data_factory.create_entity_data(title=title)
    entity = JSONParser().parse_entity(entity_data)

    assert entity.title == title, "Wrong title"


def test_missing_title(json_data_factory):
    """Test that entity can be parsed if title is not specified.

    1. Create a json parser.
    2. Parse an entity from a dictionary without 'title' key.
    3. Check that parsed entity has None as a title.
    """
    entity_data = json_data_factory.create_entity_data(title="title")
    entity_data.pop("title", None)
    entity = JSONParser().parse_entity(entity_data)

    assert entity.title is None, "Wrong title"


def test_creation_error(json_data_factory):
    """Test that ValueError from Entity creation is reraised by parser.

    1. Create a json parser.
    2. Try to parse an entity from a dictionary causing ValueError during the creation of
       an instance of Entity class.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    invalid_properties = [1, 2, 3]

    entity_data = json_data_factory.create_entity_data(properties=invalid_properties)
    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_entity(entity_data)

    with pytest.raises(ValueError) as expected_error_info:
        Entity(properties=invalid_properties)

    assert error_info.value.args[0] == expected_error_info.value.args[0], "Wrong error"
