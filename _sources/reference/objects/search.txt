======
Search
======

.. class:: Search

The TempoIQ API uses searches to select a set of objects. Objects can
either be devices or sensors, depending on the specific API call.

Searches are composed from :class:`Selector` objects that define the search
criteria.

When searching for sensors, your search may include selectors on individual
sensors as well as the devices that they belong to.


Example
-------

Select sensors with key "temperature" that are attached to devices in
the "headquarters" building::


    {
      "devices": {
        "attributes": {
          "building": "headquarters"
        }
      },
      "sensors": {
        "key": "temperature"
      }
    }
