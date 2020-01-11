"""Configuration file for pytest."""

import pytest

from lila.core.link import EmbeddedLink
from lila.core.entity import EmbeddedRepresentation


@pytest.fixture(params=["link", "representation"])
def non_marshalable_sub_entity(request):
    """Non marshalable sub entity."""
    sub_entity = None
    if request.param == "link":

        class _NonMarshallableLink(EmbeddedLink):
            @property
            def classes(self):
                return None

        sub_entity = _NonMarshallableLink(relations=["self"], target="/self")
    elif request.param == "representation":

        class _NonMarshallableRepresentation(EmbeddedRepresentation):
            @property
            def classes(self):
                return None

        sub_entity = _NonMarshallableRepresentation(relations=["self"])

    if sub_entity is None:
        pytest.fail("Unknown sub entity type")

    return sub_entity
