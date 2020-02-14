"""Module with JSON parser for Siren objects."""

import logging
import json

from lila.core.field import InputType, Field
from lila.core.action import Method, Action
from lila.core.link import Link, EmbeddedLink
from lila.core.entity import Entity, EmbeddedRepresentation
from lila.serialization.parser import Parser


class JSONParser(Parser):
    """Class to parse Siren objects from JSON."""

    def parse_field(self, data):
        """Parse serialized Siren field.

        :param data: serialized field.
        :returns: :class:`Field <lila.core.field.Field>`.
        :raises: :class:ValueError.
        """
        data = _ensure_json(data)

        logger = logging.getLogger(__name__)
        logger.debug("Try to parse a field from '%s'", data)

        try:
            name = data["name"]
        except KeyError:
            logger.error("Failed to parse a field: data do not have required 'name' key")
            raise ValueError("Field data do not have required 'name' key")

        classes = data.get("class", ())

        input_type_value = str(data.get("type", InputType.TEXT.value))
        try:
            input_type = InputType(input_type_value)
        except ValueError:
            logger.error("Failed to parse a field: unsupported input type is specified")
            raise ValueError("Unsupported input type is specified")

        value = data.get("value", None)
        title = data.get("title", None)

        try:
            field = Field(
                name=name,
                classes=classes,
                input_type=input_type,
                value=value,
                title=title,
                )
        except ValueError:
            logger.error("Failed to create a field with the provided data")
            raise

        logger.info("Successfully parsed a field")
        return field

    def parse_action(self, data):
        """Parse serialized Siren action.

        :param data: serialized action.
        :returns: :class:`Action <lila.core.action.Action>`.
        :raises: :class:ValueError.
        """
        data = _ensure_json(data)

        logger = logging.getLogger(__name__)
        logger.debug("Try to parse an action from '%s'", data)

        try:
            name = data["name"]
        except KeyError:
            logger.error("Failed to parse an action: data do not have required 'name' key")
            raise ValueError("Action data do not have required 'name' key")

        classes = data.get("class", ())

        method_value = data.get("method", Method.GET.value)
        try:
            method = next(
                action_method for action_method in Method if action_method.value == method_value
                )
        except StopIteration:
            logger.error("Failed to parse an action: unsupported method is specified")
            raise ValueError("Unsupported method is specified")

        try:
            target = data["href"]
        except KeyError:
            logger.error("Failed to parse an action: data do not have required 'href' key")
            raise ValueError("Action data do not have required 'href' key")

        title = data.get("title", None)
        encoding_type = data.get("type", None)

        fields_data = data.get("fields", ())
        try:
            fields = [self.parse_field(field_data) for field_data in fields_data]
        except (TypeError, ValueError) as error:
            logger.error("Failed to parse an action: failed to parse fields")
            raise ValueError("Failed to parse action fields") from error

        try:
            action = Action(
                name=name,
                classes=classes,
                method=method,
                target=target,
                title=title,
                encoding_type=encoding_type,
                fields=fields,
                )
        except ValueError:
            logger.error("Failed to create an action with the provided data")
            raise

        logger.info("Successfully parsed an action")
        return action

    def parse_link(self, data):
        """Parse serialized Siren link.

        :param data: serialized link.
        :returns: :class:`Link <lila.core.link.Link>`.
        :raises: :class:ValueError.
        """
        data = _ensure_json(data)

        logger = logging.getLogger(__name__)
        logger.debug("Try to parse a link from '%s'", data)

        try:
            relations = data["rel"]
        except KeyError:
            logger.error("Failed to parse a link: data do not have required 'rel' key")
            raise ValueError("Link data do not have required 'rel' key")

        classes = data.get("class", ())

        try:
            target = data["href"]
        except KeyError:
            logger.error("Failed to parse a link: data do not have required 'href' key")
            raise ValueError("Link data do not have required 'href' key")

        title = data.get("title", None)
        target_media_type = data.get("type", None)

        try:
            link = Link(
                relations=relations,
                classes=classes,
                target=target,
                title=title,
                target_media_type=target_media_type,
                )
        except ValueError:
            logger.error("Failed to create a link with the provided data")
            raise

        logger.info("Successfully parsed a link")
        return link

    def parse_embedded_link(self, data):
        """Parse serialized embedded Siren link.

        :param data: serialized embedded link.
        :returns: :class:`EmbeddedLink <lila.core.link.EmbeddedLink>`.
        :raises: :class:ValueError.
        """
        data = _ensure_json(data)

        logger = logging.getLogger(__name__)
        logger.debug("Try to parse an embedded link from '%s'", data)

        try:
            relations = data["rel"]
        except KeyError:
            logger.error("Failed to parse an embedded link: data do not have required 'rel' key")
            raise ValueError("Embedded link data do not have required 'rel' key")

        classes = data.get("class", ())

        try:
            target = data["href"]
        except KeyError:
            logger.error("Failed to parse an embedded link: data do not have required 'href' key")
            raise ValueError("Embedded link data do not have required 'href' key")

        title = data.get("title", None)
        target_media_type = data.get("type", None)

        try:
            embedded_link = EmbeddedLink(
                relations=relations,
                classes=classes,
                target=target,
                title=title,
                target_media_type=target_media_type,
                )
        except ValueError:
            logger.error("Failed to create an embedded link with the provided data")
            raise

        logger.info("Successfully parsed an embedded link")
        return embedded_link

    def parse_entity(self, data):
        """Parse serialized Siren entity.

        :param data: serialized entity.
        :returns: :class:`Entity <lila.core.entity.Entity>`.
        :raises: :class:ValueError.
        """
        data = _ensure_json(data)

        logger = logging.getLogger(__name__)
        logger.debug("Try to parse an entity from '%s'", data)

        classes = data.get("class", ())
        properties = data.get("properties", {})

        sub_entities_data = data.get("entities", ())
        try:
            sub_entities = [
                self._parse_sub_entity(sub_entity_data) for sub_entity_data in sub_entities_data
                ]
        except (TypeError, ValueError) as error:
            logger.error("Failed to parse an entity: failed to parse sub entities")
            raise ValueError("Failed to parse sub entities of entity") from error

        links_data = data.get("links", ())
        try:
            links = [self.parse_link(link_data) for link_data in links_data]
        except (TypeError, ValueError) as error:
            logger.error("Failed to parse an entity: failed to parse links")
            raise ValueError("Failed to parse entity links") from error

        actions_data = data.get("actions", ())
        try:
            actions = [self.parse_action(action_data) for action_data in actions_data]
        except (TypeError, ValueError) as error:
            logger.error("Failed to parse an entity: failed to parse actions")
            raise ValueError("Failed to parse entity actions") from error

        title = data.get("title", None)

        try:
            entity = Entity(
                classes=classes,
                properties=properties,
                entities=sub_entities,
                links=links,
                actions=actions,
                title=title,
                )
        except ValueError:
            logger.error("Failed to create an entity with the provided data")
            raise

        logger.info("Successfully parsed an entity")
        return entity

    def parse_embedded_representation(self, data):
        """Parse serialized Siren embedded representation.

        :param data: serialized embedded representation.
        :returns: :class:`Entity <lila.core.entity.EmbeddedRepresentation>`.
        :raises: :class:ValueError.
        """
        data = _ensure_json(data)

        logger = logging.getLogger(__name__)
        logger.debug("Try to parse an embedded representation from '%s'", data)

        classes = data.get("class", ())
        properties = data.get("properties", {})

        try:
            relations = data["rel"]
        except KeyError:
            logger.error(
                "Failed to parse an embedded representation: data do not have required 'rel' key",
                )
            raise ValueError("Embedded representation data do not have required 'rel' key")

        sub_entities_data = data.get("entities", ())
        try:
            sub_entities = [
                self._parse_sub_entity(sub_entity_data) for sub_entity_data in sub_entities_data
                ]
        except (TypeError, ValueError) as error:
            logger.error("Failed to parse an embedded representation: failed to parse sub entities")
            raise ValueError("Failed to parse sub entities of embedded representation") from error

        links_data = data.get("links", ())
        try:
            links = [self.parse_link(link_data) for link_data in links_data]
        except (TypeError, ValueError) as error:
            logger.error("Failed to parse an embedded representation: failed to parse links")
            raise ValueError("Failed to parse links of embedded representation") from error

        actions_data = data.get("actions", ())
        try:
            actions = [self.parse_action(action_data) for action_data in actions_data]
        except (TypeError, ValueError) as error:
            logger.error("Failed to parse an embedded representation: failed to parse actions")
            raise ValueError("Failed to parse actions of embedded representation") from error

        title = data.get("title", None)

        try:
            embedded_representation = EmbeddedRepresentation(
                relations=relations,
                classes=classes,
                properties=properties,
                entities=sub_entities,
                links=links,
                actions=actions,
                title=title,
                )
        except ValueError:
            logger.error("Failed to create an embedded representation with the provided data")
            raise

        logger.info("Successfully parsed an entity")
        return embedded_representation

    def _parse_sub_entity(self, data):
        """Parse serialized sub entity.

        :param data: serialized sub entity.
        :returns: depending on the data either
            :class:`Entity <lila.core.entity.EmbeddedRepresentation>`
            or
            :class:`EmbeddedLink <lila.core.link.EmbeddedLink>`.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to parse sub entity")
        try:
            data["href"]
        except KeyError:
            logger.debug("Parse sub entity as an embedded representation")
            sub_entity = self.parse_embedded_representation(data=data)
        except TypeError as error:
            logger.error("Failed to parse sub entity: sub entity data are not a dictionary")
            raise ValueError("Sub entity data are not a dictionary") from error
        else:
            logger.debug("Parse sub entity as an embedded link")
            sub_entity = self.parse_embedded_link(data=data)

        logger.debug("Successfully parsed sub entity")
        return sub_entity


def _ensure_json(data):
    """Convert data into JSON object (dictionary or list).

    :param data: data to convert.
    :returns: JSON object.
    """
    logger = logging.getLogger(__name__)
    logger.debug("Ensure that data are a valid JSON object")
    try:
        adjusted_data = json.loads(json.dumps(data))
    except TypeError as error:
        logger.error("Specified data are not a valid JSON object")
        raise ValueError("Specified data are not a valid JSON object") from error

    logger.debug("Ensured that data are a valid JSON object")
    return adjusted_data
