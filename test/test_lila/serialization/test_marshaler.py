"""Test cases for base marshaler."""

import pytest

from lila.core.field import Field
from lila.core.action import Action
from lila.core.link import Link, EmbeddedLink
from lila.core.entity import Entity, EmbeddedRepresentation
from lila.serialization.marshaler import Marshaler


def test_marshal_field():
    """Check that NotImplementedError is raised if marshal_field is called.

    1. Create an instance of Marshaler class.
    2. Try to marshal a field.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    with pytest.raises(NotImplementedError) as error_info:
        Marshaler().marshal_field(field=Field(name="field"))

    assert error_info.value.args[0] == "Marshaler does not support siren fields"


def test_marshal_action():
    """Check that NotImplementedError is raised if marshal_action is called.

    1. Create an instance of Marshaler class.
    2. Try to marshal an action.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    with pytest.raises(NotImplementedError) as error_info:
        Marshaler().marshal_action(action=Action(name="action", target="/action"))

    assert error_info.value.args[0] == "Marshaler does not support siren actions"


def test_marshal_link():
    """Check that NotImplementedError is raised if marshal_link is called.

    1. Create an instance of Marshaler class.
    2. Try to marshal a link.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    with pytest.raises(NotImplementedError) as error_info:
        Marshaler().marshal_link(link=Link(relations=["self"], target="/link"))

    assert error_info.value.args[0] == "Marshaler does not support siren links"


def test_marshal_embedded_link():
    """Check that NotImplementedError is raised if marshal_embedded_link is called.

    1. Create an instance of Marshaler class.
    2. Try to marshal an embedded link.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    link = EmbeddedLink(relations=["self"], target="/embedded/link")

    with pytest.raises(NotImplementedError) as error_info:
        Marshaler().marshal_embedded_link(embedded_link=link)

    assert error_info.value.args[0] == "Marshaler does not support embedded siren links"


def test_marshal_embedded_representation():
    """Check that NotImplementedError is raised if marshal_embedded_representation is called.

    1. Create an instance of Marshaler class.
    2. Try to marshal an embedded representation.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    representation = EmbeddedRepresentation(relations=["self"])

    with pytest.raises(NotImplementedError) as error_info:
        Marshaler().marshal_embedded_representation(embedded_representation=representation)

    assert error_info.value.args[0] == "Marshaler does not support siren embedded representation"


def test_marshal_entity():
    """Check that NotImplementedError is raised if marshal_entity is called.

    1. Create an instance of Marshaler class.
    2. Try to marshal an entity.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    entity = Entity()

    with pytest.raises(NotImplementedError) as error_info:
        Marshaler().marshal_entity(entity=entity)

    assert error_info.value.args[0] == "Marshaler does not support siren entity"
