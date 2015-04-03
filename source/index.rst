===============
Getting Started
===============

TempoIQ is a cloud service for monitoring, storing, and analyzing sensor data.

Connect your devices and sensors, and stream in data in realtime.  TempoIQ 
watches all incoming data for anomalies and sends you push alerts (webhook, 
email, etc) right when something happens.  We also store all of your sensor 
data, and provide flexible APIs to look back and do analyses like summaries, 
rollups, aggregations, and interpolations.


Organizing your data
--------------------

You’ve got devices and sensors connected all over the world, measuring things and generating time series data non-stop.  TempoIQ helps you organize your raw data by tagging your devices and sensors.

It’s really easy: each sensor stores a time series of numeric values.  Group sensors together in a device.

.. image:: /images/device_model.png

Some examples of devices and sensors you might have in your application:

* Thermostat -> (Temperature, Humidity)
* Solar Inverter -> (DC Power, AC Power, Voltage, Current)

After you’ve grouped your sensors into devices, you can further organize your 
devices and sensors by tagging them with attributes (key/value pairs).  You 
could add a tag to a device like, “location=home”, or you could add a tag to 
a sensor like “unit=celsius”.

Tags are very flexible, and you can create hierarchies between devices or 
arbitrary grouping.  This becomes very powerful when running queries later.
You could ask a question like, “give me the max temperature in location=home
on an hourly basis for the last week”

Your raw data might not have an obvious mapping to this model. Don’t worry, 
tagging is quite flexible and we’re here to help. See our 
`data organization guide` for a deeper look at how to organize your sensor data.


Example
~~~~~~~

For your first device, create a thermostat with two sensors: temperature and humidity.
If you haven't done so already, 
`create a free trial account <https://developers.tempoiq.com/accounts/trial/>`_.

You can create a device via the `web UI <https://developers.tempoiq.com/devices/create/>`_:

.. image:: /images/create_device.png
   :scale: 50%

Or through the API using one of our libraries.
First you will need to instantiate a client object with
your host, key, and secret, which can be found on the 
`management console <https://developers.tempoiq.com/console/>`_:

.. snippet-display:: create-client

Then, use the client object to create the device:

.. snippet-display:: create-device


Data collection
---------------

.. image:: /images/datapoint_model.png

Sensor data is a time series of numeric values.
Our data collection APIs enable you to stream or batch write this sensor data. 
Then you can visualize, analyze, or transform the data in TempoIQ.

If your devices have direct access to the internet, they can 
write their data directly to TempoIQ, or you can use a gateway or cloud server
to aggregate and write the data. Either way, the APIs are very flexible, and can 
handle data being written in realtime or in batches.


Example
~~~~~~~

In the example above, you created a device 'thermostat.1' which has two sensors,
'temperature' and 'humidity'. Now try writing some data points to these sensors.
Each point consists of a timestamp and a value. It's possible to write multiple
data points to one or more sensors in a single API call:

.. snippet-display:: write-data

Currently, it's not possible to write arbitrary sensor data via the web UI. 
However, we do have a demo where TempoIQ can collect volume data from your 
computer's microphone. Check out the demo `here`.


Building your app
-----------------

Todo

.. snippet-display:: read-data-one-device


Next steps
----------

This guide just scratches the surface of TempoIQ's capabilities. From here,
you can learn more about the :doc:`data model </concepts/data-model>` or the
:doc:`analytics pipeline </concepts/pipeline>`. To dive into the details
of the API, check out the :doc:`API reference </reference/index>`.

Harness the power of TempoIQ in your application in a few easy steps:

1. :doc:`Model your devices and sensors </concepts/data-model>`
2. :doc:`Write sensor data </concepts/writing>`
3. :doc:`Analyze the data </concepts/reading>`


.. only:: dev

   :doc:`todos`

