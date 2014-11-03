===========
ReadRequest
===========

.. class:: ReadRequest

Describes a read operation to perform.

Fields
------

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - search
     - :class:`Search`
     - Required. Selects the sensors to read
   * - read
     - :class:`ReadAction`
     - Required. Parameters for specifying the time range of data to read
   * - pipeline
     - :class:`Pipeline`
     - Optional. A sequence of operations to transform the raw sensor data

Example
--------

Read two days of raw data from temperature sensors on devices in the "foo" region::

    {
      "search": {
        "filters": {
          "devices": {
            "attributes": {
              "region": "foo"
            }
          },
          "sensors": {
            "key": "temperature"
          }
        }
      },
      "read": {
        "start": "2014-09-01T00:00:00Z",
        "stop": "2014-09-03T00:00:00Z"
      }
    }
