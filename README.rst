lila
====
.. image:: https://github.com/KillAChicken/lila/workflows/Tests/badge.svg
    :target: https://github.com/KillAChicken/lila/actions?query=workflow%3ATests

Lila is a Python library to work with `Siren <https://github.com/kevinswiber/siren>`_ protocol. It aims to encapsulate most of the requirements of the protocol, so that one can utilize EAFP principle instead of validating incoming and outgoing data.

Installation
============

.. code-block:: text

    $ python -m pip install lila

Documentation
=============
Documentation for the package can be found on the `Wiki <https://github.com/KillAChicken/lila/wiki>`_.

Quickstart
==========
Assume we expect to receive or need to send the following json data:

.. code-block:: python

    entity_data = {
      "class": [ "order" ],
      "properties": { 
          "orderNumber": 42, 
          "itemCount": 3,
          "status": "pending"
      },
      "entities": [
        { 
          "class": [ "items", "collection" ], 
          "rel": [ "http://x.io/rels/order-items" ], 
          "href": "http://api.x.io/orders/42/items"
        },
        {
          "class": [ "info", "customer" ],
          "rel": [ "http://x.io/rels/customer" ], 
          "properties": { 
            "customerId": "pj123",
            "name": "Peter Joseph"
          },
          "links": [
            { "rel": [ "self" ], "href": "http://api.x.io/customers/pj123" }
          ]
        }
      ],
      "actions": [
        {
          "name": "add-item",
          "title": "Add Item",
          "method": "POST",
          "href": "http://api.x.io/orders/42/items",
          "type": "application/x-www-form-urlencoded",
          "fields": [
            { "name": "orderNumber", "type": "hidden", "value": "42" },
            { "name": "productCode", "type": "text" },
            { "name": "quantity", "type": "number" }
          ]
        }
      ],
      "links": [
        { "rel": [ "self" ], "href": "http://api.x.io/orders/42" },
        { "rel": [ "previous" ], "href": "http://api.x.io/orders/41" },
        { "rel": [ "next" ], "href": "http://api.x.io/orders/43" }
      ]
    }

One can parse these data into a python object and access parts of it (client-side):

.. code-block:: python

    from lila.serialization.json.parser import JSONParser

    entity = JSONParser().parse_entity(entity_data)

    assert entity.actions[0].fields[0].value == "42"

Or start with a python object and build this json (server-side):

.. code-block:: python

    from lila.core.field import InputType, Field
    from lila.core.action import Method, Action
    from lila.core.link import Link, EmbeddedLink
    from lila.core.entity import Entity, EmbeddedRepresentation
    from lila.serialization.json.marshaler import JSONMarshaler

    entity = Entity(
        classes=["order"],
        properties={
            "orderNumber": 42, 
            "itemCount": 3,
            "status": "pending",
        },
        entities=[
            EmbeddedLink(
                classes=["items", "collection"],
                relations=["http://x.io/rels/order-items"],
                target="http://api.x.io/orders/42/items",
            ),
            EmbeddedRepresentation(
                classes=["info", "customer"],
                relations=["http://x.io/rels/customer"], 
                properties={ 
                    "customerId": "pj123",
                    "name": "Peter Joseph",
                },
                links=[
                    Link(
                        relations=["self"],
                        target="http://api.x.io/customers/pj123",
                    ),
                ],
            ),
        ],
        actions=[
            Action(
                name="add-item",
                title="Add Item",
                method=Method.POST,
                target="http://api.x.io/orders/42/items",
                media_type="application/x-www-form-urlencoded",
                fields=[
                    Field(
                        name="orderNumber",
                        input_type=InputType.HIDDEN,
                        value="42"
                    ),
                    Field(
                        name="productCode",
                        input_type=InputType.TEXT,
                    ),
                    Field(
                        name="quantity",
                        input_type=InputType.NUMBER,
                    ),
                ]
            )
        ],
        links=[
            Link(
                relations=["self"],
                target="http://api.x.io/orders/42",
            ),
            Link(
                relations=["previous"],
                target="http://api.x.io/orders/41",
            ),
            Link(
                relations=["next"],
                target="http://api.x.io/orders/43",
            ),
        ]
    )

    entity_data = JSONMarshaler().marshal_entity(entity)

    assert entity_data["actions"][0]["fields"][0]["value"] == "42"
