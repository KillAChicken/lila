"""Pytest configuration file."""

import json

import pytest


class _ComponentValidator:
    """Class to validate Siren components."""

    @staticmethod
    def validate_field(field, expected_field):
        """Validate a field.

        :param field: field to validate.
        :param expected_field: field with expected attributes.
        :raises: :exception:AssertionError if fields are different.
        """
        assert field.name == expected_field.name, "Wrong name of the field"
        assert field.classes == expected_field.classes, "Wrong classes of the field"
        assert field.input_type == expected_field.input_type, "Wrong input type of the field"
        assert field.value == expected_field.value, "Wrong value of the field"
        assert field.title == expected_field.title, "Wrong title of the field"

    def validate_action(self, action, expected_action):
        """Validate an action.

        :param action: action to validate.
        :param expected_action: action with expected attributes.
        :raises: :exception:AssertionError if actions are different.
        """
        assert action.name == expected_action.name, "Wrong name of the action"
        assert action.classes == expected_action.classes, "Wrong classes of the action"
        assert action.method == expected_action.method, "Wrong method of the action"
        assert action.target == expected_action.target, "Wrong target of the action"
        assert action.title == expected_action.title, "Wrong title of the action"
        assert action.encoding_type == expected_action.encoding_type, (
            "Wrong encoding type of the action"
            )

        fields = action.fields
        expected_fields = expected_action.fields

        assert len(fields) == len(expected_fields), "Wrong number of fields of the action"

        for field, expected_field in zip(fields, expected_fields):
            self.validate_field(field, expected_field)

    @staticmethod
    def validate_link(link, expected_link):
        """Validate a link.

        :param link: link to validate.
        :param expected_link: link with expected attributes.
        :raises: :exception:AssertionError if links are different.
        """
        assert link.relations == expected_link.relations, "Wrong relations of the link"
        assert link.classes == expected_link.classes, "Wrong classes of the link"
        assert link.title == expected_link.title, "Wrong title of the link"
        assert link.target == expected_link.target, "Wrong target of the link"
        assert link.target_media_type == expected_link.target_media_type, (
            "Wrong target media type of the link"
            )

    @staticmethod
    def validate_embedded_link(embedded_link, expected_embedded_link):
        """Validate an embedded link.

        :param embedded_link: embedded link to validate.
        :param expected_embedded_link: embedded link with expected attributes.
        :raises: :exception:AssertionError if embedded links are different.
        """
        assert embedded_link.relations == expected_embedded_link.relations, (
            "Wrong relations of the embedded link"
            )
        assert embedded_link.classes == expected_embedded_link.classes, (
            "Wrong classes of the embedded link"
            )
        assert embedded_link.title == expected_embedded_link.title, (
            "Wrong title of the embedded link"
            )
        assert embedded_link.target == expected_embedded_link.target, (
            "Wrong target of the embedded link"
            )
        assert embedded_link.target_media_type == expected_embedded_link.target_media_type, (
            "Wrong target media type of the embedded link"
            )

    def validate_entity(self, entity, expected_entity):
        # pylint: disable=too-many-locals
        """Validate an entity.

        :param entity: entity to validate.
        :param expected_entity: entity with expected attributes.
        :raises: :exception:AssertionError if entities are different.
        """
        assert entity.classes == expected_entity.classes, "Wrong classes of the entity"
        assert entity.title == expected_entity.title, "Wrong title of the entity"

        json_properties = json.dumps(entity.properties, sort_keys=True)
        expected_json_properties = json.dumps(expected_entity.properties, sort_keys=True)
        assert json_properties == expected_json_properties, "Wrong properties of the entity"

        links = entity.links
        expected_links = expected_entity.links

        assert len(links) == len(expected_links), "Wrong number of links of the entity"

        for link, expected_link in zip(links, expected_links):
            self.validate_link(link, expected_link)

        actions = entity.actions
        expected_actions = expected_entity.actions

        assert len(actions) == len(expected_actions), "Wrong number of actions of the entity"

        for action, expected_action in zip(actions, expected_actions):
            self.validate_action(action, expected_action)

        sub_entities = entity.entities
        expected_sub_entities = expected_entity.entities

        assert len(sub_entities) == len(expected_sub_entities), (
            "Wrong number of sub-entities of the entity"
            )

        for sub_entity, expected_sub_entities in zip(sub_entities, expected_sub_entities):
            self._validate_sub_entity(sub_entity, expected_sub_entities)


    def validate_embedded_representation(
            self, embedded_representation, expected_embedded_representation,
        ):
        # pylint: disable=too-many-locals
        """Validate an embedded representation.

        :param embedded_representation: embedded representation to validate.
        :param expected_embedded_representation: embedded representation with expected attributes.
        :raises: :exception:AssertionError if embedded representations are different.
        """
        assert embedded_representation.relations == expected_embedded_representation.relations, (
            "Wrong relations of the embedded representation"
            )
        assert embedded_representation.classes == expected_embedded_representation.classes, (
            "Wrong classes of the embedded representation"
            )
        assert embedded_representation.title == expected_embedded_representation.title, (
            "Wrong title of the embedded representation"
            )

        json_properties = json.dumps(embedded_representation.properties, sort_keys=True)
        expected_json_properties = json.dumps(
            expected_embedded_representation.properties,
            sort_keys=True,
            )
        assert json_properties == expected_json_properties, (
            "Wrong properties of the embedded representation"
            )

        links = embedded_representation.links
        expected_links = expected_embedded_representation.links

        assert len(links) == len(expected_links), (
            "Wrong number of links of the embedded representation"
            )

        for link, expected_link in zip(links, expected_links):
            self.validate_link(link, expected_link)

        actions = embedded_representation.actions
        expected_actions = expected_embedded_representation.actions

        assert len(actions) == len(expected_actions), (
            "Wrong number of actions of the embedded representation"
            )

        for action, expected_action in zip(actions, expected_actions):
            self.validate_action(action, expected_action)

        sub_entities = embedded_representation.entities
        expected_sub_entities = expected_embedded_representation.entities

        assert len(sub_entities) == len(expected_sub_entities), (
            "Wrong number of sub-entities of the embedded representation"
            )

        for sub_entity, expected_sub_entities in zip(sub_entities, expected_sub_entities):
            self._validate_sub_entity(sub_entity, expected_sub_entities)

    def _validate_sub_entity(self, sub_entity, expected_sub_entity):
        """Validate a sub-entity.

        :param sub_entity: embedded link or representation to validate.
        :param expected_sub_entity: siren component of the same type as sub_entity with
            expected attributes.
        :raises: :exception:AssertionError if sub-entities are different.
        """
        assert type(sub_entity) is type(expected_sub_entity), "Sub-entities have different types"
        if hasattr(sub_entity, "target"):
            self.validate_embedded_link(sub_entity, expected_sub_entity)
        else:
            self.validate_embedded_representation(sub_entity, expected_sub_entity)


@pytest.fixture(scope="session")
def component_validator():
    """Validator of Siren components."""
    return _ComponentValidator()
