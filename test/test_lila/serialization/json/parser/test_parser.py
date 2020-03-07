"""Test cases for JSON parser."""

import pytest

from lila.serialization.json.parser import JSONParser
from lila.serialization.json.field import FieldParser
from lila.serialization.json.action import ActionParser
from lila.serialization.json.link import LinkParser, EmbeddedLinkParser
from lila.serialization.json.entity import EntityParser, EmbeddedRepresentationParser


class _CustomParser:
    """Class to be used as custom parser factory for Siren components."""

    def __init__(self, component):
        self.__component = component

    def parse(self):
        """Simple parser implementation to return predefined component."""
        return self.__component

    def __call__(self, *args, **kwargs):
        return self


def test_default_field_parser(monkeypatch):
    """Test that json parser use FieldParser to parse a field.

    1. Create json parser.
    2. Replace parse method of FieldParser so that it returns fake data.
    3. Parse a field.
    4. Check that returned field is the same as the one from the mocked method.
    """
    monkeypatch.setattr(FieldParser, "parse", lambda self: "Parsed field")

    parsed_field = JSONParser().parse_field({})
    assert parsed_field == "Parsed field", "Wrong field"


def test_custom_field_parser():
    """Test that json parser use custom parser to parse a field.

    1. Create a sub-class of JSONParser with redefined create_field_parser factory.
    2. Create json parser from the sub-class.
    3. Parse a field.
    4. Check that custom parser is used to parse a field.
    """
    class _CustomFieldParser(JSONParser):
        create_field_parser = _CustomParser("Custom parsed field")

    parsed_field = _CustomFieldParser().parse_field({})
    assert parsed_field == "Custom parsed field", "Wrong field"


def test_invalid_field():
    """Test that error is propagated from field parser to json parser.

    1. Create json parser.
    2. Try to parse a field from invalid data.
    3. Check that error is raised.
    4. Check that error is the same as one that field parser raises.
    """
    invalid_field_data = object()
    parser = JSONParser()
    with pytest.raises(ValueError) as actual_error_info:
        parser.parse_field(invalid_field_data)

    with pytest.raises(ValueError) as expected_error_info:
        parser.create_field_parser(invalid_field_data).parse()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )


def test_default_action_parser(monkeypatch):
    """Test that json parser use ActionParser to parse an action.

    1. Create json parser.
    2. Replace parse method of ActionParser so that it returns fake data.
    3. Parse an action.
    4. Check that returned action is the same as the one from the mocked method.
    """
    monkeypatch.setattr(ActionParser, "parse", lambda self: "Parsed action")

    parsed_action = JSONParser().parse_action({})
    assert parsed_action == "Parsed action", "Wrong action"


def test_custom_action_parser():
    """Test that json parser use custom parser to parse an action.

    1. Create a sub-class of JSONParser with redefined create_action_parser factory.
    2. Create json parser from the sub-class.
    3. Parse an action.
    4. Check that custom parser is used to parse an action.
    """
    class _CustomActionParser(JSONParser):
        create_action_parser = _CustomParser("Custom parsed action")

    parsed_action = _CustomActionParser().parse_action({})
    assert parsed_action == "Custom parsed action", "Wrong action"


def test_invalid_action():
    """Test that error is propagated from action parser to json parser.

    1. Create json parser.
    2. Try to parse an action from invalid data.
    3. Check that error is raised.
    4. Check that error is the same as one that action parser raises.
    """
    invalid_action_data = object()
    parser = JSONParser()
    with pytest.raises(ValueError) as actual_error_info:
        parser.parse_action(invalid_action_data)

    with pytest.raises(ValueError) as expected_error_info:
        parser.create_action_parser(invalid_action_data).parse()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )


def test_default_link_parser(monkeypatch):
    """Test that json parser use LinkParser to parse a link.

    1. Create json parser.
    2. Replace parse method of LinkParser so that it returns fake data.
    3. Parse a link.
    4. Check that returned link is the same as the one from the mocked method.
    """
    monkeypatch.setattr(LinkParser, "parse", lambda self: "Parsed link")

    parsed_link = JSONParser().parse_link({})
    assert parsed_link == "Parsed link", "Wrong link"


def test_custom_link_parser():
    """Test that json parser use custom parser to parse a link.

    1. Create a sub-class of JSONParser with redefined create_link_parser factory.
    2. Create json parser from the sub-class.
    3. Parse a link.
    4. Check that custom parser is used to parse a link.
    """
    class _CustomLinkParser(JSONParser):
        create_link_parser = _CustomParser("Custom parsed link")

    parsed_link = _CustomLinkParser().parse_link({})
    assert parsed_link == "Custom parsed link", "Wrong link"


def test_invalid_link():
    """Test that error is propagated from link parser to json parser.

    1. Create json parser.
    2. Try to parse a link from invalid data.
    3. Check that error is raised.
    4. Check that error is the same as one that link parser raises.
    """
    invalid_link_data = object()
    parser = JSONParser()
    with pytest.raises(ValueError) as actual_error_info:
        parser.parse_link(invalid_link_data)

    with pytest.raises(ValueError) as expected_error_info:
        parser.create_link_parser(invalid_link_data).parse()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )


