"""Test cases for Siren embedded Links."""

import pytest

from lila.core.link import EmbeddedLink


DEFAULT_RELATIONS = ("test", )


@pytest.mark.parametrize(
    argnames="relations, expected_relations",
    argvalues=[
        (["items", "values"], ("items", "values")),
    ],
    ids=[
        "Happy path",
    ],
)
def test_relations(relations, expected_relations):
    """Test relations of an embedded link.

    1. Create an embedded link with different relations.
    2. Get relations.
    3. Check the relations.
    """
    link = EmbeddedLink(relations=relations, target="#")
    assert link.relations == expected_relations, "Wrong relations"


def test_invalid_relations():
    """Check that ValueError is raised if invalid relations are passed.

    1. Try to create an embedded link with non-iterable relations.
    2. Check that ValueError is raised.
    """
    with pytest.raises(ValueError):
        EmbeddedLink(relations=None, target="#")


def test_missing_relations():
    """Check that ValueError is raised if relations list is empty.

    1. Try to create an embedded link with empty list of relations.
    2. Check that ValueError is raised.
    3. Check error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLink(relations=[], target="#")

    assert error_info.value.args[0] == "No relations are passed to create an embedded link", (
        "Wrong error message"
        )


@pytest.mark.parametrize(
    argnames="target, expected_target",
    argvalues=[
        ("https://example.com/somepath", "https://example.com/somepath"),
        ("/somepath", "/somepath"),
        ("#some-embedded-link", "#some-embedded-link"),
        (None, "None"),
    ],
    ids=[
        "Absolute",
        "Relative",
        "Anchor",
        "Not string",
    ],
)
def test_target(target, expected_target):
    """Check target of an embedded link.

    1. Create an embedded link with a target.
    2. Get target.
    3. Check the target.
    """
    link = EmbeddedLink(relations=DEFAULT_RELATIONS, target=target)
    assert link.target == expected_target, "Wrong target"


@pytest.mark.parametrize(
    argnames="classes, expected_classes",
    argvalues=[
        (["embedded-link1", "embedded-link2"], ("embedded-link1", "embedded-link2")),
        ([], ()),
    ],
    ids=[
        "Happy path",
        "Empty list",
    ],
)
def test_classes(classes, expected_classes):
    """Check classes of an embedded link.

    1. Create an embedded link with different classes.
    2. Get classes of the link.
    3. Check the classes.
    """
    link = EmbeddedLink(relations=DEFAULT_RELATIONS, target="#", classes=classes)
    assert link.classes == expected_classes, "Wrong classes"


def test_default_classes():
    """Check default classes of an embedded link.

    1. Create an embedded link without specifying classes.
    2. Check classes of the link.
    """
    link = EmbeddedLink(relations=DEFAULT_RELATIONS, target="#")
    assert link.classes == (), "Wrong classes"


def test_invalid_classes():
    """Check that ValueError is raised if invalid classes are passed.

    1. Try to create an embedded link with non-iterable classes.
    2. Check that ValueError is raised.
    """
    with pytest.raises(ValueError):
        EmbeddedLink(relations=DEFAULT_RELATIONS, target="#", classes=1)


@pytest.mark.parametrize(
    argnames="title, expected_title",
    argvalues=[
        ("string embedded link", "string embedded link"),
        (None, None),
        (1234, "1234"),
    ],
    ids=[
        "String",
        "None",
        "Integer",
    ],
)
def test_title(title, expected_title):
    """Check title of an embedded link.

    1. Create an embedded link with different titles.
    2. Get title of the link.
    3. Check the title.
    """
    link = EmbeddedLink(relations=DEFAULT_RELATIONS, target="#", title=title)
    assert link.title == expected_title, "Wrong title"


def test_default_title():
    """Check default title of an embedded link.

    1. Create an embedded link without specifying a title.
    2. Check the title of the link.
    """
    link = EmbeddedLink(relations=DEFAULT_RELATIONS, target="#")
    assert link.title is None, "Wrong title"


@pytest.mark.parametrize(
    argnames="target_media_type",
    argvalues=[
        "application/json",
        None,
    ],
    ids=[
        "Specified media type",
        "None",
    ],
)
def test_target_media_type(target_media_type):
    """Check target media type of an embedded link.

    1. Create an embedded link with different media types of its target.
    2. Get target media type.
    3. Check the media type.
    """
    link = EmbeddedLink(
        relations=DEFAULT_RELATIONS,
        target="#",
        target_media_type=target_media_type,
        )
    assert link.target_media_type == target_media_type, "Wrong media type"


def test_default_target_media_type():
    """Check default target media type of an embedded link.

    1. Create an embedded link without specifying media type of the target.
    2. Check the media type of the target of the link.
    """
    link = EmbeddedLink(relations=DEFAULT_RELATIONS, target="#")
    assert link.target_media_type is None, "Wrong media type"
