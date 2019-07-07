"""Module with common functions."""

import json


def adjust_classes(classes):
    """Adjust classes to Siren protocol.

    :param classes: iterable with classes.
    :returns: tuple with string names.
    """
    return tuple(str(class_) for class_ in classes)


def adjust_properties(properties):
    """Adjust properties to Siren protocol.

    :param properties: dictionary or iterable with dictionary items.
    :returns: dictionary with strings as values (property names) and json serializable values.
    """
    try:
        properties_dictionary = dict(properties)
    except (TypeError, ValueError) as error:
        raise ValueError("Can't create dictionary from properties") from error

    adjusted_properties = {}
    for name, value in properties_dictionary.items():
        adjusted_name = str(name)
        # ensure that value is a valid JSON object by dumping and loading it.
        try:
            adjusted_value = json.loads(json.dumps(value))
        except Exception:
            error_message = "Unsupported value for property '{name}'".format(name=adjusted_name)
            raise ValueError(error_message)

        adjusted_properties[adjusted_name] = adjusted_value

    return adjusted_properties
