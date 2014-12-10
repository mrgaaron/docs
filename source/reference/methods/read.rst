Reading Historical Data
=======================

Read data
---------

.. method:: read(search, read, [pipeline])

   Reads data points from one or more devices and sensors.

   :endpoint: ``GET /v2/read/``

   :cursored: Yes

   :arg Search search:

      Required. Selects the sensors to read

   :arg ReadAction read:

      Required. Parameters for specifying the time range of data to read

   :arg Pipeline pipeline:

      Optional. A sequence of operations to transform the raw sensor data

   :returns:

      :class:`ReadResponse` with the requested data.


   **Example**

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



Single point
------------

.. method:: single(search, function, timestamp, [pipeline])

   Returns a single data point for each of a selection of sensors. The function
   parameter indicates how to search for the point. The following functions
   are supported:

   - ``latest`` - Return the data point in the series with the latest timestamp,
     even if it is in the future.

   - ``earliest`` - Return the point in the series with the earliest timestamp.

   - ``exact`` - Return the point with the exact same timestamp as the provided
     *timestamp* argument, if one exists.

   - ``before`` - Return the point closest to the provided *timestamp* argument,
     searching only backwards in time.

   - ``after`` - Return the point closest to the provided *timestamp* argument,
     searching only forwards in time.

   - ``nearest`` - Return the point closest to the provided *timestamp* argument,
     searching both forwards and backwards.


   :endpoint: ``GET /v2/single``

   :arg Search search:

      Required. Selects the sensors to read

   :arg String function:

      Required. One of: ``earliest``, ``latest``, ``before``, ``after``,
      ``nearest``, ``exact``.

   :arg DateTime timestamp:

      Required for all functions except ``earliest`` and ``latest``.

   :arg Pipeline pipeline:

      Optional. A sequence of operations to transform the raw sensor data

   :returns:

      :class:`ReadResponse` with the requested data.


   **Example:**

   .. snippet-display:: single-point