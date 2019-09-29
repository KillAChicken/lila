"""Test cases for parse_embedded_link method of JSON parser."""

import pytest

from lila.core.link import EmbeddedLink
from lila.serialization.json.parser import JSONParser


def test_invalid_json():
    """Test that ValueError is raised if input data are not a valid JSON object.

    1. Create a json parser.
    2. Try to call parse_embedded_link method with object() as data.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_embedded_link(data=object())

    assert error_info.value.args[0] == "Specified data are not a valid JSON object", "Wrong error"


@pytest.mark.parametrize(
    argnames="relations",
    argvalues=[
        ("relation1", "relation2"),
        ],
    ids=[
        "Simple",
        ],
    )
def test_relations(json_data_factory, relations):
    """Test that relations are properly parsed.

    1. Create a json parser.
    2. Parse an embedded link from a dictionary with specific relations.
    3. Check relations of the parsed embedded link.
    """
    embedded_link_data = json_data_factory.create_embedded_link_data(relations=relations)
    embedded_link = JSONParser().parse_embedded_link(embedded_link_data)

    assert embedded_link.relations == tuple(relations), "Wrong relations"


def test_missing_relations(json_data_factory):
    """Test that ValueError is raised if input data don't contain relations.

    1. Create a json parser.
    2. Try to parse an embedded link from a dictionary without 'rel' key.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    embedded_link_data = json_data_factory.create_embedded_link_data(relations=["relation"])
    embedded_link_data.pop("rel", None)

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_embedded_link(data=embedded_link_data)

    assert error_info.value.args[0] == "Embedded link data do not have required 'rel' key", (
        "Wrong error"
        )


@pytest.mark.parametrize(
    argnames="classes",
    argvalues=[
        ("class1", "class2"),
        (),
        ],
    ids=[
        "Simple",
        "Empty",
        ],
    )
def test_classes(json_data_factory, classes):
    """Test that classes are properly parsed.

    1. Create a json parser.
    2. Parse an embedded link from a dictionary with specific classes.
    3. Check classes of the parsed embedded link.
    """
    embedded_link_data = json_data_factory.create_embedded_link_data(classes=classes)
    embedded_link = JSONParser().parse_embedded_link(embedded_link_data)

    assert embedded_link.classes == tuple(classes), "Wrong classes"


def test_missing_classes(json_data_factory):
    """Test that embedded link can be parsed if classes are not specified.

    1. Create a json parser.
    2. Parse an embedded link from a dictionary without 'class' key.
    3. Check that parsed embedded link has empty list of classes.
    """
    embedded_link_data = json_data_factory.create_embedded_link_data(classes=["class"])
    embedded_link_data.pop("class", None)
    embedded_link = JSONParser().parse_embedded_link(embedded_link_data)

    assert embedded_link.classes == (), "Wrong classes"


@pytest.mark.parametrize(
    argnames="target",
    argvalues=[
        "/simple/target",
        ],
    ids=[
        "Simple",
        ],
    )
def test_target(json_data_factory, target):
    """Test that target is properly parsed.

    1. Create a json parser.
    2. Parse an embedded link from a dictionary with a specific target.
    3. Check name of the parsed embedded link.
    """
    embedded_link_data = json_data_factory.create_embedded_link_data(target=target)
    embedded_link = JSONParser().parse_embedded_link(embedded_link_data)

    assert embedded_link.target == target, "Wrong target"


def test_missing_target(json_data_factory):
    """Test that ValueError is raised if input data don't contain a target.

    1. Create a json parser.
    2. Try to parse an embedded link from a dictionary without 'href' key.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    embedded_link_data = json_data_factory.create_embedded_link_data(target="/target")
    embedded_link_data.pop("href", None)

    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_embedded_link(data=embedded_link_data)

    assert error_info.value.args[0] == "Embedded link data do not have required 'href' key", (
        "Wrong error"
        )


@pytest.mark.parametrize(
    argnames="title",
    argvalues=[
        "simple title",
        u"Заголовок",
        "",
        None,
        ],
    ids=[
        "Simple",
        "Unicode",
        "Empty",
        "None",
        ],
    )
def test_title(json_data_factory, title):
    """Test that title is properly parsed.

    1. Create a json parser.
    2. Parse an embedded link from a dictionary with a specific title.
    3. Check the title of the parsed embedded link.
    """
    embedded_link_data = json_data_factory.create_embedded_link_data(title=title)
    embedded_link = JSONParser().parse_embedded_link(embedded_link_data)

    assert embedded_link.title == title, "Wrong title"


def test_missing_title(json_data_factory):
    """Test that embedded link can be parsed if title is not specified.

    1. Create a json parser.
    2. Parse an embedded link from a dictionary without 'title' key.
    3. Check that parsed embedded link has None as a title.
    """
    embedded_link_data = json_data_factory.create_embedded_link_data(title="title")
    embedded_link_data.pop("title", None)
    embedded_link = JSONParser().parse_embedded_link(embedded_link_data)

    assert embedded_link.title is None, "Wrong title"


@pytest.mark.parametrize(
    argnames="target_media_type",
    argvalues=[
        "application/json",
        None,
        ],
    ids=[
        "Simple",
        "None",
        ],
    )
def test_target_media_type(json_data_factory, target_media_type):
    """Test that target media type is properly parsed.

    1. Create a json parser.
    2. Parse an embedded link from a dictionary with a specific media type of the target.
    3. Check the target media type of the parsed embedded link.
    """
    embedded_link_data = json_data_factory.create_embedded_link_data(
        target_media_type=target_media_type,
        )
    embedded_link = JSONParser().parse_embedded_link(embedded_link_data)

    assert embedded_link.target_media_type == target_media_type, "Wrong target media type"


def test_missing_target_media_type(json_data_factory):
    """Test that embedded link can be parsed if target media type is not specified.

    1. Create a json parser.
    2. Parse an embedded link from a dictionary without 'type' key.
    3. Check that parsed embedded link has None as a target media type.
    """
    embedded_link_data = json_data_factory.create_embedded_link_data(
        target_media_type="target_media_type",
        )
    embedded_link_data.pop("type", None)
    embedded_link = JSONParser().parse_embedded_link(embedded_link_data)

    assert embedded_link.target_media_type is None, "Wrong target media type"


def test_creation_error(json_data_factory):
    """Test that ValueError from EmbeddedLink creation is reraised by parser.

    1. Create a json parser.
    2. Try to parse an embedded link from a dictionary causing ValueError during the creation of
       an instance of EmbeddedLink class.
    3. Check that ValueError is raised.
    4. Check the error message.
    """
    invalid_relations = ()

    embedded_link_data = json_data_factory.create_embedded_link_data(relations=invalid_relations)
    with pytest.raises(ValueError) as error_info:
        JSONParser().parse_embedded_link(embedded_link_data)

    with pytest.raises(ValueError) as expected_error_info:
        EmbeddedLink(relations=invalid_relations, target="/target")

    assert error_info.value.args[0] == expected_error_info.value.args[0], "Wrong error"
