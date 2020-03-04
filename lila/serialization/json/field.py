"""Module with default marshaler and parser for a field."""

import logging

from lila.core.field import Field, InputType


class FieldMarshaler:
    """Class to marshal a single field."""

    def __init__(self, field):
        self._field = field

    def marshal(self):
        """Marshal the field.

        :returns: dictionary with field data.
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
        except ValueError as error:
            logger.error("Field's input type is not supported")
            raise ValueError("Field's input type is not supported") from error

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


class FieldParser:
    """Class to parse a single field."""

    def __init__(self, data):
        self._data = data

    def parse(self):
        """Parse a field from the data.

        :returns: :class:`Field <lila.core.field.Field>`.
        """
        return Field(
            name=self.parse_name(),
            classes=self.parse_classes(),
            input_type=self.parse_input_type(),
            value=self.parse_value(),
            title=self.parse_title(),
            )

    def parse_name(self):
        """Parse field's name.

        :returns: string name of the field.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            field_name = self._data["name"]
        except TypeError as error:
            logger.error("Failed to get name from field data")
            raise ValueError("Failed to get name from field data") from error
        except KeyError as error:
            logger.error("Field data do not have required 'name' key")
            raise ValueError("Field data do not have required 'name' key") from error

        return str(field_name)

    def parse_classes(self):
        """Parse field's classes.

        :returns: list with string names of field's classes.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            field_classes = self._data["class"]
        except TypeError as error:
            logger.error("Failed to get classes from field data")
            raise ValueError("Failed to get classes from field data") from error
        except KeyError:
            field_classes = ()

        try:
            field_classes = tuple(str(class_) for class_ in field_classes)
        except TypeError as error:
            logger.error("Failed to iterate over classes from field data")
            raise ValueError("Failed to iterate over classes from field data") from error

        return field_classes

    def parse_input_type(self):
        """Parse field's input type.

        :returns: :class:`InputType <lila.core.field.InputType>`.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            field_input_type = self._data["type"]
        except TypeError as error:
            logger.error("Failed to get input type from field data")
            raise ValueError("Failed to get input type from field data") from error
        except KeyError:
            field_input_type = InputType.TEXT.value

        try:
            field_input_type = InputType(field_input_type)
        except ValueError as error:
            logger.error("Field data contain not supported input type")
            raise ValueError("Field data contain not supported input type") from error

        return field_input_type

    def parse_value(self):
        """Parse field's value.

        :returns: string value or None.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            field_value = self._data["value"]
        except TypeError as error:
            logger.error("Failed to get value from field data")
            raise ValueError("Failed to get value from field data") from error
        except KeyError:
            field_value = None

        if field_value is not None:
            field_value = str(field_value)

        return field_value

    def parse_title(self):
        """Parse field's title.

        :returns: string title of the field or None.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            field_title = self._data["title"]
        except TypeError as error:
            logger.error("Failed to get title from field data")
            raise ValueError("Failed to get title from field data") from error
        except KeyError:
            field_title = None

        if field_title is not None:
            field_title = str(field_title)

        return field_title
