"""Module to work with Siren links."""

import lila.core.common as common


class Link:
    """Class to work with Siren link."""

    def __init__(self, relations, target, classes=(), title=None, target_media_type=None):
        # pylint: disable=too-many-arguments
        self._relations = common.adjust_relations(relations)
        self._target = str(target)
        self._classes = common.adjust_classes(classes)

        if title is not None:
            title = str(title)
        self._title = title

        if target_media_type is not None:
            target_media_type = str(target_media_type)
        self._target_media_type = target_media_type

    @property
    def relations(self):
        """Relationships between the link and entity."""
        return tuple(self._relations)

    @property
    def target(self):
        """Target of the link."""
        return self._target

    @property
    def classes(self):
        """Classes of the link."""
        return tuple(self._classes)

    @property
    def title(self):
        """Descriptive title for the link."""
        return self._title

    @property
    def target_media_type(self):
        """Media type of the target resource."""
        return self._target_media_type
