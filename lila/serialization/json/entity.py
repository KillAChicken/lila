"""Module with default marshaler for an entity."""

import logging
import json

from lila.core.entity import Entity, EmbeddedRepresentation


class EntityMarshaler:
    """Class to marshal a single entity."""

    def __init__(self, entity, marshaler):
        self._entity = entity
        self._marshaler = marshaler

    def marshal(self):
        """Marshal the entity.

        :returns: dictionary with entity data.
        :raises: :class:ValueError.
        """
        return {
            "class": self.marshal_classes(),
            "properties": self.marshal_properties(),
            "entities": self.marshal_entities(),
            "links": self.marshal_links(),
            "actions": self.marshal_actions(),
            "title": self.marshal_title(),
            }

    def marshal_classes(self):
        """Marshal entity's classes.

        :returns: list with string names of entity's classes.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        entity = self._entity
        try:
            classes = list(str(class_) for class_ in entity.classes)
        except AttributeError as error:
            logger.error("Failed to get entity's classes")
            raise ValueError("Failed to get entity's classes") from error
        except TypeError as error:
            logger.error("Failed to marshal an entity: failed to iterate over entity's classes")
            raise ValueError("Failed to iterate over entity's classes") from error

        return classes

    def marshal_properties(self):
        """Marshal entity's properties.

        :returns: JSON serializable object with entity's properties.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        entity = self._entity
        try:
            properties = json.loads(json.dumps(entity.properties))
        except AttributeError as error:
            logger.error("Failed to get entity's")
            raise ValueError("Failed to get entity's properties") from error
        except TypeError as error:
            logger.error("Failed to marshal entity's properties")
            raise ValueError("Failed to marshal entity's properties") from error

        return properties

    def marshal_entities(self):
        """Marshal entity's sub-entities.

        :returns: list with marshaled data of entity's sub-entities.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        entity = self._entity
        try:
            entity_sub_entities = list(entity.entities)
        except AttributeError as error:
            logger.error("Failed to get sub-entities of the entity")
            raise ValueError("Failed to get sub-entities of the entity") from error
        except TypeError as error:
            logger.error("Failed to iterate over sub-entities of the entity")
            raise ValueError("Failed to iterate over sub-entities of the entity") from error

        marshaler = self._marshaler
        marshal_sub_entity = lambda sub_entity: _marshal_sub_entity(sub_entity, marshaler)

        marshaled_sub_entities = []
        for sub_entity in entity_sub_entities:
            try:
                sub_entity_data = marshal_sub_entity(sub_entity)
            except Exception as error:
                logger.error("Failed to marshal sub-entities of the entity")
                raise ValueError("Failed to marshal sub-entities of the entity") from error

            marshaled_sub_entities.append(sub_entity_data)

        return marshaled_sub_entities

    def marshal_links(self):
        """Marshal entity's links.

        :returns: list with marshaled data of entity's links.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        entity = self._entity
        try:
            entity_links = list(entity.links)
        except AttributeError as error:
            logger.error("Failed to get entity's links")
            raise ValueError("Failed to get entity's links") from error
        except TypeError as error:
            logger.error("Failed to iterate over entity's links")
            raise ValueError("Failed to iterate over entity's links") from error

        marshal_link = self._marshaler.marshal_link

        marshaled_links = []
        for link in entity_links:
            try:
                link_data = marshal_link(link)
            except Exception as error:
                logger.error("Failed to marshal entity's links")
                raise ValueError("Failed to marshal entity's links") from error

            marshaled_links.append(link_data)

        return marshaled_links

    def marshal_actions(self):
        """Marshal entity's actions.

        :returns: list with marshaled data of entity's actions.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        entity = self._entity
        try:
            entity_actions = list(entity.actions)
        except AttributeError as error:
            logger.error("Failed to get entity's actions")
            raise ValueError("Failed to get entity's actions") from error
        except TypeError as error:
            logger.error("Failed to iterate over entity's actions")
            raise ValueError("Failed to iterate over entity's actions") from error

        marshal_action = self._marshaler.marshal_action
        marshaled_actions = []
        for action in entity_actions:
            try:
                action_data = marshal_action(action)
            except Exception as error:
                logger.error("Failed to marshal entity's actions")
                raise ValueError("Failed to marshal entity's actions") from error

            marshaled_actions.append(action_data)

        return marshaled_actions

    def marshal_title(self):
        """Marshal entity's title.

        :returns: string title of the entity or None.
        :raises: :class:ValueError.
        """
        entity = self._entity
        try:
            title = entity.title
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get entity's title")
            raise ValueError("Failed to get entity's title") from error

        if title is not None:
            title = str(title)

        return title


class EmbeddedRepresentationMarshaler:
    """Class to marshal a single embedded representation."""

    def __init__(self, embedded_representation, marshaler):
        self._embedded_representation = embedded_representation
        self._marshaler = marshaler

    def marshal(self):
        """Marshal the embedded representation.

        :returns: dictionary with entity data.
        :raises: :class:ValueError.
        """
        return {
            "rel": self.marshal_relations(),
            "class": self.marshal_classes(),
            "properties": self.marshal_properties(),
            "entities": self.marshal_entities(),
            "links": self.marshal_links(),
            "actions": self.marshal_actions(),
            "title": self.marshal_title(),
            }

    def marshal_relations(self):
        """Marshal relations of the embedded representation.

        :returns: list of string relations of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        embedded_representation = self._embedded_representation
        try:
            relations = list(str(relation) for relation in embedded_representation.relations)
        except AttributeError as error:
            logger.error("Failed to get relations of the embedded representation")
            raise ValueError("Failed to get relations of the embedded representation") from error
        except TypeError as error:
            logger.error("Failed to iterate over relations of the embedded representation")
            raise ValueError(
                "Failed to iterate over relations of the embedded representation",
                ) from error

        return relations

    def marshal_classes(self):
        """Marshal classes of the embedded representation.

        :returns: list with string names of classes of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        embedded_representation = self._embedded_representation
        try:
            classes = list(str(class_) for class_ in embedded_representation.classes)
        except AttributeError as error:
            logger.error("Failed to get classes of the embedded representation")
            raise ValueError("Failed to get classes of the embedded representation") from error
        except TypeError as error:
            logger.error("Failed to iterate over classes of the embedded representation")
            raise ValueError(
                "Failed to iterate over classes of the embedded representation",
                ) from error

        return classes

    def marshal_properties(self):
        """Marshal properties of the embedded representation.

        :returns: JSON serializable object with properties of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        embedded_representation = self._embedded_representation
        try:
            properties = json.loads(json.dumps(embedded_representation.properties))
        except AttributeError as error:
            logger.error("Failed to get properties of the embedded representation")
            raise ValueError("Failed to get properties of the embedded representation") from error
        except TypeError as error:
            logger.error("Failed to marshal properties of the embedded representation")
            raise ValueError(
                "Failed to marshal properties of the embedded representation",
                ) from error

        return properties

    def marshal_entities(self):
        """Marshal sub-entities of the embedded representation.

        :returns: list with marshaled data of sub-entities of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        embedded_representation = self._embedded_representation
        try:
            representation_sub_entities = list(embedded_representation.entities)
        except AttributeError as error:
            logger.error("Failed to get sub-entities of the embedded representation")
            raise ValueError("Failed to get sub-entities of the embedded representation") from error
        except TypeError as error:
            logger.error("Failed to iterate over sub-entities of the embedded representation")
            raise ValueError(
                "Failed to iterate over sub-entities of the embedded representation",
                ) from error

        marshaler = self._marshaler
        marshal_sub_entity = lambda sub_entity: _marshal_sub_entity(sub_entity, marshaler)

        marshaled_sub_entities = []
        for sub_entity in representation_sub_entities:
            try:
                sub_entity_data = marshal_sub_entity(sub_entity)
            except Exception as error:
                logger.error("Failed to marshal sub-entities of the embedded representation")
                raise ValueError(
                    "Failed to marshal sub-entities of the embedded representation",
                    ) from error

            marshaled_sub_entities.append(sub_entity_data)

        return marshaled_sub_entities

    def marshal_links(self):
        """Marshal links of the embedded representation.

        :returns: list with marshaled data of links of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        embedded_representation = self._embedded_representation
        try:
            representation_links = list(embedded_representation.links)
        except AttributeError as error:
            logger.error("Failed to get links of the embedded representation")
            raise ValueError("Failed to get links of the embedded representation") from error
        except TypeError as error:
            logger.error("Failed to iterate over links of the embedded representation")
            raise ValueError(
                "Failed to iterate over links of the embedded representation",
                ) from error

        marshal_link = self._marshaler.marshal_link

        marshaled_links = []
        for link in representation_links:
            try:
                link_data = marshal_link(link)
            except Exception as error:
                logger.error("Failed to marshal links of the embedded representation")
                raise ValueError(
                    "Failed to marshal links of the embedded representation",
                    ) from error

            marshaled_links.append(link_data)

        return marshaled_links

    def marshal_actions(self):
        """Marshal actions of the embedded representation.

        :returns: list with marshaled data of actions of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        embedded_representation = self._embedded_representation
        try:
            representation_actions = list(embedded_representation.actions)
        except AttributeError as error:
            logger.error("Failed to get actions of the embedded representation")
            raise ValueError("Failed to get actions of the embedded representation") from error
        except TypeError as error:
            logger.error("Failed to iterate over actions of the embedded representation")
            raise ValueError(
                "Failed to iterate over actions of the embedded representation",
                ) from error

        marshal_action = self._marshaler.marshal_action

        marshaled_actions = []
        for action in representation_actions:
            try:
                action_data = marshal_action(action)
            except Exception as error:
                logger.error("Failed to marshal actions of the embedded representation")
                raise ValueError(
                    "Failed to marshal actions of the embedded representation",
                    ) from error

            marshaled_actions.append(action_data)

        return marshaled_actions

    def marshal_title(self):
        """Marshal title of the embedded representation.

        :returns: string title of the embedded representation or None.
        :raises: :class:ValueError.
        """
        embedded_representation = self._embedded_representation
        try:
            title = embedded_representation.title
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get title of the embedded representation")
            raise ValueError("Failed to get title of the embedded representation") from error

        if title is not None:
            title = str(title)

        return title


class EntityParser:
    """Class to parse a single entity."""

    def __init__(self, data, parser):
        self._data = data
        self._parser = parser

    def parse(self):
        """Parse the entity.

        :returns: :class:`Entity <lila.core.entity.Entity>`.
        """
        return Entity(
            classes=self.parse_classes(),
            properties=self.parse_properties(),
            entities=self.parse_entities(),
            links=self.parse_links(),
            actions=self.parse_actions(),
            title=self.parse_title(),
            )

    def parse_classes(self):
        """Parse entity's classes.

        :returns: list with string names of entity's classes.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            entity_classes = self._data["class"]
        except TypeError as error:
            logger.error("Failed to get classes from entity data")
            raise ValueError("Failed to get classes from entity data") from error
        except KeyError:
            entity_classes = ()

        try:
            entity_classes = tuple(str(class_) for class_ in entity_classes)
        except TypeError as error:
            logger.error("Failed to iterate over classes from entity data")
            raise ValueError("Failed to iterate over classes from entity data") from error

        return entity_classes

    def parse_properties(self):
        """Parse entity's properties.

        :returns: JSON object with entity's properties.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            entity_properties = self._data["properties"]
        except TypeError as error:
            logger.error("Failed to get properties from entity data")
            raise ValueError("Failed to get properties from entity data") from error
        except KeyError:
            entity_properties = {}

        try:
            entity_properties = json.loads(json.dumps(entity_properties))
        except TypeError as error:
            logger.error("Failed to parse entity's properties")
            raise ValueError("Failed to parse entity's properties") from error

        return entity_properties

    def parse_entities(self):
        """Parse entity's sub-entities.

        :returns: list with parsed entity's sub-entities.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            entity_sub_entities_data = self._data["entities"]
        except TypeError as error:
            logger.error("Failed to get sub-entities data from entity data")
            raise ValueError("Failed to get sub-entities data from entity data") from error
        except KeyError:
            entity_sub_entities_data = ()

        try:
            entity_sub_entities_data = list(entity_sub_entities_data)
        except TypeError as error:
            logger.error("Failed to iterate over sub-entities data from entity data")
            raise ValueError("Failed to iterate over sub-entities data from entity data") from error

        parser = self._parser
        parse_sub_entity = lambda data: _parse_sub_entity(data, parser)

        entity_sub_entities = []
        for data in entity_sub_entities_data:
            try:
                sub_entity = parse_sub_entity(data)
            except Exception as error:
                logger.error("Failed to parse entity's sub-entities")
                raise ValueError("Failed to parse entity's sub-entities") from error

            entity_sub_entities.append(sub_entity)

        return tuple(entity_sub_entities)

    def parse_links(self):
        """Parse entity's links.

        :returns: list with parsed entity's links.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            entity_links_data = self._data["links"]
        except TypeError as error:
            logger.error("Failed to get links data from entity data")
            raise ValueError("Failed to get links data from entity data") from error
        except KeyError:
            entity_links_data = ()

        try:
            entity_links_data = list(entity_links_data)
        except TypeError as error:
            logger.error("Failed to iterate over links data from entity data")
            raise ValueError("Failed to iterate over links data from entity data") from error

        parse_link = self._parser.parse_link

        entity_links = []
        for data in entity_links_data:
            try:
                link = parse_link(data)
            except Exception as error:
                logger.error("Failed to parse entity's links")
                raise ValueError("Failed to parse entity's links") from error

            entity_links.append(link)

        return tuple(entity_links)

    def parse_actions(self):
        """Parse entity's actions.

        :returns: list with parsed entity's actions.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            entity_actions_data = self._data["actions"]
        except TypeError as error:
            logger.error("Failed to get actions data from entity data")
            raise ValueError("Failed to get actions data from entity data") from error
        except KeyError:
            entity_actions_data = ()

        try:
            entity_actions_data = list(entity_actions_data)
        except TypeError as error:
            logger.error("Failed to iterate over actions data from entity data")
            raise ValueError("Failed to iterate over actions data from entity data") from error

        parse_action = self._parser.parse_action

        entity_actions = []
        for data in entity_actions_data:
            try:
                action = parse_action(data)
            except Exception as error:
                logger.error("Failed to parse entity's actions")
                raise ValueError("Failed to parse entity's actions") from error

            entity_actions.append(action)

        return tuple(entity_actions)

    def parse_title(self):
        """Parse entity's title.

        :returns: string title of the entity or None.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            entity_title = self._data["title"]
        except TypeError as error:
            logger.error("Failed to get title from entity data")
            raise ValueError("Failed to get title from entity data") from error
        except KeyError:
            entity_title = None

        if entity_title is not None:
            entity_title = str(entity_title)

        return entity_title


class EmbeddedRepresentationParser:
    """Class to parse a single embedded representation."""

    def __init__(self, data, parser):
        self._data = data
        self._parser = parser

    def parse(self):
        """Parse the embedded representation.

        :returns: :class:`EmbeddedRepresentation <lila.core.entity.EmbeddedRepresentation>`.
        """
        return EmbeddedRepresentation(
            relations=self.parse_relations(),
            classes=self.parse_classes(),
            properties=self.parse_properties(),
            entities=self.parse_entities(),
            links=self.parse_links(),
            actions=self.parse_actions(),
            title=self.parse_title(),
            )

    def parse_relations(self):
        """Parse relations of the embedded representation.

        :returns: list of string relations of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            representation_relations = self._data["rel"]
        except TypeError as error:
            logger.error("Failed to get relations from data of the embedded representation")
            raise ValueError(
                "Failed to get relations from data of the embedded representation",
                ) from error
        except KeyError as error:
            logger.error("Data of the embedded representation do not have required 'rel' key")
            raise ValueError(
                "Data of the embedded representation do not have required 'rel' key",
                ) from error

        try:
            representation_relations = tuple(str(relation) for relation in representation_relations)
        except TypeError as error:
            logger.error(
                "Failed to iterate over relations from data of the embedded representation",
                )
            raise ValueError(
                "Failed to iterate over relations from data of the embedded representation",
                ) from error

        return representation_relations

    def parse_classes(self):
        """Parse classes of the embedded representation.

        :returns: list with string names of classes of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            representation_classes = self._data["class"]
        except TypeError as error:
            logger.error("Failed to get classes from data of the embedded representation")
            raise ValueError(
                "Failed to get classes from data of the embedded representation",
                ) from error
        except KeyError:
            representation_classes = ()

        try:
            representation_classes = tuple(str(class_) for class_ in representation_classes)
        except TypeError as error:
            logger.error("Failed to iterate over classes from data of the embedded representation")
            raise ValueError(
                "Failed to iterate over classes from data of the embedded representation",
                ) from error

        return representation_classes

    def parse_properties(self):
        """Parse properties of the embedded representation.

        :returns: JSON object with properties of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            representation_properties = self._data["properties"]
        except TypeError as error:
            logger.error("Failed to get properties from data of the embedded representation")
            raise ValueError(
                "Failed to get properties from data of the embedded representation",
                ) from error
        except KeyError:
            representation_properties = {}

        try:
            representation_properties = json.loads(json.dumps(representation_properties))
        except TypeError as error:
            logger.error("Failed to parse properties of the embedded representation")
            raise ValueError("Failed to parse properties of the embedded representation") from error

        return representation_properties

    def parse_entities(self):
        """Parse sub-entities of the embedded representation.

        :returns: list with parsed sub-entities of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            representation_sub_entities_data = self._data["entities"]
        except TypeError as error:
            logger.error("Failed to get sub-entities data from data of the embedded representation")
            raise ValueError(
                "Failed to get sub-entities data from data of the embedded representation",
                ) from error
        except KeyError:
            representation_sub_entities_data = ()

        try:
            representation_sub_entities_data = list(representation_sub_entities_data)
        except TypeError as error:
            logger.error(
                "Failed to iterate over sub-entities data from data of the embedded representation",
                )
            raise ValueError(
                "Failed to iterate over sub-entities data from data of the embedded representation",
                ) from error

        parser = self._parser
        parse_sub_entity = lambda data: _parse_sub_entity(data, parser)

        representation_sub_entities = []
        for data in representation_sub_entities_data:
            try:
                sub_entity = parse_sub_entity(data)
            except Exception as error:
                logger.error("Failed to parse sub-entities of the embedded representation")
                raise ValueError(
                    "Failed to parse sub-entities of the embedded representation",
                    ) from error

            representation_sub_entities.append(sub_entity)

        return tuple(representation_sub_entities)

    def parse_links(self):
        """Parse links of the embedded representation.

        :returns: list with parsed links of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            representation_links_data = self._data["links"]
        except TypeError as error:
            logger.error("Failed to get links data from data of the embedded representation")
            raise ValueError(
                "Failed to get links data from data of the embedded representation",
                ) from error
        except KeyError:
            representation_links_data = ()

        try:
            representation_links_data = list(representation_links_data)
        except TypeError as error:
            logger.error(
                "Failed to iterate over links data from data of the embedded representation",
                )
            raise ValueError(
                "Failed to iterate over links data from data of the embedded representation",
                ) from error

        parse_link = self._parser.parse_link

        representation_links = []
        for data in representation_links_data:
            try:
                link = parse_link(data)
            except Exception as error:
                logger.error("Failed to parse links of the embedded representation")
                raise ValueError("Failed to parse links of the embedded representation") from error

            representation_links.append(link)

        return tuple(representation_links)

    def parse_actions(self):
        """Parse actions of the embedded representation.

        :returns: list with parsed actions of the embedded representation.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            representation_actions_data = self._data["actions"]
        except TypeError as error:
            logger.error(
                "Failed to get actions data from data of the embedded representation",
                )
            raise ValueError(
                "Failed to get actions data from data of the embedded representation",
                ) from error
        except KeyError:
            representation_actions_data = ()

        try:
            representation_actions_data = list(representation_actions_data)
        except TypeError as error:
            logger.error(
                "Failed to iterate over actions data from data of the embedded representation",
                )
            raise ValueError(
                "Failed to iterate over actions data from data of the embedded representation",
                ) from error

        parse_action = self._parser.parse_action

        representation_actions = []
        for data in representation_actions_data:
            try:
                action = parse_action(data)
            except Exception as error:
                logger.error("Failed to parse actions of the embedded representation")
                raise ValueError(
                    "Failed to parse actions of the embedded representation",
                    ) from error

            representation_actions.append(action)

        return tuple(representation_actions)

    def parse_title(self):
        """Parse title of the embedded representation.

        :returns: string title of the embedded representation or None.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            representation_title = self._data["title"]
        except TypeError as error:
            logger.error("Failed to get title from data of the embedded representation")
            raise ValueError(
                "Failed to get title from data of the embedded representation",
                ) from error
        except KeyError:
            representation_title = None

        if representation_title is not None:
            representation_title = str(representation_title)

        return representation_title


