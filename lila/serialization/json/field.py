"""Module with default marshaler for a field."""

import logging
from lila.core.field import InputType


class FieldMarshaler:
    """Class to marshal a single field."""

    def __init__(self, field):
        self._field = field

    def marshal(self):
        """Marshal the field.

        :returns: dictionary with field data.
        :raises: :class:ValueError.
        """
        return {
            "name": self.marshal_name(),
            "class": self.marshal_classes(),
            "type": self.marshal_input_type(),
            "value": self.marshal_value(),
            "title": self.marshal_title(),
            }

    def marshal_name(self):
        """Marshal field's name.

        :returns: string name of the field.
        :raises: :class:ValueError.
        """
        field = self._field
        try:
            name = field.name
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get field's name")
            raise ValueError("Failed to get field's name") from error

        return str(name)

    def marshal_classes(self):
        """Marshal field's classes.

        :returns: list with string names of field's classes.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        field = self._field
        try:
            classes = list(str(class_) for class_ in field.classes)
        except AttributeError as error:
            logger.error("Failed to get field's classes")
            raise ValueError("Failed to get field's classes") from error
        except TypeError as error:
            logger.error("Failed to iterate over field's classes")
            raise ValueError("Failed to iterate over field's classes") from error

        return classes

    def marshal_input_type(self):
        """Marshal field's input type.

        :returns: string value of field's input type.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        field = self._field
        try:
            input_type = str(field.input_type)
        except AttributeError as error:
            logger.error("Failed to get field's input type")
            raise ValueError("Failed to get field's input type") from error

        try:
            input_type = InputType(input_type)
        except ValueError:
            logger.error("Field's input type is not supported")
            raise ValueError("Field's input type is not supported")

        return input_type.value

    def marshal_value(self):
        """Marshal field's value.

        :returns: string value of the field or None.
        :raises: :class:ValueError.
        """
        field = self._field
        try:
            value = field.value
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get field's value")
            raise ValueError("Failed to get field's value") from error

        if value is not None:
            value = str(value)

        return value

    def marshal_title(self):
        """Marshal field's title.

        :returns: string title of the field or None.
        :raises: :class:ValueError.
        """
        field = self._field
        try:
            title = field.title
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get field's title")
            raise ValueError("Failed to get field's title") from error

        if title is not None:
            title = str(title)

        return title
