========
Selector
========

.. class:: Selector

Criteria for selecting objects in a Search.

See: Search

and
---

Select an object if it matches all the provided selectors.

Arguments: list of Selectors

or
---

Select an object if it matches any of the provided selectors.

Arguments: list of Selectors


not
---

Select an object if it does not match the provided selector.

Arguments: Selector


all
---

Select all objects in the environment.

Applies to: Device, Sensor

Arguments: none


key
---

Select an object if its key matches the provided value

Arguments: String


attribute
---------

Select an object based on an attribute.

Arguments: key (String, required); value (String, required)
