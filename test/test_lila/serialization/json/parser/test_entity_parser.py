"""Test cases for a parser class for entity data."""

import pytest

from lila.core.action import Action
from lila.core.link import Link, EmbeddedLink
from lila.core.entity import Entity, EmbeddedRepresentation
from lila.serialization.json.parser import JSONParser
from lila.serialization.json.entity import EntityParser


def test_unobtainable_classes():
    """Test that ValueError is raised if classes can't be retrieved from entity data.

    1. Create an entity parser for a non-subscriptable object.
    2. Try to call parse_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data=None, parser=JSONParser()).parse_classes()

    assert error_info.value.args[0] == "Failed to get classes from entity data", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if entity data has a non-iterable object for classes.

    1. Create an entity parser for a dictionary with non-iterable classes.
    2. Try to call parse_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data={"class": None}, parser=JSONParser()).parse_classes()

    assert error_info.value.args[0] == "Failed to iterate over classes from entity data", (
        "Wrong error"
        )


def test_missing_classes():
    """Test that empty tuple is returned if entity data don't have 'class' key.

    1. Create an entity parser for a dictionary without classes.
    2. Parse classes.
    3. Check that empty tuple is returned.
    """
    actual_classes = EntityParser(data={}, parser=JSONParser()).parse_classes()
    assert actual_classes == (), "Wrong classes"


@pytest.mark.parametrize(
    argnames="classes,expected_classes",
    argvalues=[
        ([], ()),
        (["entity class"], ("entity class", )),
        (
            ["first entity class", "second entity class"],
            ("first entity class", "second entity class"),
            ),
        (("first", None, [1, 2]), ("first", "None", "[1, 2]")),
        ],
    ids=[
        "Empty list",
        "Single class",
        "Multiple classes",
        "Non-string classes",
        ],
    )
def test_classes(classes, expected_classes):
    """Test that classes are properly parsed.

    1. Create an entity parser for a dictionary with specific classes.
    2. Parse classes.
    3. Check the parsed classes.
    """
    actual_classes = EntityParser(data={"class": classes}, parser=JSONParser()).parse_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_unobtainable_properties():
    """Test that ValueError is raised if properties can't be retrieved from entity data.

    1. Create an entity parser for a non-subscriptable object.
    2. Try to call parse_properties method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data=None, parser=JSONParser()).parse_properties()

    assert error_info.value.args[0] == "Failed to get properties from entity data", "Wrong error"


def test_non_parsable_properties():
    """Test that ValueError is raised if entity data has invalid JSON object as properties.

    1. Create an entity parser for a dictionary with invalid JSON object in 'properties'.
    2. Try to call parse_properties method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data={"properties": object()}, parser=JSONParser()).parse_properties()

    assert error_info.value.args[0] == "Failed to parse entity's properties", "Wrong error"


def test_missing_properties():
    """Test that empty dictionary is returned if entity data don't have 'properties' key.

    1. Create an entity parser for a dictionary without properties.
    2. Parse properties.
    3. Check that empty dictionary is returned.
    """
    actual_properties = EntityParser(data={}, parser=JSONParser()).parse_properties()
    assert actual_properties == {}, "Wrong properties"


@pytest.mark.parametrize(
    argnames="properties,expected_properties",
    argvalues=[
        ({"key": "value"}, {"key": "value"}),
        ({"key": {"nested key": "nested value"}}, {"key": {"nested key": "nested value"}}),
        ({"key1": ("item1", "item2")}, {"key1": ["item1", "item2"]}),
        ],
    ids=[
        "Simple dictionary",
        "Nested dictionary",
        "Iterable items",
        ],
    )
def test_properties(properties, expected_properties):
    """Test that properties are properly parsed.

    1. Create an entity parser for a dictionary with specific properties.
    2. Parse properties.
    3. Check the parsed properties.
    """
    parser = EntityParser(data={"properties": properties}, parser=JSONParser())
    actual_properties = parser.parse_properties()
    assert actual_properties == expected_properties, "Wrong properties"


def test_unobtainable_sub_entities():
    """Test that ValueError is raised if sub-entities data can't be retrieved from entity data.

    1. Create an entity parser for a non-subscriptable object.
    2. Try to call parse_entities method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data=None, parser=JSONParser()).parse_entities()

    assert error_info.value.args[0] == "Failed to get sub-entities data from entity data", (
        "Wrong error"
        )