def _marshal_sub_entity(sub_entity, marshaler):
    """Marshal the sub-entity.

    :param sub_entity: either embedded link or embedded representation.
    :param marshaler: marshaller for the Siren entities.
    :returns: dictionary with sub-entity data.
    :raises: :class:ValueError.
    """
    logger = logging.getLogger(__name__)

    if hasattr(sub_entity, "target"):
        logger.debug("Marshal sub-entity as an embedded representation")
        marshaled_sub_entity = marshaler.marshal_embedded_representation(sub_entity)
    else:
        logger.debug("Marshal sub-entity as an embedded link")
        marshaled_sub_entity = marshaler.marshal_embedded_link(sub_entity)

    return marshaled_sub_entity


def _parse_sub_entity(data, parser):
    """Parse the sub-entity.

    :param data: dictionary with sub-entity data.
    :param parser: parser of the Siren entities.
    :returns: parsed sub-entity.
    :raises: :class:ValueError.
    """
    logger = logging.getLogger(__name__)

    if "href" in data:
        logger.debug("Parse data as for an embedded representation")
        parsed_sub_entity = parser.parse_embedded_link(data)
    else:
        logger.debug("Parse data as for an embedded link")
        parsed_sub_entity = parser.parse_embedded_representation(data)

    return parsed_sub_entity
