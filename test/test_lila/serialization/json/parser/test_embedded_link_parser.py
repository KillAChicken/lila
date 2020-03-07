"""Test cases for a parser class for data of embedded link."""

import pytest

from lila.core.link import EmbeddedLink
from lila.serialization.json.link import EmbeddedLinkParser


def test_unobtainable_relations():
    """Test that ValueError is raised if relations can't be retrieved from data of embedded link.

    1. Create an embedded link parser for a non-subscriptable object.
    2. Try to call parse_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkParser(data=None).parse_relations()

    assert error_info.value.args[0] == "Failed to get relations from data of the embedded link", (
        "Wrong error"
        )


def test_missing_relations():
    """Test that ValueError is raised if data of embedded link don't contain 'rel' key.

    1. Create an embedded link parser for a dictionary without relations.
    2. Try to call parse_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkParser(data={}).parse_relations()

    assert error_info.value.args[0] == "Data of the embedded link do not have required 'rel' key", (
        "Wrong error"
        )


def test_non_iterable_relations():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if data of embedded link has a non-iterable object for relations.

    1. Create an embedded link parser for a dictionary with non-iterable relations.
    2. Try to call parse_relations method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkParser(data={"rel": None}).parse_relations()

    expected_message = "Failed to iterate over relations from data of the embedded link"
    assert error_info.value.args[0] == expected_message, "Wrong error"


@pytest.mark.parametrize(
    argnames="relations,expected_relations",
    argvalues=[
        (["embedded link relation"], ("embedded link relation", )),
        (
            ["first embedded link relation", "second embedded link relation"],
            ("first embedded link relation", "second embedded link relation"),
            ),
        (("first", None, [1, 2]), ("first", "None", "[1, 2]")),
        ],
    ids=[
        "Single relation",
        "Multiple relations",
        "Non-string relations",
        ],
    )
def test_relations(relations, expected_relations):
    """Test that relations are properly parsed.

    1. Create an embedded link parser for a dictionary with specific relations.
    2. Parse relations.
    3. Check the parsed classes.
    """
    actual_relations = EmbeddedLinkParser(data={"rel": relations}).parse_relations()
    assert actual_relations == expected_relations, "Wrong relations"


def test_unobtainable_classes():
    """Test that ValueError is raised if classes can't be retrieved from data of embedded link.

    1. Create an embedded link parser for a non-subscriptable object.
    2. Try to call parse_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkParser(data=None).parse_classes()

    assert error_info.value.args[0] == "Failed to get classes from data of the embedded link", (
        "Wrong error"
        )


def test_non_iterable_classes():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if data of embedded link has a non-iterable object for classes.

    1. Create an embedded link parser for a dictionary with non-iterable classes.
    2. Try to call parse_classes method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: enable=line-too-long
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkParser(data={"class": None}).parse_classes()

    expected_message = "Failed to iterate over classes from data of the embedded link"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_missing_classes():
    """Test that empty tuple is returned if data of embedded link don't have 'class' key.

    1. Create an embedded link parser for a dictionary without classes.
    2. Parse classes.
    3. Check that empty tuple is returned.
    """
    actual_classes = EmbeddedLinkParser(data={}).parse_classes()
    assert actual_classes == (), "Wrong classes"


@pytest.mark.parametrize(
    argnames="classes,expected_classes",
    argvalues=[
        ([], ()),
        (["embedded link class"], ("embedded link class", )),
        (
            ["first embedded link class", "second embedded link class"],
            ("first embedded link class", "second embedded link class")),
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

    1. Create an embedded link parser for a dictionary with specific classes.
    2. Parse classes.
    3. Check the parsed classes.
    """
    actual_classes = EmbeddedLinkParser(data={"class": classes}).parse_classes()
    assert actual_classes == expected_classes, "Wrong classes"


