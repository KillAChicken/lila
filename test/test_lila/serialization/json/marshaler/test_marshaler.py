"""Test cases for JSON marshaler."""

import pytest

from lila.core.field import Field
from lila.core.action import Action
from lila.core.link import Link, EmbeddedLink
from lila.core.entity import Entity, EmbeddedRepresentation
from lila.serialization.json.marshaler import JSONMarshaler
from lila.serialization.json.field import FieldMarshaler
from lila.serialization.json.action import ActionMarshaler
from lila.serialization.json.link import LinkMarshaler, EmbeddedLinkMarshaler
from lila.serialization.json.entity import EntityMarshaler, EmbeddedRepresentationMarshaler


class _CustomMarshaler:
    """Class to be used as custom marshaler factory for Siren components."""

    def __init__(self, data):
        self.__data = data

    def marshal(self):
        """Simple marshal implementation to return predefined data."""
        return self.__data

    def __call__(self, *args, **kwargs):
        return self


def test_default_field_marshaler(monkeypatch):
    """Test that json marshaler use FieldMarshaler to marshal a field.

    1. Create json marshaler.
    2. Replace marshal method of FieldMarshaler so that it returns fake data.
    3. Marshal a field.
    4. Check that returned data are the same as ones from the mocked method.
    """
    monkeypatch.setattr(FieldMarshaler, "marshal", lambda self: "Marshaled field")

    marshaled_field = JSONMarshaler().marshal_field(Field(name="field"))
    assert marshaled_field == "Marshaled field", "Wrong field data"


def test_custom_field_marshaler():
    """Test that json marshaler use custom marshaler to marshal a field.

    1. Create a sub-class of JSONMarshaler with redefined create_field_marshaler factory.
    2. Create json marshaler from the sub-class.
    3. Marshal a field.
    4. Check that custom marshaler is used to marshal a field.
    """
    class _CustomFieldMarshaler(JSONMarshaler):
        create_field_marshaler = _CustomMarshaler("Custom marshaled field")

    marshaled_field = _CustomFieldMarshaler().marshal_field(Field(name="field"))
    assert marshaled_field == "Custom marshaled field", "Wrong field data"


def test_invalid_field():
    """Test that error is propagated from field marshaler to json marshaler.

    1. Create json marshaler.
    2. Try to marshal invalid field.
    3. Check that error is raised.
    4. Check that error is the same as one that field marshaler raises.
    """
    invalid_field = None
    marshaler = JSONMarshaler()
    with pytest.raises(ValueError) as actual_error_info:
        marshaler.marshal_field(invalid_field)

    with pytest.raises(ValueError) as expected_error_info:
        marshaler.create_field_marshaler(invalid_field).marshal()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )


def test_default_action_marshaler(monkeypatch):
    """Test that json marshaler use ActionMarshaler to marshal an action.

    1. Create json marshaler.
    2. Replace marshal method of ActionMarshaler so that it returns fake data.
    3. Marshal an action.
    4. Check that returned data are the same as ones from the mocked method.
    """
    monkeypatch.setattr(ActionMarshaler, "marshal", lambda self: "Marshaled action")

    marshaled_action = JSONMarshaler().marshal_action(
        action=Action(name="action", target="/target"),
        )
    assert marshaled_action == "Marshaled action", "Wrong action data"


def test_custom_action_marshaler():
    """Test that json marshaler use custom marshaler to marshal an action.

    1. Create a sub-class of JSONMarshaler with redefined create_action_marshaler factory.
    2. Create json marshaler from the sub-class.
    3. Marshal an action.
    4. Check that custom marshaler is used to marshal an action.
    """
    class _CustomActionMarshaler(JSONMarshaler):
        create_action_marshaler = _CustomMarshaler("Custom marshaled action")

    marshaled_action = _CustomActionMarshaler().marshal_action(
        action=Action(name="action", target="/target"),
        )
    assert marshaled_action == "Custom marshaled action", "Wrong action data"


