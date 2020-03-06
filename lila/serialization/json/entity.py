"""Module with default marshaler for an entity."""

import logging
import json


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
            raise ValueError("Failed to get sub entities of the entity") from error
        except TypeError as error:
            logger.error("Failed to iterate over sub-entities of the entity")
            raise ValueError("Failed to iterate over sub entities of the entity") from error

        marshaler = self._marshaler
        marshal_sub_entity = lambda sub_entity: _marshal_sub_entity(sub_entity, marshaler)

        marshaled_sub_entities = []
        for sub_entity in entity_sub_entities:
            try:
                sub_entity_data = marshal_sub_entity(sub_entity)
            except Exception as error:
                logger.error("Failed to marshal sub-entities of the entity")
                raise ValueError("Failed to marshal sub entities of the entity") from error

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
            raise ValueError("Failed to get sub entities of the embedded representation") from error
        except TypeError as error:
            logger.error("Failed to iterate over sub-entities of the embedded representation")
            raise ValueError(
                "Failed to iterate over sub entities of the embedded representation",
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
                    "Failed to marshal sub entities of the embedded representation",
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
