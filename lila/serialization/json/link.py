"""Module with default marshaler for a link."""

import logging


class LinkMarshaler:
    """Class to marshal a single link."""

    def __init__(self, link):
        self._link = link

    def marshal(self):
        """Marshal the link.

        :returns: dictionary with link data.
        :raises: :class:ValueError.
        """
        return {
            "rel": self.marshal_relations(),
            "class": self.marshal_classes(),
            "href": self.marshal_target(),
            "title": self.marshal_title(),
            "type": self.marshal_target_media_type(),
            }

    def marshal_relations(self):
        """Marshal link's relations.

        :returns: list of string relations of the link.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        link = self._link
        try:
            relations = list(str(relation) for relation in link.relations)
        except AttributeError as error:
            logger.error("Failed to get link's relations")
            raise ValueError("Failed to get link's relations") from error
        except TypeError as error:
            logger.error("Failed to iterate over link's relations")
            raise ValueError("Failed to iterate over link's relations") from error

        return relations

    def marshal_classes(self):
        """Marshal link's classes.

        :returns: list with string names of link's classes.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        link = self._link
        try:
            classes = list(str(class_) for class_ in link.classes)
        except AttributeError as error:
            logger.error("Failed to get link's classes")
            raise ValueError("Failed to get link's classes") from error
        except TypeError as error:
            logger.error("Failed to iterate over link's classes")
            raise ValueError("Failed to iterate over link's classes") from error

        return classes

    def marshal_target(self):
        """Marshal link's target.

        :returns: string target of the link.
        :raises: :class:ValueError.
        """
        link = self._link
        try:
            target = link.target
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get link's target")
            raise ValueError("Failed to get link's target") from error

        return str(target)

    def marshal_title(self):
        """Marshal link's title.

        :returns: string title of the link or None.
        :raises: :class:ValueError.
        """
        link = self._link
        try:
            title = link.title
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get link's title")
            raise ValueError("Failed to get link's title") from error

        if title is not None:
            title = str(title)

        return title

    def marshal_target_media_type(self):
        """Marshal link's target media type.

        :returns: string value of link's target media type or None.
        :raises: :class:ValueError.
        """
        link = self._link
        try:
            target_media_type = link.target_media_type
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get link's target media type")
            raise ValueError("Failed to get link's target media type") from error

        if target_media_type is not None:
            target_media_type = str(target_media_type)

        return target_media_type


class EmbeddedLinkMarshaler:
    """Class to marshal a single embedded link."""

    def __init__(self, embedded_link):
        self._embedded_link = embedded_link

    def marshal(self):
        """Marshal the embedded link.

        :returns: dictionary with data of the embedded link.
        :raises: :class:ValueError.
        """
        return {
            "rel": self.marshal_relations(),
            "class": self.marshal_classes(),
            "href": self.marshal_target(),
            "title": self.marshal_title(),
            "type": self.marshal_target_media_type(),
            }

    def marshal_relations(self):
        """Marshal relations of the embedded link.

        :returns: list of string relations of the embedded link.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        embedded_link = self._embedded_link
        try:
            relations = list(str(relation) for relation in embedded_link.relations)
        except AttributeError as error:
            logger.error("Failed to get relations of the embedded link")
            raise ValueError("Failed to get relations of the embedded link") from error
        except TypeError as error:
            logger.error("Failed to iterate over relations of the embedded link")
            raise ValueError("Failed to iterate over relations of the embedded link") from error

        return relations

    def marshal_classes(self):
        """Marshal classes of the embedded link.

        :returns: list with string names of classes of the embedded link.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        embedded_link = self._embedded_link
        try:
            classes = list(str(class_) for class_ in embedded_link.classes)
        except AttributeError as error:
            logger.error("Failed to get classes of the embedded link")
            raise ValueError("Failed to get classes of the embedded link") from error
        except TypeError as error:
            logger.error("Failed to iterate over classes of the embedded link")
            raise ValueError("Failed to iterate over classes of the embedded link") from error

        return classes

    def marshal_target(self):
        """Marshal target of the embedded link.

        :returns: string target of the embedded link.
        :raises: :class:ValueError.
        """
        embedded_link = self._embedded_link
        try:
            target = embedded_link.target
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get target of the embedded link")
            raise ValueError("Failed to get target of the embedded link") from error

        return str(target)

    def marshal_title(self):
        """Marshal title of the embedded link.

        :returns: string title of the embedded link or None.
        :raises: :class:ValueError.
        """
        embedded_link = self._embedded_link
        try:
            title = embedded_link.title
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get title of the embedded link")
            raise ValueError("Failed to get title of the embedded link") from error

        if title is not None:
            title = str(title)

        return title

    def marshal_target_media_type(self):
        """Marshal target media type of the embedded link.

        :returns: string value of target media type of the embedded link or None.
        :raises: :class:ValueError.
        """
        embedded_link = self._embedded_link
        try:
            target_media_type = embedded_link.target_media_type
        except AttributeError as error:
            logging.getLogger(__name__).error(
                "Failed to get target media type of the embedded link",
                )
            raise ValueError("Failed to get target media type of the embedded link") from error

        if target_media_type is not None:
            target_media_type = str(target_media_type)

        return target_media_type
