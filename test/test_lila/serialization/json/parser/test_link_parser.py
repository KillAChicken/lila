"""Test cases for a parser class for link data."""

import pytest

from lila.core.link import Link
from lila.serialization.json.link import LinkParser


def test_unobtainable_relations():
    """Test that ValueError is raised if relations can't be retrieved from link data.

    1. Create a link parser for a non-subscriptable object.
    2. Try to call parse_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkParser(data=None).parse_relations()

    assert error_info.value.args[0] == "Failed to get relations from link data", "Wrong error"


def test_missing_relations():
    """Test that ValueError is raised if link data don't contain 'rel' key.

    1. Create a link parser for a dictionary without relations.
    2. Try to call parse_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkParser(data={}).parse_relations()

    assert error_info.value.args[0] == "Link data do not have required 'rel' key", "Wrong error"


def test_non_iterable_relations():
    """Test that ValueError is raised if link data has a non-iterable object for relations.

    1. Create a link parser for a dictionary with non-iterable relations.
    2. Try to call parse_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkParser(data={"rel": None}).parse_relations()

    assert error_info.value.args[0] == "Failed to iterate over relations from link data", (
        "Wrong error"
        )


@pytest.mark.parametrize(
    argnames="relations,expected_relations",
    argvalues=[
        ([], ()),
        (["link relation"], ("link relation", )),
        (
            ["first link relation", "second link relation"],
            ("first link relation", "second link relation"),
            ),
        (("first", None, [1, 2]), ("first", "None", "[1, 2]")),
        ],
    ids=[
        "Empty list",
        "Single relation",
        "Multiple relations",
        "Non-string relations",
        ],
    )
def test_relations(relations, expected_relations):
    """Test that relations are properly parsed.

    1. Create a link parser for a dictionary with specific relations.
    2. Parse relations.
    3. Check the parsed classes.
    """
    actual_relations = LinkParser(data={"rel": relations}).parse_relations()
    assert actual_relations == expected_relations, "Wrong relations"


def test_unobtainable_classes():
    """Test that ValueError is raised if classes can't be retrieved from link data.

    1. Create a link parser for a non-subscriptable object.
    2. Try to call parse_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkParser(data=None).parse_classes()

    assert error_info.value.args[0] == "Failed to get classes from link data", "Wrong error"


def test_non_iterable_classes():
    """Test that ValueError is raised if link data has a non-iterable object for classes.

    1. Create a link parser for a dictionary with non-iterable classes.
    2. Try to call parse_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkParser(data={"class": None}).parse_classes()

    assert error_info.value.args[0] == "Failed to iterate over classes from link data", (
        "Wrong error"
        )


def test_missing_classes():
    """Test that empty tuple is returned if link data don't have 'class' key.

    1. Create a link parser for a dictionary without classes.
    2. Parse classes.
    3. Check that empty tuple is returned.
    """
    actual_classes = LinkParser(data={}).parse_classes()
    assert actual_classes == (), "Wrong classes"


@pytest.mark.parametrize(
    argnames="classes,expected_classes",
    argvalues=[
        ([], ()),
        (["link class"], ("link class", )),
        (["first link class", "second link class"], ("first link class", "second link class")),
        (("first", None, [1, 2]), ("first", "None", "[1, 2]")),
        ],
    ids=[
        "Empty list",
        "Single class",
        "Multiple classes",
        "Non-string classes",
        ],
    )
def test_classes(classes, expected_classes):
    """Test that classes are properly parsed.

    1. Create a link parser for a dictionary with specific classes.
    2. Parse classes.
    3. Check the parsed classes.
    """
    actual_classes = LinkParser(data={"class": classes}).parse_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_unobtainable_target():
    """Test that ValueError is raised if target can't be retrieved from link data.

    1. Create a link parser for a non-subscriptable object.
    2. Try to call parse_target method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkParser(data=None).parse_target()

    assert error_info.value.args[0] == "Failed to get target from link data", "Wrong error"


