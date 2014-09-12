=================
ValueDescriptor
=================

.. class:: ValueDescriptor

A description of a value to match as part of a selector.

In the device search
``{ "device": { "key": "testdev23" } }``\ ,
the string "testdev23" is a ValueDescriptor. It indicates that the
device key must exactly match that string.


Literal values
--------------

The example above illustrates a literal ValueDescriptor. It is the simplest
and most commonly used ValueDescriptor. In order for an object to be included
in the search results,
its value must exactly match the literal value that you provide.

*in*
----

In order for an object to be included in the search results, its corresponding
value must match one of a list of values that you provide. This is
analogous to a SQL *IN* condition.

Example
~~~~~~~

Selects devices where the "version" attribute is either "v1", "v2", or "v2.2"::

    {
      "device": {
        "attributes": {
          "version": {
            "in": ["v1", "v2", "v2.2"]
          }
        }
      }
    }