def test_default_embedded_link_parser(monkeypatch):
    """Test that json parser use EmbeddedLinkParser to parse an embedded link.

    1. Create json parser.
    2. Replace parse method of EmbeddedLinkParser so that it returns fake data.
    3. Parse an embedded link.
    4. Check that returned embedded link is the same as the one from the mocked method.
    """
    monkeypatch.setattr(EmbeddedLinkParser, "parse", lambda self: "Parsed embedded link")

    parsed_link = JSONParser().parse_embedded_link({})
    assert parsed_link == "Parsed embedded link", "Wrong embedded link"


def test_custom_embedded_link_parser():
    """Test that json parser use custom parser to parse an embedded link.

    1. Create a sub-class of JSONParser with redefined create_embedded_link_parser factory.
    2. Create json parser from the sub-class.
    3. Parse an embedded link.
    4. Check that custom parser is used to parse an embedded link.
    """
    class _CustomEmbeddedLinkParser(JSONParser):
        create_embedded_link_parser = _CustomParser("Custom parsed embedded link")

    parsed_link = _CustomEmbeddedLinkParser().parse_embedded_link({})
    assert parsed_link == "Custom parsed embedded link", "Wrong embedded link"


def test_invalid_embedded_link():
    """Test that error is propagated from embedded link parser to json parser.

    1. Create json parser.
    2. Try to parse an embedded link from invalid data.
    3. Check that error is raised.
    4. Check that error is the same as one that embedded link parser raises.
    """
    invalid_link_data = object()
    parser = JSONParser()
    with pytest.raises(ValueError) as actual_error_info:
        parser.parse_embedded_link(invalid_link_data)

    with pytest.raises(ValueError) as expected_error_info:
        parser.create_embedded_link_parser(invalid_link_data).parse()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )


def test_default_embedded_representation(monkeypatch):
    """Test that json parser use EmbeddedRepresentationParser to parse a representation.

    1. Create json parser.
    2. Replace parse method of EmbeddedRepresentationParser so that it returns fake data.
    3. Parse an embedded representation.
    4. Check that returned embedded representation is the same as the one from the mocked method.
    """
    monkeypatch.setattr(
        EmbeddedRepresentationParser,
        "parse",
        lambda self: "Parsed embedded representation",
        )

    parsed_representation = JSONParser().parse_embedded_representation({})
    assert parsed_representation == "Parsed embedded representation", (
        "Wrong embedded representation"
        )


def test_custom_embedded_representation_parser():
    """Test that json parser use custom parser to parse an embedded representation.

    1. Create a sub-class of JSONParser with redefined create_embedded_representation_parser
       factory.
    2. Create json parser from the sub-class.
    3. Parse an embedded representation.
    4. Check that custom parser is used to parse an embedded representation.
    """
    class _CustomEmbeddedRepresentationParser(JSONParser):
        create_embedded_representation_parser = _CustomParser(
            "Custom parsed embedded representation",
            )

    parser = _CustomEmbeddedRepresentationParser()
    parsed_representation = parser.parse_embedded_representation({})
    assert parsed_representation == "Custom parsed embedded representation", (
        "Wrong embedded representation"
        )


def test_invalid_embedded_representation():
    """Test that error is propagated from embedded representation parser to json parser.

    1. Create json parser.
    2. Try to parse an embedded representation from invalid data.
    3. Check that error is raised.
    4. Check that error is the same as one that embedded representation parser raises.
    """
    invalid_representation_data = object()
    parser = JSONParser()
    with pytest.raises(ValueError) as actual_error_info:
        parser.parse_embedded_representation(invalid_representation_data)

    with pytest.raises(ValueError) as expected_error_info:
        parser.create_embedded_representation_parser(invalid_representation_data).parse()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )


def test_default_entity(monkeypatch):
    """Test that json parser use EntityParser to parse an entity.

    1. Create json parser.
    2. Replace parse method of EntityParser so that it returns fake data.
    3. Parse an entity.
    4. Check that returned entity is the same as the one from the mocked method.
    """
    monkeypatch.setattr(EntityParser, "parse", lambda self: "Parsed entity")

    parsed_entity = JSONParser().parse_entity({})
    assert parsed_entity == "Parsed entity", "Wrong entity"


def test_custom_entity_parser():
    """Test that json parser use custom parser to parse an entity.

    1. Create a sub-class of JSONParser with redefined create_entity_parser factory.
    2. Create json parser from the sub-class.
    3. Parse an entity.
    4. Check that custom parser is used to parse an entity.
    """
    class _CustomEntityParser(JSONParser):
        create_entity_parser = _CustomParser("Custom parsed entity")

    parsed_entity = _CustomEntityParser().parse_entity({})
    assert parsed_entity == "Custom parsed entity", "Wrong entity"


def test_invalid_entity():
    """Test that error is propagated from entity parser to json parser.

    1. Create json parser.
    2. Try to parse an entity from invalid data.
    3. Check that error is raised.
    4. Check that error is the same as one that entity parser raises.
    """
    invalid_entity_data = object()
    parser = JSONParser()
    with pytest.raises(ValueError) as actual_error_info:
        parser.parse_entity(invalid_entity_data)

    with pytest.raises(ValueError) as expected_error_info:
        parser.create_entity_parser(invalid_entity_data).parse()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )
