"""Module with base marshaler for Siren objects."""


class Marshaler:
    """Class to marshal serialized Siren objects."""

    def marshal_field(self, field):
        """Marshal Siren field.

        :param field: Siren Field.
        :returns: serialized field.
        """
        raise NotImplementedError("Marshaler does not support siren fields")

    def marshal_action(self, action):
        """Marshal Siren action.

        :param action: Siren Action.
        :returns: serialized action.
        """
        raise NotImplementedError("Marshaler does not support siren actions")

    def marshal_link(self, link):
        """Marshal Siren link.

        :param link: Siren Link.
        :returns: dictionary with link data.
        """
        raise NotImplementedError("Marshaler does not support siren links")

    def marshal_embedded_link(self, embedded_link):
        """Marshal embedded Siren link.

        :param embedded_link: embedded Siren Link.
        :returns: dictionary with embedded link data.
        """
        raise NotImplementedError("Marshaler does not support embedded siren links")
