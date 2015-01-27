===============
Getting Started
===============

This guide introduces the basic TempoIQ API operations you will use to build
your sensor application. You can follow along with one of our 
:doc:`official libraries </sdk/index>`, or via the command line with ``curl``.

Connecting to your backend
--------------------------

Regardless of how you're communicating with your backend, the first step is 
to find your host and :class:`Credentials`. They can be found at the 
bottom of the `development console <https://developers.tempoiq.com/console/>`_:

.. image:: /images/console-credentials.png

When using a library, you instantiate a client object with your host, key, and 
secret. When interacting directly via HTTP, the credentials must be included with
every request.

.. snippet-display:: create-client


Creating a device
-----------------

Next, create a device 'thermostat.0' with two sensors: temperature and humidity. 

.. snippet-display:: create-device

In addition to these sensors, you can also add metadata in the form of attributes.
You can query devices based on attributes, allowing you to perform operations on
many devices at once.


Writing sensor data
-------------------

Write data to a sensor in the form of a sequence of :class:`DataPoints <DataPoint>`.
Timestamps can be specified in any time zone, but are converted to UTC for storage.
Timestamps with no timezone are treated as UTC.

A DataPoint's value is a double-precision floating point number.

.. snippet-display:: write-data


Reading raw data
----------------

There are many functions for reading and analyzing sensor data in TempoIQ. One
of the simplest is to read raw data from a selected device over a time range.

.. snippet-display:: read-data-one-device


Next steps
----------

This guide just scratches the surface of TempoIQ's capabilities. From here,
you can learn more about the :doc:`data model </concepts/data-model>` or the
:doc:`analytics pipeline </concepts/pipeline>`. To dive into the details
of the API, check out the :doc:`API reference </reference/index>`.