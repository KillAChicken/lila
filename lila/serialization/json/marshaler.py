"""Module with JSON marshaler for Siren objects."""

import logging

from lila.core.field import InputType
from lila.serialization.marshaler import Marshaler


class JSONMarshaler(Marshaler):
    """Class to marshal Siren objects into JSON."""

    def marshal_field(self, field):
        """Marshal Siren field.

        :param field: Siren Field.
        :returns: dictionary with field data.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marhal a field '%s'", field)

        try:
            name = str(field.name)
        except AttributeError as error:
            logger.error("Failed to marshal a field: failed to get field's name")
            raise ValueError("Failed to get field's name") from error

        try:
            classes = list(str(class_) for class_ in field.classes)
        except AttributeError as error:
            logger.error("Failed to marshal a field: failed to get field's classes")
            raise ValueError("Failed to get field's classes") from error
        except TypeError as error:
            logger.error("Failed to marshal a field: failed to iterate over field's classes")
            raise ValueError("Failed to iterate over field's classes") from error

        try:
            input_type = field.input_type
        except AttributeError as error:
            logger.error("Failed to marshal a field: failed to get field's input type")
            raise ValueError("Failed to get field's input type") from error

        if input_type not in InputType:
            logger.error("Failed to marshal a field: field's input type is not supported")
            raise ValueError("Field's input type is not supported")

        try:
            value = field.value
        except AttributeError as error:
            logger.error("Failed to marshal a field: failed to get field's value")
            raise ValueError("Failed to get field's value") from error

        if value is not None:
            value = str(value)

        try:
            title = field.title
        except AttributeError as error:
            logger.error("Failed to marshal a field: failed to get field's title")
            raise ValueError("Failed to get field's title") from error

        if title is not None:
            title = str(title)

        marshaled_field = {
            "name": name,
            "class": classes,
            "type": input_type.value,
            "value": value,
            "title": title,
            }

        logger.info("Successfully marshaled a field")
        return marshaled_field