def test_non_iterable_sub_entities():
    """Test that ValueError is raised if entity data has a non-iterable object for sub-entities.

    1. Create an entity parser for a dictionary with non-iterable sub-entities data.
    2. Try to call parse_entities method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data={"entities": None}, parser=JSONParser()).parse_entities()

    expected_message = "Failed to iterate over sub-entities data from entity data"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_non_parsable_sub_entities():
    """Test that ValueError is raised if one of sub-entities can't be parsed.

    1. Create json parser that raises exception when either parse_embedded_link or
       parse_embedded_representation is called.
    2. Create an entity parser with the parser.
    3. Try to call parse_entities method.
    4. Check that ValueError is raised.
    5. Check the error message.
    """
    class _SubEntityErrorParser(JSONParser):
        def parse_embedded_link(self, data):
            raise Exception()

        def parse_embedded_representation(self, data):
            raise Exception()

    parser = EntityParser(
        data={"entities": [{}, {"href": "/target"}]},
        parser=_SubEntityErrorParser(),
        )

    with pytest.raises(ValueError) as error_info:
        parser.parse_entities()

    assert error_info.value.args[0] == "Failed to parse entity's sub-entities", "Wrong error"


def test_missing_sub_entities():
    """Test that empty tuple is returned if entity data don't have 'entities' key.

    1. Create an entity parser for a dictionary without sub-entities.
    2. Parse sub-entities.
    3. Check that empty tuple is returned.
    """
    actual_sub_entities = EntityParser(data={}, parser=JSONParser()).parse_entities()
    assert actual_sub_entities == (), "Wrong sub-entities"


@pytest.mark.parametrize(
    argnames="sub_entities_data",
    argvalues=[
        [],
        [{"id": "single"}],
        [{"id": "first"}, {"id": "second"}],
        [{"href": "/target"}, {}]
        ],
    ids=[
        "Empty list",
        "Single sub-entity",
        "Multiple sub-entities",
        "Embedded link and representation",
        ],
    )
def test_sub_entities(sub_entities_data):
    """Test that sub-entities are properly parsed.

    1. Create json parser with overridden parse_embedded_link and parse_embedded_representation.
    2. Create an entity parser with the parser.
    3. Parse fields.
    4. Check the parsed fields.
    """
    class _SubEntitiesParser(JSONParser):
        def parse_embedded_link(self, data):
            if "href" not in data:
                pytest.fail("Try to parse embedded link instead of embedded representation")
            return sub_entities_data.index(data)

        def parse_embedded_representation(self, data):
            if "href" in data:
                pytest.fail("Try to parse embedded representation instead of embedded link")
            return sub_entities_data.index(data)

    parser = EntityParser(data={"entities": sub_entities_data}, parser=_SubEntitiesParser())
    actual_sub_entities = parser.parse_entities()
    assert actual_sub_entities == tuple(range(len(sub_entities_data))), "Wrong sub-entities"


def test_unobtainable_links():
    """Test that ValueError is raised if links data can't be retrieved from entity data.

    1. Create an entity parser for a non-subscriptable object.
    2. Try to call parse_links method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data=None, parser=JSONParser()).parse_links()

    assert error_info.value.args[0] == "Failed to get links data from entity data", "Wrong error"


def test_non_iterable_links():
    """Test that ValueError is raised if entity data has a non-iterable object for links.

    1. Create an entity parser for a dictionary with non-iterable links data.
    2. Try to call parse_links method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data={"links": None}, parser=JSONParser()).parse_links()

    assert error_info.value.args[0] == "Failed to iterate over links data from entity data", (
        "Wrong error"
        )


def test_non_parsable_links():
    """Test that ValueError is raised if one of links can't be parsed.

    1. Create json parser that raises exception when parse_link is called.
    2. Create an entity parser with the parser.
    3. Try to call parse_links method.
    4. Check that ValueError is raised.
    5. Check the error message.
    """
    class _LinkErrorParser(JSONParser):
        def parse_link(self, data):
            raise Exception()


    with pytest.raises(ValueError) as error_info:
        EntityParser(data={"links": [{}]}, parser=_LinkErrorParser()).parse_links()

    assert error_info.value.args[0] == "Failed to parse entity's links", "Wrong error"


def test_missing_links():
    """Test that empty tuple is returned if entity data don't have 'links' key.

    1. Create an entity parser for a dictionary without links.
    2. Parse links.
    3. Check that empty tuple is returned.
    """
    actual_links = EntityParser(data={}, parser=JSONParser()).parse_links()
    assert actual_links == (), "Wrong links"


@pytest.mark.parametrize(
    argnames="links_data",
    argvalues=[
        [],
        [{"id": "single"}],
        [{"id": "first"}, {"id": "second"}],
        ],
    ids=[
        "Empty list",
        "Single link",
        "Multiple links",
        ],
    )
def test_links(links_data):
    """Test that links are properly parsed.

    1. Create json parser.
    2. Replace parse_link method of the parser so that it returns fake data.
    3. Create an entity parser with the parser.
    4. Parse fields.
    5. Check the parsed fields.
    """
    json_parser = JSONParser()
    json_parser.parse_link = links_data.index

    actual_links = EntityParser(data={"links": links_data}, parser=json_parser).parse_links()
    assert actual_links == tuple(range(len(links_data))), "Wrong links"


def test_unobtainable_actions():
    """Test that ValueError is raised if actions data can't be retrieved from entity data.

    1. Create an entity parser for a non-subscriptable object.
    2. Try to call parse_actions method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data=None, parser=JSONParser()).parse_actions()

    assert error_info.value.args[0] == "Failed to get actions data from entity data", "Wrong error"


