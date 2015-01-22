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

Read responses can be consumed in a number of ways.  The first way is to bind
to a single stream of data contained in the response.  The stream must be 
identified uniquely in the call or an exception will be thrown:

.. snippet-display:: bind-single-stream

Another way is to simply iterate through each of the possible streams, 
consuming data from each in turn:

.. snippet-display:: bind-all-streams

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

      Optional. Only supports the :class:`ConvertTZ` pipeline operation.

   :returns:

      :class:`ReadResponse` with the requested data.


   **Example:**

   Find the data point at or before the given timestamp for the *temperature* sensor
   on *device1*.

   .. snippet-display:: single-point
