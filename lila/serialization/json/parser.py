"""Module with JSON parser for Siren objects."""

import logging

from lila.serialization.parser import Parser
from lila.serialization.json.field import FieldParser
from lila.serialization.json.action import ActionParser
from lila.serialization.json.link import LinkParser, EmbeddedLinkParser
from lila.serialization.json.entity import EntityParser, EmbeddedRepresentationParser


class JSONParser(Parser):
    """Class to parse Siren objects from JSON."""

    create_field_parser = FieldParser
    create_link_parser = LinkParser
    create_embedded_link_parser = EmbeddedLinkParser

    def create_action_parser(self, data):
        """Factory method to create a parser for an action.

        :param data: action data to parse.
        :returns: :class:`ActionParser <lila.serialization.json.action.ActionParser>`.
        """
        return ActionParser(data=data, parser=self)

    def create_entity_parser(self, data):
        """Factory method to create a parser for an entity.

        :param data: entity data to parse.
        :returns: :class:`EntityParser <lila.serialization.json.entity.EntityParser>`.
        """
        return EntityParser(data=data, parser=self)

    def create_embedded_representation_parser(self, data):
        """Factory method to create a parser for an embedded representation.

        :param data: data of embedded representation to parse.
        :returns: :class:`EmbeddedRepresentationParser
            <lila.serialization.json.entity.EmbeddedRepresentationParser>`.
        """
        return EmbeddedRepresentationParser(data=data, parser=self)

    def parse_field(self, data):
        """Parse serialized Siren field.

        :param data: serialized field.
        :returns: parsed field.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to parse a field from data '%s'", data)

        parser = self.create_field_parser(data)
        try:
            parsed_field = parser.parse()
        except Exception:
            logger.error("Failed to parse a field")
            raise

        logger.info("Successfully parsed a field")
        return parsed_field

    def parse_action(self, data):
        """Parse serialized Siren action.

        :param data: serialized action.
        :returns: parsed action.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to parse an action from data '%s'", data)

        parser = self.create_action_parser(data)
        try:
            parsed_action = parser.parse()
        except Exception:
            logger.error("Failed to parse an action")
            raise

        logger.info("Successfully parsed an action")
        return parsed_action

    def parse_link(self, data):
        """Parse serialized Siren link.

        :param data: serialized link.
        :returns: parsed link.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to parse a link from data '%s'", data)

        parser = self.create_link_parser(data)
        try:
            parsed_link = parser.parse()
        except Exception:
            logger.error("Failed to parse a link")
            raise

        logger.info("Successfully parsed a link")
        return parsed_link

    def parse_embedded_link(self, data):
        """Parse serialized Siren embedded link.

        :param data: serialized embedded link.
        :returns: parsed embedded link.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to parse an embedded link from data '%s'", data)

        parser = self.create_embedded_link_parser(data)
        try:
            parsed_embedded_link = parser.parse()
        except Exception:
            logger.error("Failed to parse an embedded link")
            raise

        logger.info("Successfully parsed an embedded link")
        return parsed_embedded_link

    def parse_embedded_representation(self, data):
        """Parse serialized Siren embedded representation.

        :param data: serialized embedded representation.
        :returns: parsed embedded representation.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to parse an embedded representation from data '%s'", data)

        parser = self.create_embedded_representation_parser(data)
        try:
            parsed_representation = parser.parse()
        except Exception:
            logger.error("Failed to parse an embedded representation")
            raise

        logger.info("Successfully parsed an embedded representation")
        return parsed_representation

    def parse_entity(self, data):
        """Parse serialized Siren entity.

        :param data: serialized entity.
        :returns: parsed entity.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to parse an entity from data '%s'", data)

        parser = self.create_entity_parser(data)
        try:
            parsed_entity = parser.parse()
        except Exception:
            logger.error("Failed to parse an entity")
            raise

        logger.info("Successfully parsed an entity")
        return parsed_entity
