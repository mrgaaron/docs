================
TempoIQ Overview
================

TempoIQ is an analytics backend for sensor data. Any connected device can write
sensor data to TempoIQ via our write APIs. You can then perform historical
analysis of the data through our analytics APIs.

TempoIQ's data model makes it easy to map your real-world sensors to
virtual data streams. A :class:`Device` represents a single physical unit such
as a power meter or vehicle, and each device has one or more :class:`Sensors <Sensor>`
attached. Each sensor corresponds to a single time-varying measurement on the
device, such as voltage or temperature. This model allows for flexible queries
on sensors within a single device, or comparing corresponding sensors across
many devices.

Harness the power of TempoIQ in your application in a few easy steps:

1. :doc:`Model your devices and sensors </concepts/data-model>`
2. :doc:`Write sensor data </concepts/writing>`
3. :doc:`Analyze the data </concepts/reading>`

Code examples
-------------

Here's how to create devices:

.. snippet-display:: create-device


SDKs
----

TempoIQ provides API libraries and example code for most common
languages and frameworks. See the :doc:`SDKs page </sdk/index>` for the
complete list of supported languages.


Transitioning from TempoDB
--------------------------

Are you migrating from TempoDB to TempoIQ? Our
:doc:`migration guide </guides/tempodb-transition>` includes a mapping
of TempoDB functions to TempoIQ, as well as other useful information.


:ref:`genindex`

.. only:: dev

   :doc:`todos`

.. include:: toc-main.rst
