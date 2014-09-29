TempoIQ manual
==============

TempoIQ is an analytics backend for sensor data. Any connected device can write
sensor data to TempoIQ via our write APIs. You can then perform historical
analysis of the data through our analytics APIs. In addition, real-time
monitoring rules can alert you as soon as devices report abnormal sensor data.

TempoIQ's data model makes it easy to map your real-world sensors to
virtual data streams. A :class:`Device` represents a single physical unit such
as a power meter or vehicle, and each device has one or more :class:`Sensors <Sensor>`
attached. Each sensor corresponds to a single time-varying measurement on the
device, such as voltage or temperature. This model allows for flexible queries
on sensors within a single device, or comparing corresponding sensors across
many devices.

Harness the power of TempoIQ in your application in a few easy steps:

* :doc:`Model your devices and sensors </concepts/data-model>`
* :doc:`Write sensor data </concepts/writing>`
* :doc:`Analyze the data </concepts/reading>`
* :doc:`Set up real-time monitoring rules </concepts/monitoring>`

SDKs
----

TempoIQ provides API libraries and example code for most common
languages and frameworks. See the :doc:`/sdk/index` SDKS page



:ref:`genindex`

.. only:: dev

   :ref:`todos`

.. include:: toc-main.rst
