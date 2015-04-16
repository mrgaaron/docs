Collect your Data
===================

.. contents::
   :local:
   :depth: 1

.. image:: /images/datapoint_model.png

Every sensor stores its data as a time series of data points. A data point consists
of a timestamp and a value. To write a single data point, specify the sensor to
write to (device key+sensor key), and the data point to write. 

Write requests are simply lists of data points to write to one or more sensors.
Some libraries may implement convenience methods for special cases, such as
writing values for many sensors at the same timestamp.


Properties of sensor data
-------------------------

TempoIQ's write APIs are designed to be as flexible and easy-to-use as possible.
A few notes to help you make the most of them:

* A sensor can only have one value for a given timestamp. If you write a data
  point for the same timestamp as an existing point, the new value will overwrite
  the old one.
* A sensor's data points are allowed to be written out of order.

Writing data
------------

.. method:: writeData(data)

   :endpoint: ``POST /v2/write/``

   :arg WriteRequest data: Data points to write

   :returns: Nothing

Writes data points to one or more devices and sensors.

If a sensor already has a DataPoint at a given timestamp, writing a new
DataPoint with the same timestamp overwrites the old DataPoint's
value. This means that writes are idempotent, in other words, repeatedly
writing the same data to a sensor does not change what's stored. This
can often simplify your application's write logic, because there's
no risk of data corruption if you happen to write data multiple times.

Example
~~~~~~~

.. snippet-display:: write-data


Errors
~~~~~~

If you attempt to write an invalid DataPoint, for instance, not sending
a number as the value, a MultiStatus will be returned
indicating which Devices succeeded and which failed in writing.


Deleting data
-------------

.. method:: deleteDataPoints(device, sensor, start, stop)

   :endpoint: ``DELETE /v2/devices/:devicekey/sensors/:sensorkey/datapoints``

   Delete a range of data points for a given sensor.

   :arg DateTime start: Beginning of time range to delete (inclusive)
   :arg DateTime stop: End of time range to delete (exclusive)

   :returns: The number of data points that were deleted


.. snippet-display:: delete-data
