Build your App
===================

Using TempoIQ's analytics APIs, you can read, analyze, and perform complex
calculations with your sensor data.

Basic historical read
---------------------

A basic read operation takes a sensor selector, and a start and end datetime.
It returns streams of data points for the selected sensors over the specified time
range.

.. todo:: schematic diagram of relationship between selectors, streams, sensors, and a read request


Selectors
~~~~~~~~~

A selector defines a set of sensors from your environment by matching
search criteria, such as:

* Device keys
* Device attributes
* Sensor keys
* Sensor attributes

Multiple criteria can be combined using boolean AND and OR operations.

A selector is only valid if it includes both device criteria and sensor criteria.
If you want to select all sensors on a device, or all devices in your environment,
you must use special wildcard statements. See the API reference for the actual syntax.


Streams
~~~~~~~

A stream is an ordered sequence of :class:`DataPoints <DataPoint>`
along with a :class:`StreamHeader` describing the source of the data points.
When you read data from several sensors, TempoIQ returns one stream per sensor,
where each stream's metadata describes the device and sensor that the stream
originated from.


Latest value
------------

Sometimes you just need the latest value for a sensor, not a whole range of historical data points.
The `latest` method is similar to the `read` call, but returns a single data point
for each sensor instead of a stream. There are no 'start' or 'end' parameters, but
the selector parameter acts exactly as in the `read` call.

Example
~~~~~~~
A dashboard application shows the current value for a given thermostat's temperature
and humidity.

.. code-block:: javascript

    sensors = {
                devices: { key: thermostatKey },  // As supplied by user or database lookup
                sensors: "all"
              };

    response = client.latest(sensors);


Analytics Pipeline
------------------

A pipeline defines a sequence of operations that are applied to a stream of data
from a sensor, resulting in a new output stream of data points.
:class:`Pipeline operations <PipelineFunction>` are typically mathematical functions, 
such as daily max/min rollups.

Pipelines operate individually on each sensor in a selector. Therefore, for a basic
pipeline, there's a one-to-one correspondence between input sensor streams and
output streams.

.. todo:: diagram of where a basic pipeline fits in a read query

TempoIQ supports many pipeline operations as part of the client libraries.
See the Analytics API reference for details.


Using pipelines in a read query
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Analyzing historical sensor data with a pipeline is straightforward: simply
supply a pipeline object as an argument in the :method:`read` call. 


Chaining pipeline operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An analytics pipeline can contain several operations in sequence. Each operation takes
the result of the previous operation as its input. This enables you to compose complex
analysis functions out of simple component operations.

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

.. snippet-display:: read-data-one-device

.. only:: dev

   UPCOMING READ API

   Read responses contain two relevant data fields: a list of :class:`StreamHeader` 
   objects and the data from the read itself.  Each stream header represents a 
   one-dimensional set of data points that were included by the given search 
   criteria:

   .. snippet-display:: read-data-streams

   Another way is to bind to a single stream of data contained in the response.  
   The stream must be identified uniquely in the call or an exception will be 
   thrown:

   .. snippet-display:: bind-single-stream

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
