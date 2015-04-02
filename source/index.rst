===============
Getting Started
===============

TempoIQ is a cloud service for monitoring, storing, and analyzing sensor data. 

Some key features of TempoIQ include:

* HTTPS API for writing and reading data
* Realtime alerting
* Built-in concept of devices and sensors


Organizing your data
--------------------

TempoIQ is purpose-built for sensor data. What is sensor data? Typically it:

* Comes from a device that may be measuring several related types of data
* Is a physical measurement that varies over time
* Is reported periodically (e.g. once a minute)
* Has context that does not change, such as a building ID or unit of measurement

In TempoIQ, this data is organized into sensors, where each sensor belongs to a 
device:

.. image:: /images/device_model.png

Each sensor stores a sequence of numeric values and the timestamps corresponding to each
value. TempoIQ can then process this data in a variety of ways.

Some examples of devices and sensors you might have in your application:

* Thermostat -> (Temperature, Humidity)
* Solar Inverter -> (DC Power, AC Power, Voltage, Current)

Your raw sensor data might not have an obvious mapping to this model. See our 
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

In addition to a unique key and human-readable name, devices and sensors can have 
attributes. You can use attributes to define properties of devices or sensors, such
as a location, user ID, or measurement unit. Attributes are covered in more detail
in the `data organization guide`.


Data collection
---------------

<Image goes here?>

TempoIQ's data collection APIs let you write your sensor data according to the structure
defined above. Sensor data is a sequence of numeric values over time. This data can 
then be visualized, analyzed, or transformed in TempoIQ.

If your devices have direct access to the internet, they can 
write their data directly to TempoIQ, or you can use a gateway or cloud server
to aggregate and write the data. Either way, the APIs are very flexible, and can 
handle data being written in realtime, or in batches.


Example
~~~~~~~

In the example above, you created a device 'thermostat.6' which has two sensors,
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

