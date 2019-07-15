"""Test cases for Siren Links."""

import pytest

from lila.core.link import Link


DEFAULT_RELATIONS = ("self", )


@pytest.mark.parametrize(
    argnames="relations, expected_relations",
    argvalues=[
        (["self", "about"], ("self", "about")),
    ],
    ids=[
        "Happy path",
    ],
)
def test_relations(relations, expected_relations):
    """Test relations of the link.

    1. Create a link with different relations.
    2. Get relations.
    3. Check the relations.
    """
    link = Link(relations=relations, target="#")
    assert link.relations == expected_relations, "Wrong relations"


def test_invalid_relations():
    """Check that ValueError is raised if invalid relations are passed.

    1. Try to create a link with non-iterable relations.
    2. Check that ValueError is raised.
    """
    with pytest.raises(ValueError):
        Link(relations=None, target="#")


@pytest.mark.parametrize(
    argnames="target, expected_target",
    argvalues=[
        ("https://example.com/somepath", "https://example.com/somepath"),
        ("/somepath", "/somepath"),
        ("#some-link", "#some-link"),
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
    """Check target of the link.

    1. Create a link with a target.
    2. Get target.
    3. Check the target.
    """
    link = Link(relations=DEFAULT_RELATIONS, target=target)
    assert link.target == expected_target, "Wrong target"


def test_default_classes():
    """Check default classes of a link.

    1. Create a link without specifying classes.
    2. Check classes of the field.
    """
    link = Link(relations=DEFAULT_RELATIONS, target="#")
    assert link.classes == (), "Wrong classes"


@pytest.mark.parametrize(
    argnames="classes, expected_classes",
    argvalues=[
        (["link-class1", "link-class2"], ("link-class1", "link-class2")),
    ],
    ids=[
        "Happy path",
    ],
)
def test_classes(classes, expected_classes):
    """Check classes of a link.

    1. Create a link with different classes.
    2. Get classes of the link.
    3. Check the classes.
    """
    link = Link(relations=DEFAULT_RELATIONS, target="#", classes=classes)
    assert link.classes == expected_classes, "Wrong classes"


def test_invalid_classes():
    """Check that ValueError is raised if invalid classes are passed.

    1. Try to create a link with non-iterable classes.
    2. Check that ValueError is raised.
    """
    with pytest.raises(ValueError):
        Link(relations=DEFAULT_RELATIONS, target="#", classes=1)


@pytest.mark.parametrize(
    argnames="title, expected_title",
    argvalues=[
        ("string link", "string link"),
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
    """Check title of a link.

    1. Create a link with different titles.
    2. Get title of the link.
    3. Check the title.
    """
    link = Link(relations=DEFAULT_RELATIONS, target="#", title=title)
    assert link.title == expected_title, "Wrong title"


def test_default_title():
    """Check default title of a link.

    1. Create a link without specifying a title.
    2. Check the title of the link.
    """
    link = Link(relations=DEFAULT_RELATIONS, target="#")
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
    """Check target media type of a link.

    1. Create a link with different media types of its target.
    2. Get target media type.
    3. Check the media type.
    """
    link = Link(relations=DEFAULT_RELATIONS, target="#", target_media_type=target_media_type)
    assert link.target_media_type == target_media_type, "Wrong media type"


def test_default_target_media_type():
    """Check default target media type of a link.

    1. Create a link without specifying media type of the target.
    2. Check the media type of the target of the link.
    """
    link = Link(relations=DEFAULT_RELATIONS, target="#")
    assert link.target_media_type is None, "Wrong media type"