def test_missing_target():
    """Test that ValueError is raised if link data don't contain 'href' key.

    1. Create a link parser for a dictionary without target.
    2. Try to call parse_target method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkParser(data={}).parse_target()

    assert error_info.value.args[0] == "Link data do not have required 'href' key", "Wrong error"


@pytest.mark.parametrize(
    argnames="target,expected_target",
    argvalues=[
        ("/target", "/target"),
        ("", ""),
        (None, "None"),
        ],
    ids=[
        "Simple",
        "Empty",
        "None",
        ],
    )
def test_target(target, expected_target):
    """Test that target is properly parsed.

    1. Create a link parser for dictionary with specific target.
    2. Parse a target.
    3. Check the parsed target.
    """
    actual_target = LinkParser(data={"href": target}).parse_target()
    assert actual_target == expected_target, "Wrong target"


def test_unobtainable_title():
    """Test that ValueError is raised if title can't be retrieved from link data.

    1. Create a link parser for a non-subscriptable object.
    2. Try to call parse_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkParser(data=None).parse_title()

    assert error_info.value.args[0] == "Failed to get title from link data", "Wrong error"


def test_missing_title():
    """Test that None is returned if link data don't have 'title' key.

    1. Create a link parser for a dictionary without title.
    2. Parse title.
    3. Check that None is returned.
    """
    actual_title = LinkParser(data={}).parse_title()
    assert actual_title is None, "Wrong title"


@pytest.mark.parametrize(
    argnames="title,expected_title",
    argvalues=[
        ("link title", "link title"),
        (u"Заголовок на русском", u"Заголовок на русском"),
        ("", ""),
        (None, None),
        ],
    ids=[
        "Simple",
        "Unicode",
        "Empty",
        "None",
        ],
    )
def test_title(title, expected_title):
    """Test that title is properly parsed.

    1. Create a link parser for dictionary with specific title.
    2. Parse a title.
    3. Check the parsed title.
    """
    actual_title = LinkParser(data={"title": title}).parse_title()
    assert actual_title == expected_title, "Wrong title"


def test_unobtainable_target_media_type():
    """Test that ValueError is raised if target media type can't be retrieved from link data.

    1. Create a link parser for a non-subscriptable object.
    2. Try to call parse_target_media_type method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        LinkParser(data=None).parse_target_media_type()

    assert error_info.value.args[0] == "Failed to get target media type from link data", (
        "Wrong error"
        )


def test_missing_target_media_type():
    """Test that None is returned if link data don't have 'type' key.

    1. Create a link parser for a dictionary without target media type.
    2. Parse target media type.
    3. Check that None is returned.
    """
    actual_target_media_type = LinkParser(data={}).parse_target_media_type()
    assert actual_target_media_type is None, "Wrong target media type"


@pytest.mark.parametrize(
    argnames="target_media_type",
    argvalues=["application/json", None],
    ids=["Simple", "None"],
    )
def test_target_media_type(target_media_type):
    """Test that target media type is properly parsed.

    1. Create a link parser for dictionary with specific target media type.
    2. Parse a target media type.
    3. Check the parsed target media type.
    """
    parser = LinkParser(data={"type": target_media_type})
    actual_target_media_type = parser.parse_target_media_type()
    assert actual_target_media_type == target_media_type, "Wrong target media type"


def test_parse(component_validator):
    """Test that link data is properly parsed.

    1. Create a link.
    2. Create a link parser.
    3. Replace parser methods so that they return predefined data.
    4. Parse the link.
    5. Check the parsed data.
    """
    link = Link(
        relations=("parsed relation 1", "parsed relation 2"),
        classes=("parsed class 1", "parsed class 2"),
        title="parsed title",
        target="/parsed/target",
        target_media_type="application/parsed+media+type",
        )

    parser = LinkParser(data={})
    parser.parse_relations = lambda: link.relations
    parser.parse_classes = lambda: link.classes
    parser.parse_target = lambda: link.target
    parser.parse_title = lambda: link.title
    parser.parse_target_media_type = lambda: link.target_media_type

    actual_link = parser.parse()
    component_validator.validate_link(actual_link, link)
