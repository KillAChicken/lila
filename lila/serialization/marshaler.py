"""Module with base marshaler for Siren objects."""


class Marshaler:
    """Class to marshal serialized Siren objects."""

    def marshal_field(self, field):
        """Marshal Siren field.

        :param field: Siren Field.
        :returns: serialized field.
        """
        raise NotImplementedError("Marshaler does not support siren fields")
