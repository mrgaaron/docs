Reading Historical Data
=======================

Read data
---------

.. method:: read(search, read, [pipeline])

   :endpoint: ``GET /v2/read/``

   :cursored: Yes

   Reads data points from one or more devices and sensors.

   :arg Search search:

      Required. Selects the sensors to read

   :arg ReadAction read:

      Required. Parameters for specifying the time range of data to read

   :arg Pipeline pipeline:

      Optional. A sequence of operations to transform the raw sensor data

   :returns:

      :class:`ReadResponse` with the requested data.


Example
~~~~~~~

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


Latest value
------------

.. method:: latest(search, [pipeline])

   :endpoint: ``GET /v2/single``

   Returns the single latest data point for each of a selection of sensors.
   *Latest* in this case means the data point with the highest timestamp, even
   if it is in the future.

   :arg Search search:

      Required. Selects the sensors to read

   :arg Pipeline pipeline:

      Optional. A sequence of operations to transform the raw sensor data

   :returns:

      :class:`ReadResponse` with the requested data.