def test_unobtainable_target():
    """Test that ValueError is raised if target can't be retrieved from data of embedded link.

    1. Create an embedded link parser for a non-subscriptable object.
    2. Try to call parse_target method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkParser(data=None).parse_target()

    assert error_info.value.args[0] == "Failed to get target from data of the embedded link", (
        "Wrong error"
        )


def test_missing_target():
    """Test that ValueError is raised if data of embedded link don't contain 'href' key.

    1. Create an embedded link parser for a dictionary without target.
    2. Try to call parse_target method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkParser(data={}).parse_target()

    expected_message = "Data of the embedded link do not have required 'href' key"
    assert error_info.value.args[0] == expected_message, "Wrong error"


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

    1. Create an embedded link parser for dictionary with specific target.
    2. Parse a target.
    3. Check the parsed target.
    """
    actual_target = EmbeddedLinkParser(data={"href": target}).parse_target()
    assert actual_target == expected_target, "Wrong target"


def test_unobtainable_title():
    """Test that ValueError is raised if title can't be retrieved from data of embedded link.

    1. Create an embedded link parser for a non-subscriptable object.
    2. Try to call parse_title method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkParser(data=None).parse_title()

    assert error_info.value.args[0] == "Failed to get title from data of the embedded link", (
        "Wrong error"
        )


def test_missing_title():
    """Test that None is returned if data of embedded link don't have 'title' key.

    1. Create an embedded link parser for a dictionary without title.
    2. Parse title.
    3. Check that None is returned.
    """
    actual_title = EmbeddedLinkParser(data={}).parse_title()
    assert actual_title is None, "Wrong title"


@pytest.mark.parametrize(
    argnames="title,expected_title",
    argvalues=[
        ("embedded link title", "embedded link title"),
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

    1. Create an embedded link parser for dictionary with specific title.
    2. Parse a title.
    3. Check the parsed title.
    """
    actual_title = EmbeddedLinkParser(data={"title": title}).parse_title()
    assert actual_title == expected_title, "Wrong title"


def test_unobtainable_target_media_type():
    # pylint: disable=line-too-long
    """Test that ValueError is raised if target media type can't be retrieved from data of embedded link.

    1. Create an embedded link parser for a non-subscriptable object.
    2. Try to call parse_target_media_type method.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    # pylint: disable=line-too-long
    with pytest.raises(ValueError) as error_info:
        EmbeddedLinkParser(data=None).parse_target_media_type()

    expected_message = "Failed to get target media type from data of the embedded link"
    assert error_info.value.args[0] == expected_message, "Wrong error"


def test_missing_target_media_type():
    """Test that None is returned if data of embedded link don't have 'type' key.

    1. Create an embedded link parser for a dictionary without target media type.
    2. Parse target media type.
    3. Check that None is returned.
    """
    actual_target_media_type = EmbeddedLinkParser(data={}).parse_target_media_type()
    assert actual_target_media_type is None, "Wrong target media type"


@pytest.mark.parametrize(
    argnames="target_media_type",
    argvalues=["application/json", None],
    ids=["Simple", "None"],
    )
def test_target_media_type(target_media_type):
    """Test that target media type is properly parsed.

    1. Create an embedded link parser for dictionary with specific target media type.
    2. Parse a target media type.
    3. Check the parsed target media type.
    """
    parser = EmbeddedLinkParser(data={"type": target_media_type})
    actual_target_media_type = parser.parse_target_media_type()
    assert actual_target_media_type == target_media_type, "Wrong target media type"


def test_parse():
    """Test that data of embedded link is properly parsed.

    1. Create an embedded link.
    2. Create an embedded link parser.
    3. Replace parser methods so that they return predefined data.
    4. Parse the embedded link.
    5. Check the parsed data.
    """
    embedded_link = EmbeddedLink(
        relations=("parsed relation 1", "parsed relation 2"),
        classes=("parsed class 1", "parsed class 2"),
        title="parsed title",
        target="/parsed/target",
        target_media_type="application/parsed+media+type",
        )

    parser = EmbeddedLinkParser(data={})
    parser.parse_relations = lambda: embedded_link.relations
    parser.parse_classes = lambda: embedded_link.classes
    parser.parse_target = lambda: embedded_link.target
    parser.parse_title = lambda: embedded_link.title
    parser.parse_target_media_type = lambda: embedded_link.target_media_type

    actual_embedded_link = parser.parse()
    assert actual_embedded_link.relations == embedded_link.relations, (
        "Relations of embedded link are not properly parsed"
        )
    assert actual_embedded_link.classes == embedded_link.classes, (
        "Classes of embedded link are not properly parsed"
        )
    assert actual_embedded_link.target == embedded_link.target, (
        "Target of embedded link is not properly parsed"
        )
    assert actual_embedded_link.title == embedded_link.title, (
        "Title of embedded link is not properly parsed"
        )
    assert actual_embedded_link.target_media_type == embedded_link.target_media_type, (
        "Target media type of embedded link is not properly parsed"
        )
