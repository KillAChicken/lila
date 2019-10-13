"""Module with base class for all Siren components."""

import lila.core.common as common


class Component:
    """Class for base Siren component."""

    def __init__(self, classes=(), title=None):
        self._classes = common.adjust_classes(classes)

        if title is not None:
            title = str(title)
        self._title = title

    @property
    def classes(self):
        """Classes of the component."""
        return tuple(self._classes)

    @property
    def title(self):
        """Descriptive title for the component."""
        return self._title
