"""Configuration file for pytest."""

import pytest

from lila.core.field import InputType
from lila.core.link import EmbeddedLink


@pytest.fixture
def json_data_factory():
    """Factory to create valid data for Siren objects."""
    return _DataFactory()


class _DataFactory:
    """Class to generate valid data for Sired objects."""

    def create_field_data(
            self,
            name="name",
            classes=(),
            input_type=InputType.TEXT,
            value=None,
            title=None,
        ):
        # pylint: disable=no-self-use, too-many-arguments
        """Create valid field data.

        :param name: name of the field.
        :param classes: iterable with classes of the field.
        :param input_type: item from :class:InputType enumerable.
        :param value: value of the field.
        :param title: title of the field.
        :returns: dictionary with serialized field data.
        """
        return {
            "name": name,
            "class": list(classes),
            "type": input_type.value,
            "value": value,
            "title": title,
            }

    def create_action_data(
            self,
            name="name",
            classes=(),
            method="GET",
            target="/action",
            title=None,
            encoding_type=None,
            fields=(),
        ):
        # pylint: disable=too-many-arguments
        """Create valid action data.

        :param name: name of the action.
        :param classes: iterable with classes of the action.
        :param method: method of the action.
        :param target: target of the action.
        :param title: title of the action.
        :param encoding_type: encoding type of the action.
        :param fields: iterable with :class:Fields of the action.
        :returns: dictionary with serialized action data.
        """
        fields_data = []
        for field in fields:
            field_data = self.create_field_data(
                name=field.name,
                classes=field.classes,
                input_type=field.input_type,
                value=field.value,
                title=field.title,
                )
            fields_data.append(field_data)

        return {
            "name": name,
            "class": list(classes),
            "method": method,
            "href": target,
            "title": title,
            "type": encoding_type,
            "fields": fields_data,
            }

    def create_link_data(
            self,
            relations=(),
            classes=(),
            target="/link",
            title=None,
            target_media_type=None,
        ):
        # pylint: disable=no-self-use, too-many-arguments
        """Create valid link data.

        :param relations: iterable with relations of the link.
        :param classes: iterable with classes of the link.
        :param target: target of the link.
        :param title: title of the link.
        :param target_media_type: media type of the linked resource.
        :returns: dictionary with serialized link data.
        """
        return {
            "rel": list(relations),
            "class": list(classes),
            "href": target,
            "title": title,
            "type": target_media_type,
            }

    def create_embedded_link_data(
            self,
            relations=("self", ),
            classes=(),
            target="/link",
            title=None,
            target_media_type=None,
        ):
        # pylint: disable=no-self-use, too-many-arguments
        """Create valid embedded link data.

        :param relations: iterable with relations of the embedded link.
        :param classes: iterable with classes of the embedded link.
        :param target: target of the embedded link.
        :param title: title of the embedded link.
        :param target_media_type: media type of the linked resource.
        :returns: dictionary with serialized embedded link data.
        """
        return {
            "rel": list(relations),
            "class": list(classes),
            "href": target,
            "title": title,
            "type": target_media_type,
            }

    def create_embedded_representation_data(
            self,
            classes=(),
            properties=(),
            relations=("self", ),
            entities=(),
            links=(),
            actions=(),
            title=None,
        ):
        # pylint: disable=too-many-arguments
        """Create valid embedded representation data.

        :param classes: iterable with classes of the embedded representation.
        :param properties: properties of the embedded representation.
        :param relations: iterable with relations of the embedded representation.
        :param entities: iterable with sub entities of the embedded representation.
        :param links: iterable with :class:Link of the embedded representation.
        :param actions: iterable with :class:Action of the embedded representation.
        :param title: title of the embedded representation.
        :returns: dictionary with serialized embedded representation data.
        """
        return {
            "class": list(classes),
            "properties": properties,
            "rel": list(relations),
            "entities": [self._create_subentity_data(sub_entity) for sub_entity in entities],
            "links": [self._create_link_data(link) for link in links],
            "actions": [self._create_action_data(action) for action in actions],
            "title": title,
            }

    def create_entity_data(
            self,
            classes=(),
            properties=(),
            entities=(),
            links=(),
            actions=(),
            title=None,
        ):
        # pylint: disable=too-many-arguments
        """Create valid entity data.

        :param classes: iterable with classes of the entity.
        :param properties: properties of the entity.
        :param entities: iterable with sub entities of the entity.
        :param links: iterable with :class:Link of the entity.
        :param actions: iterable with :class:Action of the entity.
        :param title: title of the entity.
        :returns: dictionary with serialized entity data.
        """
        return {
            "class": list(classes),
            "properties": properties,
            "entities": [self._create_subentity_data(sub_entity) for sub_entity in entities],
            "links": [self._create_link_data(link) for link in links],
            "actions": [self._create_action_data(action) for action in actions],
            "title": title,
            }

    def _create_link_data(self, link):
        """Create link data from a link object.

        :param link: :class:Link.
        :returns: dictionary with serialized link.
        """
        return self.create_link_data(
            relations=link.relations,
            classes=link.classes,
            target=link.target,
            title=link.title,
            target_media_type=link.target_media_type,
            )

    def _create_action_data(self, action):
        """Create action data from an action object.

        :param action: :class:Action.
        :returns: dictionary with serialized action.
        """
        return self.create_action_data(
            name=action.name,
            classes=action.classes,
            method=action.method,
            target=action.target,
            title=action.title,
            encoding_type=action.encoding_type,
            fields=action.fields,
            )

    def _create_subentity_data(self, sub_entity):
        """Create sub entity data from a sub entity.

        :param sub_entity: sub entity object (:class:EmbeddedLink or :class:EmbeddedRepresentation).
        :returns: dictionary with serialized sub entity.
        """
        if isinstance(sub_entity, EmbeddedLink):
            sub_entity_data = self.create_embedded_link_data(
                relations=sub_entity.relations,
                classes=sub_entity.classes,
                target=sub_entity.target,
                title=sub_entity.title,
                target_media_type=sub_entity.target_media_type,
                )
        else:
            sub_entity_data = self.create_embedded_representation_data(
                classes=sub_entity.classes,
                properties=sub_entity.properties,
                relations=sub_entity.relations,
                links=sub_entity.links,
                actions=sub_entity.actions,
                title=sub_entity.title,
                )

        return sub_entity_data
