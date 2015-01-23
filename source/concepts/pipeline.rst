Analytics pipeline
==================

This section illustrates how to use the analytics pipeline to extract insight from
your raw sensor data.


Pipeline overview
-----------------

A pipeline defines a sequence of operations that are applied to a stream of data
from a sensor, resulting in a new output stream of data points.
Pipeline operations are typically mathematical functions, such as daily max/min
rollups.

Pipelines operate individually on each sensor in a selector. Therefore, for a basic
pipeline, there's a one-to-one correspondence between input sensor streams and
output streams.

.. todo:: diagram of where a basic pipeline fits in a read query

TempoIQ supports many pipeline operations as part of the client libraries.
See the Analytics API reference for details.


Using pipelines in a read query
-------------------------------

Analyzing historical sensor data with a pipeline is straightforward: simply
supply a pipeline object as an argument in the :method:`read` call.

Example
~~~~~~~

Thermostat devices record data once a minute, but it is unnecessary to have this
level of granularity in a week-long graph. You can use the rollup pipeline operation
to downsample the raw data streams to hourly averages:

.. snippet-display:: pipeline-concept


Chaining pipeline operations
----------------------------

An analytics pipeline can contain several operations in sequence. Each operation takes
the result of the previous operation as its input. This enables you to compose complex
analysis functions out of simple component operations.
