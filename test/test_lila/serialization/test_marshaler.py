"""Test cases for base marshaler."""

import pytest

from lila.core.field import Field
from lila.serialization.marshaler import Marshaler


def test_marshal_field():
    """Check that NotImplementedError is raised if marshal_field is called.

    1. Create an instance of Marshaler class.
    2. Try to marshal a field.
    3. Check that NotImplementedError is raised.
    4. Check the error message.
    """
    with pytest.raises(NotImplementedError) as error_info:
        Marshaler().marshal_field(field=Field(name="field"))

    assert error_info.value.args[0] == "Marshaler does not support siren fields"