def test_invalid_action():
    """Test that error is propagated from action marshaler to json marshaler.

    1. Create json marshaler.
    2. Try to marshal invalid action.
    3. Check that error is raised.
    4. Check that error is the same as one that action marshaler raises.
    """
    invalid_action = None
    marshaler = JSONMarshaler()
    with pytest.raises(ValueError) as actual_error_info:
        marshaler.marshal_action(invalid_action)

    with pytest.raises(ValueError) as expected_error_info:
        marshaler.create_action_marshaler(invalid_action).marshal()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )


def test_default_link_marshaler(monkeypatch):
    """Test that json marshaler use LinkMarshaler to marshal a link.

    1. Create json marshaler.
    2. Replace marshal method of LinkMarshaler so that it returns fake data.
    3. Marshal a link.
    4. Check that returned data are the same as ones from the mocked method.
    """
    monkeypatch.setattr(LinkMarshaler, "marshal", lambda self: "Marshaled link")

    marshaled_link = JSONMarshaler().marshal_link(link=Link(relations=(), target="/target"))
    assert marshaled_link == "Marshaled link", "Wrong link data"


def test_custom_link_marshaler():
    """Test that json marshaler use custom marshaler to marshal a link.

    1. Create a sub-class of JSONMarshaler with redefined create_link_marshaler factory.
    2. Create json marshaler from the sub-class.
    3. Marshal a link.
    4. Check that custom marshaler is used to marshal a link.
    """
    class _CustomLinkMarshaler(JSONMarshaler):
        create_link_marshaler = _CustomMarshaler("Custom marshaled link")

    marshaled_link = _CustomLinkMarshaler().marshal_link(link=Link(relations=(), target="/target"))
    assert marshaled_link == "Custom marshaled link", "Wrong link data"


def test_invalid_link():
    """Test that error is propagated from link marshaler to json marshaler.

    1. Create json marshaler.
    2. Try to marshal invalid link.
    3. Check that error is raised.
    4. Check that error is the same as one that link marshaler raises.
    """
    invalid_link = None
    marshaler = JSONMarshaler()
    with pytest.raises(ValueError) as actual_error_info:
        marshaler.marshal_link(invalid_link)

    with pytest.raises(ValueError) as expected_error_info:
        marshaler.create_link_marshaler(invalid_link).marshal()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )


def test_default_embedded_link_marshaler(monkeypatch):
    """Test that json marshaler use EmbeddedLinkMarshaler to marshal an embedded link.

    1. Create json marshaler.
    2. Replace marshal method of EmbeddedLinkMarshaler so that it returns fake data.
    3. Marshal an embedded link.
    4. Check that returned data are the same as ones from the mocked method.
    """
    monkeypatch.setattr(EmbeddedLinkMarshaler, "marshal", lambda self: "Marshaled embedded link")

    marshaled_link = JSONMarshaler().marshal_embedded_link(
        embedded_link=EmbeddedLink(relations=["self"], target="/target"),
        )
    assert marshaled_link == "Marshaled embedded link", "Wrong data of the embedded link"


def test_custom_embedded_link_marshaler():
    """Test that json marshaler use custom marshaler to marshal an embedded link.

    1. Create a sub-class of JSONMarshaler with redefined create_embedded_link_marshaler factory.
    2. Create json marshaler from the sub-class.
    3. Marshal an embedded link.
    4. Check that custom marshaler is used to marshal an embedded link.
    """
    class _CustomEmbeddedLinkMarshaler(JSONMarshaler):
        create_embedded_link_marshaler = _CustomMarshaler("Custom marshaled embedded link")

    marshaled_link = _CustomEmbeddedLinkMarshaler().marshal_embedded_link(
        embedded_link=EmbeddedLink(relations=["self"], target="/target"),
        )
    assert marshaled_link == "Custom marshaled embedded link", "Wrong data of the embedded link"


def test_invalid_embedded_link():
    """Test that error is propagated from embedded link marshaler to json marshaler.

    1. Create json marshaler.
    2. Try to marshal invalid embedded link.
    3. Check that error is raised.
    4. Check that error is the same as one that embedded link marshaler raises.
    """
    invalid_link = None
    marshaler = JSONMarshaler()
    with pytest.raises(ValueError) as actual_error_info:
        marshaler.marshal_embedded_link(invalid_link)

    with pytest.raises(ValueError) as expected_error_info:
        marshaler.create_embedded_link_marshaler(invalid_link).marshal()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )


