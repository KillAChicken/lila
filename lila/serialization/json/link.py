"""Module with default marshaler and parser for a link and embedded link."""

import logging

from lila.core.link import Link, EmbeddedLink


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


class LinkParser:
    """Class to parse a single link."""

    def __init__(self, data):
        self._data = data

    def parse(self):
        """Parse the link.

        :returns: :class:`Link <lila.core.link.Link>`.
        """
        return Link(
            relations=self.parse_relations(),
            classes=self.parse_classes(),
            target=self.parse_target(),
            title=self.parse_title(),
            target_media_type=self.parse_target_media_type(),
            )

    def parse_relations(self):
        """Parse link's relations.

        :returns: list of string relations of the link.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            link_relations = self._data["rel"]
        except TypeError as error:
            logger.error("Failed to get relations from link data")
            raise ValueError("Failed to get relations from link data") from error
        except KeyError as error:
            logger.error("Link data do not have required 'rel' key")
            raise ValueError("Link data do not have required 'rel' key") from error

        try:
            link_relations = tuple(str(relation) for relation in link_relations)
        except TypeError as error:
            logger.error("Failed to iterate over relations from link data")
            raise ValueError("Failed to iterate over relations from link data") from error

        return link_relations

    def parse_classes(self):
        """Parse link's classes.

        :returns: list with string names of link's classes.
        """
        logger = logging.getLogger(__name__)

        try:
            link_classes = self._data["class"]
        except TypeError as error:
            logger.error("Failed to get classes from link data")
            raise ValueError("Failed to get classes from link data") from error
        except KeyError:
            link_classes = ()

        try:
            link_classes = tuple(str(class_) for class_ in link_classes)
        except TypeError as error:
            logger.error("Failed to iterate over classes from link data")
            raise ValueError("Failed to iterate over classes from link data") from error

        return link_classes

    def parse_target(self):
        """Parse link's target.

        :returns: string target of the link.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            link_target = self._data["href"]
        except TypeError as error:
            logger.error("Failed to get target from link data")
            raise ValueError("Failed to get target from link data") from error
        except KeyError as error:
            logger.error("Link data do not have required 'href' key")
            raise ValueError("Link data do not have required 'href' key") from error

        return str(link_target)

    def parse_title(self):
        """Parse link's title.

        :returns: string title of the link or None.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            link_title = self._data["title"]
        except TypeError as error:
            logger.error("Failed to get title from link data")
            raise ValueError("Failed to get title from link data") from error
        except KeyError:
            link_title = None

        if link_title is not None:
            link_title = str(link_title)

        return link_title

    def parse_target_media_type(self):
        """Parse link's target media type.

        :returns: string value of link's target media type or None.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            link_target_media_type = self._data["type"]
        except TypeError as error:
            logger.error("Failed to get target media type from link data")
            raise ValueError("Failed to get target media type from link data") from error
        except KeyError:
            link_target_media_type = None

        if link_target_media_type is not None:
            link_target_media_type = str(link_target_media_type)

        return link_target_media_type


class EmbeddedLinkParser:
    """Class to parse a single embedded link."""

    def __init__(self, data):
        self._data = data

    def parse(self):
        """Parse the embedded link.

        :returns: :class:`EmbeddedLink <lila.core.link.Link>`.
        """
        return EmbeddedLink(
            relations=self.parse_relations(),
            classes=self.parse_classes(),
            target=self.parse_target(),
            title=self.parse_title(),
            target_media_type=self.parse_target_media_type(),
            )

    def parse_relations(self):
        """Parse relations of the embedded link.

        :returns: list of string relations of the embedded link.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            embedded_link_relations = self._data["rel"]
        except TypeError as error:
            logger.error("Failed to get relations from data of embedded link")
            raise ValueError("Failed to get relations from data of embedded link") from error
        except KeyError as error:
            logger.error("Data of embedded link do not have required 'rel' key")
            raise ValueError("Data of embedded link do not have required 'rel' key") from error

        try:
            embedded_link_relations = tuple(str(relation) for relation in embedded_link_relations)
        except TypeError as error:
            logger.error("Failed to iterate over relations from data of embedded link")
            raise ValueError(
                "Failed to iterate over relations from data of embedded link",
                ) from error

        return embedded_link_relations

    def parse_classes(self):
        """Parse classes of the embedded link.

        :returns: list with string names of classes of the embedded link.
        """
        logger = logging.getLogger(__name__)

        try:
            embedded_link_classes = self._data["class"]
        except TypeError as error:
            logger.error("Failed to get classes from data of embedded link")
            raise ValueError("Failed to get classes from data of embedded link") from error
        except KeyError:
            embedded_link_classes = ()

        try:
            embedded_link_classes = tuple(str(class_) for class_ in embedded_link_classes)
        except TypeError as error:
            logger.error("Failed to iterate over classes from data of embedded link")
            raise ValueError("Failed to iterate over classes from data of embedded link") from error

        return embedded_link_classes

    def parse_target(self):
        """Parse target of the embedded link.

        :returns: string target of the embedded link.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            embedded_link_target = self._data["href"]
        except TypeError as error:
            logger.error("Failed to get target from data of embedded link")
            raise ValueError("Failed to get target from data of embedded link") from error
        except KeyError as error:
            logger.error("Data of embedded link do not have required 'href' key")
            raise ValueError("Data of embedded link do not have required 'href' key") from error

        return str(embedded_link_target)

    def parse_title(self):
        """Parse title of the embedded link.

        :returns: string title of the embedded link or None.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            embedded_link_title = self._data["title"]
        except TypeError as error:
            logger.error("Failed to get title from data of embedded link")
            raise ValueError("Failed to get title from data of embedded link") from error
        except KeyError:
            embedded_link_title = None

        if embedded_link_title is not None:
            embedded_link_title = str(embedded_link_title)

        return embedded_link_title

    def parse_target_media_type(self):
        """Parse target media type of the embedded link.

        :returns: string value of target media type of the embedded link or None.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            embedded_link_target_media_type = self._data["type"]
        except TypeError as error:
            logger.error("Failed to get target media type from data of embedded link")
            raise ValueError(
                "Failed to get target media type from data of embedded link",
                ) from error
        except KeyError:
            embedded_link_target_media_type = None

        if embedded_link_target_media_type is not None:
            embedded_link_target_media_type = str(embedded_link_target_media_type)

        return embedded_link_target_media_type
