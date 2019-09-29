"""Test cases for base parser."""

import pytest

from lila.serialization.parser import Parser


def test_parse_field():
    """Check that NotImplementedError is raised if parse_field is called.

    1. Create an instance of Parser class.
    2. Try to parse a field.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    with pytest.raises(NotImplementedError) as error_info:
        Parser().parse_field(data={})

    assert error_info.value.args[0] == "Parser does not support siren fields"


def test_parse_action():
    """Check that NotImplementedError is raised if parse_action is called.

    1. Create an instance of Parser class.
    2. Try to parse an action.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    with pytest.raises(NotImplementedError) as error_info:
        Parser().parse_action(data={})

    assert error_info.value.args[0] == "Parser does not support siren actions"


def test_parse_link():
    """Check that NotImplementedError is raised if parse_link is called.

    1. Create an instance of Parser class.
    2. Try to parse a link.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    with pytest.raises(NotImplementedError) as error_info:
        Parser().parse_link(data={})

    assert error_info.value.args[0] == "Parser does not support siren links"


def test_parse_embedded_link():
    """Check that NotImplementedError is raised if parse_embedded_link is called.

    1. Create an instance of Parser class.
    2. Try to parse an embedded link.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    with pytest.raises(NotImplementedError) as error_info:
        Parser().parse_embedded_link(data={})

    assert error_info.value.args[0] == "Parser does not support embedded siren links"


def test_parse_entity():
    """Check that NotImplementedError is raised if parse_entity is called.

    1. Create an instance of Parser class.
    2. Try to parse an entity.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    with pytest.raises(NotImplementedError) as error_info:
        Parser().parse_entity(data={})

    assert error_info.value.args[0] == "Parser does not support siren entities"


def test_parse_embedded_representation():
    """Check that NotImplementedError is raised if parse_embedded_representation is called.

    1. Create an instance of Parser class.
    2. Try to parse an embedded representation.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    with pytest.raises(NotImplementedError) as error_info:
        Parser().parse_embedded_representation(data={})

    assert error_info.value.args[0] == "Parser does not support siren embedded representations"