def test_default_embedded_representation(monkeypatch):
    """Test that json marshaler use EmbeddedRepresentationMarshaler to marshal a representation.

    1. Create json marshaler.
    2. Replace marshal method of EmbeddedRepresentationMarshaler so that it returns fake data.
    3. Marshal an embedded representation.
    4. Check that returned data are the same as ones from the mocked method.
    """
    monkeypatch.setattr(
        EmbeddedRepresentationMarshaler,
        "marshal",
        lambda self: "Marshaled embedded representation",
        )

    marshaled_representation = JSONMarshaler().marshal_embedded_representation(
        embedded_representation=EmbeddedRepresentation(relations=["self"]),
        )
    assert marshaled_representation == "Marshaled embedded representation", (
        "Wrong data of the embedded representation"
        )


def test_custom_embedded_representation_marshaler():
    """Test that json marshaler use custom marshaler to marshal an embedded representation.

    1. Create a sub-class of JSONMarshaler with redefined create_embedded_representation_marshaler
       factory.
    2. Create json marshaler from the sub-class.
    3. Marshal an embedded representation.
    4. Check that custom marshaler is used to marshal an embedded representation.
    """
    class _CustomEmbeddedRepresentationMarshaler(JSONMarshaler):
        create_embedded_representation_marshaler = _CustomMarshaler(
            "Custom marshaled embedded representation",
            )

    marshaler = _CustomEmbeddedRepresentationMarshaler()
    marshaled_representation = marshaler.marshal_embedded_representation(
        embedded_representation=EmbeddedRepresentation(relations=["self"]),
        )
    assert marshaled_representation == "Custom marshaled embedded representation", (
        "Wrong data of the embedded link"
        )


def test_invalid_embedded_representation():
    """Test that error is propagated from embedded representation marshaler to json marshaler.

    1. Create json marshaler.
    2. Try to marshal invalid embedded representation.
    3. Check that error is raised.
    4. Check that error is the same as one that embedded representation marshaler raises.
    """
    invalid_representation = None
    marshaler = JSONMarshaler()
    with pytest.raises(ValueError) as actual_error_info:
        marshaler.marshal_embedded_representation(invalid_representation)

    with pytest.raises(ValueError) as expected_error_info:
        marshaler.create_embedded_representation_marshaler(invalid_representation).marshal()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )


def test_default_entity(monkeypatch):
    """Test that json marshaler use EntityMarshaler to marshal an entity.

    1. Create json marshaler.
    2. Replace marshal method of EntityMarshaler so that it returns fake data.
    3. Marshal an entity.
    4. Check that returned data are the same as ones from the mocked method.
    """
    monkeypatch.setattr(EntityMarshaler, "marshal", lambda self: "Marshaled entity")

    marshaled_entity = JSONMarshaler().marshal_entity(entity=Entity())
    assert marshaled_entity == "Marshaled entity", "Wrong entity data"


def test_custom_entity_marshaler():
    """Test that json marshaler use custom marshaler to marshal an entity.

    1. Create a sub-class of JSONMarshaler with redefined create_entity_marshaler factory.
    2. Create json marshaler from the sub-class.
    3. Marshal an entity.
    4. Check that custom marshaler is used to marshal an entity.
    """
    class _CustomEntityMarshaler(JSONMarshaler):
        create_entity_marshaler = _CustomMarshaler("Custom marshaled entity")

    marshaled_entity = _CustomEntityMarshaler().marshal_entity(entity=Entity())
    assert marshaled_entity == "Custom marshaled entity", "Wrong entity data"


def test_invalid_entity():
    """Test that error is propagated from entity marshaler to json marshaler.

    1. Create json marshaler.
    2. Try to marshal invalid entity.
    3. Check that error is raised.
    4. Check that error is the same as one that entity marshaler raises.
    """
    invalid_entity = None
    marshaler = JSONMarshaler()
    with pytest.raises(ValueError) as actual_error_info:
        marshaler.marshal_entity(invalid_entity)

    with pytest.raises(ValueError) as expected_error_info:
        marshaler.create_entity_marshaler(invalid_entity).marshal()

    assert actual_error_info.value.args[0] == expected_error_info.value.args[0], (
        "Wrong error is raised"
        )
