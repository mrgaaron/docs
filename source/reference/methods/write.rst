Writing Data
============

Description
-----------

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

Errors
------

If you attempt to write to a sensor or device that does not exist, or
specify an invalid DataPoint format, a MultiStatus will be returned
indicating which Devices succeeded and which failed in writing.


Deleting data
-------------

.. method:: deleteDataPoints(device, sensor, start, stop)

   Delete a range of data points for a given sensor.

   :endpoint: ``DELETE /v2/devices/:devicekey/sensors/:sensorkey/datapoints``

   :arg DateTime start: Beginning of time range to delete (inclusive)
   :arg DateTime stop: End of time range to delete (exclusive)

   :returns: The number of data points that were deleted
