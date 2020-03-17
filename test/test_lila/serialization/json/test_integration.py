"""Test cases to check that JSON marshaler and parser can be integrated with each other."""

import random

from lila.core.field import Field, InputType
from lila.core.action import Action, Method
from lila.core.link import Link, EmbeddedLink
from lila.core.entity import Entity, EmbeddedRepresentation
from lila.serialization.json.marshaler import JSONMarshaler
from lila.serialization.json.parser import JSONParser


def test_field(component_validator):
    """Test that field can be marshaled and parsed back.

    1. Create a field.
    2. Create JSON parser and marshaler.
    3. Marshal the field.
    4. Parse the data.
    5. Check that parsed field has the same data as the original one.
    """
    field = Field(
        name="field name",
        classes=("field class 1", "field class 2"),
        input_type=random.choice(list(InputType)),
        value="field value",
        title="field title",
        )

    field_data = JSONMarshaler().marshal_field(field)
    actual_field = JSONParser().parse_field(field_data)

    component_validator.validate_field(actual_field, field)


def test_action(component_validator):
    """Test that action can be marshaled and parsed back.

    1. Create an action.
    2. Create JSON parser and marshaler.
    3. Marshal the field.
    4. Parse the data.
    5. Check that parsed action has the same data as the original one.
    """
    action = Action(
        name="action name",
        classes=("action class 1", "action class 2"),
        method=random.choice(list(Method)),
        target="/action/target",
        title="action title",
        media_type="application/json",
        fields=(
            Field(name="first"),
            Field(name="second")
            ),
        )

    action_data = JSONMarshaler().marshal_action(action)
    actual_action = JSONParser().parse_action(action_data)

    component_validator.validate_action(actual_action, action)


def test_link(component_validator):
    """Test that link can be marshaled and parsed back.

    1. Create a link.
    2. Create JSON parser and marshaler.
    3. Marshal the link.
    4. Parse the data.
    5. Check that parsed link has the same data as the original one.
    """
    link = Link(
        relations=("link relation 1", "link relation 2"),
        classes=("link class 1", "link class 2"),
        title="link title",
        target="/link/target",
        target_media_type="application/link",
        )

    link_data = JSONMarshaler().marshal_link(link)
    actual_link = JSONParser().parse_link(link_data)

    component_validator.validate_link(actual_link, link)


def test_embedded_link(component_validator):
    """Test that embedded link can be marshaled and parsed back.

    1. Create an embedded link.
    2. Create JSON parser and marshaler.
    3. Marshal the embedded link.
    4. Parse the data.
    5. Check that parsed embedded link has the same data as the original one.
    """
    embedded_link = EmbeddedLink(
        relations=("embedded link relation 1", "embedded link relation 2"),
        classes=("embedded link class 1", "embedded link class 2"),
        title="embedded link title",
        target="/embedded/link/target",
        target_media_type="application/embedded+link",
        )

    embedded_link_data = JSONMarshaler().marshal_embedded_link(embedded_link)
    actual_embedded_link = JSONParser().parse_embedded_link(embedded_link_data)

    component_validator.validate_embedded_link(actual_embedded_link, embedded_link)


def test_entity(component_validator):
    """Test that entity can be marshaled and parsed back.

    1. Create an entity.
    2. Create JSON parser and marshaler.
    3. Marshal the entity.
    4. Parse the data.
    5. Check that parsed entity has the same data as the original one.
    """
    entity = Entity(
        classes=("entity class 1", "entity class 2"),
        properties={"entity property 1": 1, "entity property 2": [1, 2]},
        entities=(
            EmbeddedLink(target="/embedded/link/target", relations=["relation"]),
            EmbeddedRepresentation(relations=["relation"]),
            ),
        links=[Link(target="/link/target", relations=["relation"])],
        actions=[Action(target="/action/target", name="entity action")],
        title="entity title",
        )

    entity_data = JSONMarshaler().marshal_entity(entity)
    actual_entity = JSONParser().parse_entity(entity_data)

    component_validator.validate_entity(actual_entity, entity)


def test_embedded_representation(component_validator):
    """Test that embedded representation can be marshaled and parsed back.

    1. Create an embedded representation.
    2. Create JSON parser and marshaler.
    3. Marshal the embedded representation.
    4. Parse the data.
    5. Check that parsed embedded representation has the same data as the original one.
    """
    representation = EmbeddedRepresentation(
        relations=["representation relation 1", "representation relation 2"],
        classes=("representation class 1", "representation class 2"),
        properties={"representation property 1": 1, "representation property 2": [1, 2]},
        entities=(
            EmbeddedLink(target="/embedded/link/target", relations=["relation"]),
            EmbeddedRepresentation(relations=["relation"]),
            ),
        links=[Link(target="/link/target", relations=["relation"])],
        actions=[Action(target="/action/target", name="representation action")],
        title="representation title",
        )

    representation_data = JSONMarshaler().marshal_embedded_representation(representation)
    actual_representation = JSONParser().parse_embedded_representation(representation_data)

    component_validator.validate_embedded_representation(actual_representation, representation)
