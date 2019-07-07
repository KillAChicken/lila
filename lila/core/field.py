"""Module to work with Siren actions."""

import enum

import lila.core.common as common


class InputType(enum.Enum):
    """Enumerable with supported input types."""
    HIDDEN = "hidden"
    TEXT = "text"
    SEARCH = "search"
    PHONE = "tel"
    URL = "url"
    EMAIL = "email"
    PASSWORD = "password"
    DATETIME = "datetime"
    DATE = "date"
    MONTH = "month"
    WEEK = "week"
    TIME = "time"
    DATETIME_LOCAL = "datetime-local"
    NUMBER = "number"
    RANGE = "range"
    COLOR = "color"
    CHECKBOX = "ratio"
    FILE = "file"
    SUBMIT = "submit"
    IMAGE = "image"
    RESET = "reset"
    BUTTON = "button"


class Field:
    """Class to work with Siren fields."""

    def __init__(self, name, classes=(), input_type=InputType.TEXT, value=None, title=None):
        # pylint: disable=too-many-arguments
        self._name = str(name)
        self._classes = common.adjust_classes(classes)

        if not isinstance(input_type, InputType):
            raise ValueError("Unsupported input type '{0}'".format(input_type))
        self._input_type = input_type

        if value is not None:
            value = str(value)
        self._value = value

        if title is not None:
            title = str(title)
        self._title = title

    @property
    def name(self):
        """Name of the field."""
        return self._name

    @property
    def classes(self):
        """Classes of the field."""
        return tuple(self._classes)

    @property
    def input_type(self):
        """Input type of the field."""
        return self._input_type

    @property
    def value(self):
        """Value assigned to the field."""
        return self._value

    @property
    def title(self):
        """Descriptive title for the field."""
        return self._title
