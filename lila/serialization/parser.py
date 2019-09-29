"""Module with base parser for Siren objects."""


class Parser:
    """Class to parse serialized Siren objects."""

    def parse_field(self, data):
        """Parse serialized Siren field.

        :param data: serialized field.
        :returns: Siren Field.
        """
        raise NotImplementedError("Parser does not support siren fields")

    def parse_action(self, data):
        """Parse serialized Siren action.

        :param data: serialized action.
        :returns: Siren Action.
        """
        raise NotImplementedError("Parser does not support siren actions")

    def parse_link(self, data):
        """Parse serialized Siren link.

        :param data: serialized link.
        :returns: Siren Link.
        """
        raise NotImplementedError("Parser does not support siren links")

    def parse_embedded_link(self, data):
        """Parse serialized embedded Siren link.

        :param data: serialized embedded link.
        :returns: Siren EmbeddedLink.
        """
        raise NotImplementedError("Parser does not support embedded siren links")

    def parse_entity(self, data):
        """Parse serialized Siren entity.

        :param data: serialized entity.
        :returns: Siren Entity.
        """
        raise NotImplementedError("Parser does not support siren entities")

    def parse_embedded_representation(self, data):
        """Parse serialized Siren embedded representation.

        :param data: serialized embedded representation.
        :returns: Siren EmbeddedRepresentation.
        """
        raise NotImplementedError("Parser does not support siren embedded representations")
