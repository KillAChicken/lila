"""Module with JSON marshaler for Siren objects."""

import logging

from lila.serialization.marshaler import Marshaler
from lila.serialization.json.field import FieldMarshaler
from lila.serialization.json.action import ActionMarshaler
from lila.serialization.json.link import LinkMarshaler, EmbeddedLinkMarshaler
from lila.serialization.json.entity import EntityMarshaler, EmbeddedRepresentationMarshaler


class JSONMarshaler(Marshaler):
    """Class to marshal Siren objects into JSON."""

    create_field_marshaler = FieldMarshaler
    create_link_marshaler = LinkMarshaler
    create_embedded_link_marshaler = EmbeddedLinkMarshaler

    def create_action_marshaler(self, action):
        """Factory method to create a marshaler for an action.

        :param action: Siren action to marshal.
        :returns: :class:`ActionMarshaler <lila.serialization.json.action.ActionMarshaler>`.
        """
        return ActionMarshaler(action=action, marshaler=self)

    def create_entity_marshaler(self, entity):
        """Factory method to create a marshaler for an entity.

        :param entity: Siren entity to marshal.
        :returns: :class:`EntityMarshaler <lila.serialization.json.entity.EntityMarshaler>`.
        """
        return EntityMarshaler(entity=entity, marshaler=self)

    def create_embedded_representation_marshaler(self, embedded_representation):
        """Factory method to create a marshaler for an embedded representation.

        :param embedded_representation: Siren embedded representation to marshal.
        :returns: :class:`EmbeddedRepresentationMarshaler
            <lila.serialization.json.entity.EmbeddedRepresentationMarshaler>`.
        """
        return EmbeddedRepresentationMarshaler(
            embedded_representation=embedded_representation,
            marshaler=self,
            )

    def marshal_field(self, field):
        """Marshal Siren field.

        :param field: Siren Field.
        :returns: dictionary with field data.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marshal a field '%s'", field)

        marshaler = self.create_field_marshaler(field)
        try:
            marshaled_field = marshaler.marshal()
        except Exception:
            logger.error("Failed to marshal a field")
            raise

        logger.info("Successfully marshaled a field")
        return marshaled_field

    def marshal_action(self, action):
        """Marshal Siren action.

        :param action: Siren Action.
        :returns: dictionary with action data.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marshal an action '%s'", action)

        marshaler = self.create_action_marshaler(action)
        try:
            marshaled_action = marshaler.marshal()
        except Exception:
            logger.error("Failed to marshal an action")
            raise

        logger.info("Successfully marshaled an action")
        return marshaled_action

    def marshal_link(self, link):
        """Marshal Siren link.

        :param link: Siren Link.
        :returns: dictionary with link data.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marshal a link '%s'", link)

        marshaler = self.create_link_marshaler(link)
        try:
            marshaled_link = marshaler.marshal()
        except Exception:
            logger.error("Failed to marshal a link")
            raise

        logger.info("Successfully marshaled a link")
        return marshaled_link

    def marshal_embedded_link(self, embedded_link):
        """Marshal embedded Siren link.

        :param embedded_link: embedded Siren Link.
        :returns: dictionary with embedded link data.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marshal an embedded link '%s'", embedded_link)

        marshaler = self.create_embedded_link_marshaler(embedded_link)
        try:
            marshaled_link = marshaler.marshal()
        except Exception:
            logger.error("Failed to marshal an embedded link")
            raise

        logger.info("Successfully marshaled an embedded link")
        return marshaled_link

    def marshal_embedded_representation(self, embedded_representation):
        """Marshal Siren embedded representation.

        :param embedded_representation: Siren embedded representation.
        :returns: dictionary with embedded representation data.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marshal an embedded representation '%s'", embedded_representation)

        marshaler = self.create_embedded_representation_marshaler(embedded_representation)
        try:
            marshaled_representation = marshaler.marshal()
        except Exception:
            logger.error("Failed to marshal an embedded representation")
            raise

        logger.info("Successfully marshaled an embedded representation")
        return marshaled_representation

    def marshal_entity(self, entity):
        """Marshal Siren entity.

        :param entity: Siren entity.
        :returns: dictionary with entity data.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marshal an entity '%s'", entity)

        marshaler = self.create_entity_marshaler(entity)
        try:
            marshaled_entity = marshaler.marshal()
        except Exception:
            logger.error("Failed to marshal an entity")
            raise

        logger.info("Successfully marshaled an entity")
        return marshaled_entity
