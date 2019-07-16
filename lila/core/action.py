"""Module to work with Siren actions."""

import lila.core.common as common
from lila.core.field import Field


class Action:
    """Class to work with Siren actions."""
    _SUPPORTED_METHODS = set(("GET", "PUT", "POST", "DELETE", "PATCH"))

    def __init__(
            self,
            name,
            target,
            classes=(),
            method="GET",
            title=None,
            fields=(),
            encoding_type=None,
        ):
        # pylint: disable=too-many-arguments
        self._name = str(name)
        self._target = str(target)

        self._classes = common.adjust_classes(classes)

        if method not in self._SUPPORTED_METHODS:
            raise ValueError("Method '{0}' is not supported".format(method))
        self._method = method

        if title is not None:
            title = str(title)
        self._title = title

        if any(not isinstance(field, Field) for field in fields):
            raise ValueError("Some of the fields are of incompatible type")
        self._fields = tuple(fields)

        if encoding_type is not None:
            encoding_type = str(encoding_type)
        elif self._fields:
            encoding_type = "application/x-www-form-urlencoded"
        self._encoding_type = encoding_type

    @property
    def name(self):
        """Name of the action."""
        return self._name

    @property
    def target(self):
        """Request target of the action."""
        return self._target

    @property
    def classes(self):
        """Classes of the action."""
        return tuple(self._classes)

    @property
    def method(self):
        """Method of the action."""
        return self._method

    @property
    def title(self):
        """Descriptive title of the action."""
        return self._title

    @property
    def fields(self):
        """Fields to pass to the action."""
        return tuple(self._fields)

    @property
    def encoding_type(self):
        """Type for the request."""
        return self._encoding_type
