"""Module with JSON marshaler for Siren objects."""

import logging

from lila.core.field import InputType
from lila.core.action import Method
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

        if not isinstance(input_type, InputType):
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

    def marshal_action(self, action):
        """Marshal Siren action.

        :param action: Siren Action.
        :returns: dictionary with action data.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marhal an action '%s'", action)

        try:
            name = str(action.name)
        except AttributeError as error:
            logger.error("Failed to marshal an action: failed to get action's name")
            raise ValueError("Failed to get action's name") from error

        try:
            classes = list(str(class_) for class_ in action.classes)
        except AttributeError as error:
            logger.error("Failed to marshal an action: failed to get action's classes")
            raise ValueError("Failed to get action's classes") from error
        except TypeError as error:
            logger.error("Failed to marshal an action: failed to iterate over action's classes")
            raise ValueError("Failed to iterate over action's classes") from error

        try:
            method = action.method
        except AttributeError as error:
            logger.error("Failed to marshal an action: failed to get action's method")
            raise ValueError("Failed to get action's method") from error

        if not isinstance(method, Method):
            logger.error("Failed to marshal an action: action's method is not supported")
            raise ValueError("Action's method is not supported")

        try:
            target = str(action.target)
        except AttributeError as error:
            logger.error("Failed to marshal an action: failed to get action's target")
            raise ValueError("Failed to get action's target") from error

        try:
            title = action.title
        except AttributeError as error:
            logger.error("Failed to marshal a action: failed to get action's title")
            raise ValueError("Failed to get action's title") from error

        if title is not None:
            title = str(title)

        try:
            encoding_type = action.encoding_type
        except AttributeError as error:
            logger.error("Failed to marshal a action: failed to get action's encoding type")
            raise ValueError("Failed to get action's encoding type") from error

        if encoding_type is not None:
            encoding_type = str(encoding_type)

        try:
            fields = list(self.marshal_field(field) for field in action.fields)
        except AttributeError as error:
            logger.error("Failed to marshal an action: failed to get action's fields")
            raise ValueError("Failed to get action's fields") from error
        except TypeError as error:
            logger.error("Failed to marshal an action: failed to iterate over action's fields")
            raise ValueError("Failed to iterate over action's fields") from error
        except ValueError as error:
            logger.error("Failed to marshal an action: failed to marshal action's fields")
            raise ValueError("Failed to marshal action's fields") from error

        marshaled_action = {
            "name": name,
            "class": classes,
            "method": method.value,
            "href": target,
            "title": title,
            "type": encoding_type,
            "fields": fields,
            }

        logger.info("Successfully marshaled an action")
        return marshaled_action

    def marshal_link(self, link):
        """Marshal Siren link.

        :param link: Siren Link.
        :returns: dictionary with link data.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marhal a link '%s'", link)

        try:
            relations = list(str(relation) for relation in link.relations)
        except AttributeError as error:
            logger.error("Failed to marshal a link: failed to get link's relations")
            raise ValueError("Failed to get link's relations") from error
        except TypeError as error:
            logger.error("Failed to marshal a link: failed to iterate over link's relations")
            raise ValueError("Failed to iterate over link's relations") from error

        try:
            classes = list(str(class_) for class_ in link.classes)
        except AttributeError as error:
            logger.error("Failed to marshal a link: failed to get link's classes")
            raise ValueError("Failed to get link's classes") from error
        except TypeError as error:
            logger.error("Failed to marshal a link: failed to iterate over link's classes")
            raise ValueError("Failed to iterate over link's classes") from error

        try:
            target = str(link.target)
        except AttributeError as error:
            logger.error("Failed to marshal a link: failed to get link's target")
            raise ValueError("Failed to get link's target") from error

        try:
            title = link.title
        except AttributeError as error:
            logger.error("Failed to marshal a link: failed to get link's title")
            raise ValueError("Failed to get link's title") from error

        if title is not None:
            title = str(title)

        try:
            target_media_type = link.target_media_type
        except AttributeError as error:
            logger.error("Failed to marshal a link: failed to get link's target media type")
            raise ValueError("Failed to get link's target media type") from error

        if target_media_type is not None:
            target_media_type = str(target_media_type)

        marshaled_link = {
            "rel": relations,
            "class": classes,
            "href": target,
            "title": title,
            "type": target_media_type,
            }

        logger.info("Successfully marshaled a link")
        return marshaled_link

    def marshal_embedded_link(self, embedded_link):
        """Marshal embedded Siren link.

        :param embedded_link: embedded Siren Link.
        :returns: dictionary with embedded link data.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marhal an embedded link '%s'", embedded_link)

        try:
            relations = list(str(relation) for relation in embedded_link.relations)
        except AttributeError as error:
            logger.error(
                "Failed to marshal an embedded link: failed to get relations of the embedded link",
                )
            raise ValueError("Failed to get relations of the embedded link") from error
        except TypeError as error:
            logger.error(
                "Failed to marshal an embedded link: failed to iterate over relations of the embedded link",    # pylint: disable=line-too-long
                )
            raise ValueError("Failed to iterate over relations of the embedded link") from error

        try:
            classes = list(str(class_) for class_ in embedded_link.classes)
        except AttributeError as error:
            logger.error(
                "Failed to marshal an embedded link: failed to get classes of the embedded link",
            )
            raise ValueError("Failed to get classes of the embedded link") from error
        except TypeError as error:
            logger.error(
                "Failed to marshal an embedded link: failed to iterate over classes of the embedded link",  # pylint: disable=line-too-long
                )
            raise ValueError("Failed to iterate over classes of the embedded link") from error

        try:
            target = str(embedded_link.target)
        except AttributeError as error:
            logger.error("Failed to marshal an link: failed to get target of the embedded link")
            raise ValueError("Failed to get target of the embedded link") from error

        try:
            title = embedded_link.title
        except AttributeError as error:
            logger.error(
                "Failed to marshal an embedded link: failed to get title of the embedded link",
                )
            raise ValueError("Failed to get title of the embedded link") from error

        if title is not None:
            title = str(title)

        try:
            target_media_type = embedded_link.target_media_type
        except AttributeError as error:
            logger.error(
                "Failed to marshal an embedded link: failed to get target media type of the embedded link", # pylint: disable=line-too-long
                )
            raise ValueError("Failed to get target media type of the embedded link") from error

        if target_media_type is not None:
            target_media_type = str(target_media_type)

        marshaled_link = {
            "rel": relations,
            "class": classes,
            "href": target,
            "title": title,
            "type": target_media_type,
            }

        logger.info("Successfully marshaled an embedded link")
        return marshaled_link