def test_non_iterable_actions():
    """Test that ValueError is raised if entity data has a non-iterable object for actions.

    1. Create an entity parser for a dictionary with non-iterable actions data.
    2. Try to call parse_actions method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data={"actions": None}, parser=JSONParser()).parse_actions()

    assert error_info.value.args[0] == "Failed to iterate over actions data from entity data", (
        "Wrong error"
        )


def test_non_parsable_actions():
    """Test that ValueError is raised if one of actions can't be parsed.

    1. Create json parser that raises exception when parse_action is called.
    2. Create an entity parser with the parser.
    3. Try to call parse_actions method.
    4. Check that ValueError is raised.
    5. Check the error message.
    """
    class _ActionErrorParser(JSONParser):
        def parse_action(self, data):
            raise Exception()


    with pytest.raises(ValueError) as error_info:
        EntityParser(data={"actions": [{}]}, parser=_ActionErrorParser()).parse_actions()

    assert error_info.value.args[0] == "Failed to parse entity's actions", "Wrong error"


def test_missing_actions():
    """Test that empty tuple is returned if entity data don't have 'actions' key.

    1. Create an entity parser for a dictionary without actions.
    2. Parse actions.
    3. Check that empty tuple is returned.
    """
    actual_actions = EntityParser(data={}, parser=JSONParser()).parse_actions()
    assert actual_actions == (), "Wrong actions"


@pytest.mark.parametrize(
    argnames="actions_data",
    argvalues=[
        [],
        [{"id": "single"}],
        [{"id": "first"}, {"id": "second"}],
        ],
    ids=[
        "Empty list",
        "Single action",
        "Multiple actions",
        ],
    )
def test_actions(actions_data):
    """Test that actions are properly parsed.

    1. Create json parser.
    2. Replace parse_action method of the parser so that it returns fake data.
    3. Create an entity parser with the parser.
    4. Parse fields.
    5. Check the parsed fields.
    """
    json_parser = JSONParser()
    json_parser.parse_action = actions_data.index

    parser = EntityParser(data={"actions": actions_data}, parser=json_parser)
    actual_actions = parser.parse_actions()
    assert actual_actions == tuple(range(len(actions_data))), "Wrong actions"


def test_unobtainable_title():
    """Test that ValueError is raised if title can't be retrieved from entity data.

    1. Create an entity parser for a non-subscriptable object.
    2. Try to call parse_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EntityParser(data=None, parser=JSONParser()).parse_title()

    assert error_info.value.args[0] == "Failed to get title from entity data", "Wrong error"


def test_missing_title():
    """Test that None is returned if entity data don't have 'title' key.

    1. Create an entity parser for a dictionary without title.
    2. Parse title.
    3. Check that None is returned.
    """
    actual_title = EntityParser(data={}, parser=JSONParser()).parse_title()
    assert actual_title is None, "Wrong title"


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
    """Test that title is properly parsed.

    1. Create an entity parser for dictionary with specific title.
    2. Parse a title.
    3. Check the parsed title.
    """
    actual_title = EntityParser(data={"title": title}, parser=JSONParser()).parse_title()
    assert actual_title == expected_title, "Wrong title"


def test_entity_creation_error():
    """Test that ValueError is raised if an error occurs during entity creation.

    1. Create an entity parser.
    2. Replace parse_classes method so that it returns invalid classes.
    3. Try to call parse method.
    4. Check that ValueError is raised.
    5. Check the error message.
    """
    parser = EntityParser(data={}, parser=JSONParser())
    parser.parse_classes = lambda: 1

    with pytest.raises(ValueError) as error_info:
        parser.parse()

    assert error_info.value.args[0] == "Failed to create an entity with provided data", (
        "Wrong error"
        )


def test_parse(component_validator):
    """Test that entity data is properly parsed.

    1. Create an entity.
    2. Create an entity parser.
    3. Replace parser methods so that they return predefined data.
    4. Parse the entity.
    5. Check the entity data.
    """
    entity = Entity(
        classes=("parsed class 1", "parsed class 2"),
        properties={"property 1": 1, "property 2": [1, 2]},
        entities=(
            EmbeddedLink(target="/embedded/link/target", relations=["relation"]),
            EmbeddedRepresentation(relations=["relation"]),
            ),
        links=[Link(target="/link/target", relations=["relation"])],
        actions=[Action(target="/action/target", name="action")],
        title="parsed title",
        )

    parser = EntityParser(data={}, parser=JSONParser())
    parser.parse_classes = lambda: entity.classes
    parser.parse_properties = lambda: entity.properties
    parser.parse_entities = lambda: entity.entities
    parser.parse_links = lambda: entity.links
    parser.parse_actions = lambda: entity.actions
    parser.parse_title = lambda: entity.title

    actual_entity = parser.parse()
    component_validator.validate_entity(actual_entity, entity)
