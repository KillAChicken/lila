"""Module with default marshaler for an action."""

import logging

from lila.core.action import Method


class ActionMarshaler:
    """Class to marshal a single action."""

    def __init__(self, action, marshaler):
        self._action = action
        self._marshaler = marshaler

    def marshal(self):
        """Marshal the action.

        :returns: dictionary with action data.
        :raises: :class:ValueError.
        """
        return {
            "name": self.marshal_name(),
            "class": self.marshal_classes(),
            "method": self.marshal_method(),
            "href": self.marshal_target(),
            "title": self.marshal_title(),
            "type": self.marshal_encoding_type(),
            "fields": self.marshal_fields(),
            }

    def marshal_name(self):
        """Marshal action's name.

        :returns: string name of the action.
        :raises: :class:ValueError.
        """
        action = self._action
        try:
            name = action.name
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get action's name")
            raise ValueError("Failed to get action's name") from error

        return str(name)

    def marshal_classes(self):
        """Marshal action's classes.

        :returns: list with string names of action's classes.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        action = self._action
        try:
            classes = list(str(class_) for class_ in action.classes)
        except AttributeError as error:
            logger.error("Failed to get action's classes")
            raise ValueError("Failed to get action's classes") from error
        except TypeError as error:
            logger.error("Failed to iterate over action's classes")
            raise ValueError("Failed to iterate over action's classes") from error

        return classes

    def marshal_method(self):
        """Marshal action's method.

        :returns: string value of action's method.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        action = self._action
        try:
            method = str(action.method)
        except AttributeError as error:
            logger.error("Failed to get action's method")
            raise ValueError("Failed to get action's method") from error

        try:
            method = Method(method)
        except ValueError:
            logger.error("Action's method is not supported")
            raise ValueError("Action's method is not supported")

        return method.value

    def marshal_target(self):
        """Marshal action's target.

        :returns: string target of the action.
        :raises: :class:ValueError.
        """
        action = self._action
        try:
            target = action.target
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get action's target")
            raise ValueError("Failed to get action's target") from error

        return str(target)

    def marshal_title(self):
        """Marshal action's title.

        :returns: string title of the action or None.
        :raises: :class:ValueError.
        """
        action = self._action
        try:
            title = action.title
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get action's title")
            raise ValueError("Failed to get action's title") from error

        if title is not None:
            title = str(title)

        return title

    def marshal_encoding_type(self):
        """Marshal action's encoding type.

        :returns: string value of action's encoding type or None.
        :raises: :class:ValueError.
        """
        action = self._action
        try:
            encoding_type = action.encoding_type
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get action's encoding type")
            raise ValueError("Failed to get action's encoding type") from error

        if encoding_type is not None:
            encoding_type = str(encoding_type)

        return encoding_type

    def marshal_fields(self):
        """Marshal action's fields.

        :returns: list with marshaled data of action's fields.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        action = self._action
        marshal_field = self._marshaler.marshal_field
        try:
            marshaled_fields = list(marshal_field(field) for field in action.fields)
        except AttributeError as error:
            logger.error("Failed to get action's fields")
            raise ValueError("Failed to get action's fields") from error
        except TypeError as error:
            logger.error("Failed to iterate over action's fields")
            raise ValueError("Failed to iterate over action's fields") from error
        except ValueError as error:
            logger.error("Failed to marshal action's fields")
            raise ValueError("Failed to marshal action's fields") from error

        return marshaled_fields
