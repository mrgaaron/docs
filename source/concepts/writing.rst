Writing sensor data
===================

Now that we've covered the basics of the Device and Sensor objects, let's take a
closer look at how to work with actual measured data in TempoIQ.

Every sensor stores its data as a sequence of data points. A data point consists
of a timestamp and a value. To write a single data point, specify the sensor to
write to (device key+sensor key), and the data point to write. A JSON
representation of this data structure would be:

.. code-block:: javascript

    {
      "v1-123456": {  // device key
        "temp1": [    // sensor key
          { "t": "2014-08-20T00:22:30Z", "v": 23.5 }
        ]
      }
    }


Write requests are simply lists of data points to write to one or more sensors.
Some libraries may implement convenience methods for special cases, such as
writing values for many sensors at the same timestamp.

Upserting Data
--------------

TempoIQ allows you to write data to devices without explicitly
creating them. When you write, any devices and sensors that don't
exist will be created with empty attributes, and the datapoints will
be processed like a normal write.

Properties of sensor data
-------------------------

TempoIQ's write APIs are designed to be as flexible and easy-to-use as possible.
A few notes to help you make the most of them:

* A sensor can only have one value for a given timestamp. If you write a data
  point for the same timestamp as an existing point, the new value will overwrite
  the old one.
* A sensor's data points are allowed to be written out of order.
