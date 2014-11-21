=====================================
Transitioning from TempoDB to TempoIQ
=====================================

.. contents:: :depth: 2


This page covers important differences between TempoDB and TempoIQ, and considerations
when migrating from the legacy TempoDB service.

Feature Comparison
------------------

.. list-table::
    :header-rows: 1
    :widths: 1 1 2

    * - TempoDB function/concept
      - TempoIQ equivalent
      - Notes
    * - `Create series <https://tempo-db.com/docs/api/write/series/create>`_
      - :method:`createDevice`
      - See :ref:`tdb-data-model` below.
    * - `Update series metadata <https://tempo-db.com/docs/api/write/series/update>`_
      - :method:`updateDevice`
      - It is not possible to add/remove sensors once a device is created.
    * - `Get series by key <https://tempo-db.com/docs/api/read/series/get>`_
      - :method:`getDevice`
      -
    * - `List series <https://tempo-db.com/docs/api/read/series/list>`_
      - :method:`findDevices`
      - Enhancements to the interface for selecting devices are described below in
        :ref:`tdb-selector-interface`
    * - `Delete series <https://tempo-db.com/docs/api/delete/series/>`_
      - :method:`deleteDevice`\ , :method:`deleteDevices`
      -
    * - `Write by key <https://tempo-db.com/docs/api/write/datapoints/single>`_
      - :method:`writeData`
      - TempoIQ does not have a specialized method for writing to a single device.
        See :ref:`tdb-write-interface`
    * - `Multi write <https://tempo-db.com/docs/api/write/datapoints/multi>`_
      - :method:`writeData`
      - See :ref:`tdb-write-interface`
    * - `Delete data points <https://tempo-db.com/docs/api/delete/datapoints/>`_
      - :method:`deleteDataPoints`
      -
    * - `Basic reading <https://tempo-db.com/docs/api/read/datapoints/basic>`_
      - :method:`read`
      - TempoIQ does not have a specialized method for reading from a single device.
        See :ref:`tdb-read-interface`
    * - `Multi-series read <https://tempo-db.com/docs/api/read/datapoints/multi-series>`_
      - :method:`read`
      - See :ref:`tdb-read-interface`
    * - Rollups
      - :class:`Rollup`
      -
    * - `Multi-rollups <https://tempo-db.com/docs/api/read/datapoints/multi-rollups>`_
      - :class:`MultiRollup`
      -
    * - `Interpolation <https://tempo-db.com/docs/api/read/datapoints/interpolation>`_
      - :class:`Interpolate`
      -
    * - `Aggregation <https://tempo-db.com/docs/api/read/datapoints/aggregation>`_
      - :class:`Aggregate`
      - Currenly TempoIQ only supports aggregating across sensors within a single device.
        See :ref:`tdb-aggregation`
    * - Time zone adjustment
      - :class:`ConvertTZ`
      -
    * - `Find <https://tempo-db.com/docs/api/read/datapoints/find>`_
      - :class:`Find`
      -
    * - `Summary <https://tempo-db.com/docs/api/read/datapoints/summary>`_
      - :class:`MultiRollup`
      - See :ref:`tdb-summary-endpoint` below
    * - `Single value <https://tempo-db.com/docs/api/read/datapoints/single-value>`_
      - :method:`latest`
      - Not a 100% replacement, see :ref:`tdb-single-value` below


.. _tdb-data-model:

Data Model
----------

TempoDB's concept of a series has been replaced by a two-level hierarchy of
Devices and Sensors. When migrating to TempoIQ, it's important to understand
how to map your series to a corresponding TempoIQ sensor.

Suppose you are currently storing energy meter data in TempoDB, using series
with the following format::

    "series": [
      {
        "key": "meter:12345.region:2A.voltage.",
        "tags": "voltage",
        "attributes": {
          "meter": "12345",
          "region": "2A",
          "status": "active"
        },
      },
      {
        "key": "meter:12345.region:2A.energy.",
        "tags": "energy",
        "attributes": {
          "meter": "12345",
          "region": "2A",
          "status": "active"
        },
      },
      ...
    ]

While your exact format may differ, this example illustrates a few common
conventions in TempoDB:

* Each physical unit (meter) is actually represented as multiple series; in this
  case, one for voltage and one for energy usage.
* A series key includes some or all of the series' metadata (attributes and tags).
* Series metadata describes the source of the data (which meter) as well as the
  type of measurement (voltage vs. usage). Source metadata is replicated across
  all series associated with that source.

In TempoIQ, here's how to represent this meter data as devices and sensors::

    "devices": [
      {
        "key": "meter:12345",
        "attributes": {
          "meter": "12345",
          "region": "2A",
          "status": "active"
        },
        "sensors": [
          {
            "key": "voltage",
            "attributes": {}
          },
          {
            "key": "energy",
            "attributes": {}
          }
        ]
      },
      ...
    ]

In contrast to the TempoDB example above:

* Each physical unit is represented as an individual device object, and all
  associated measurements are defined as sensors on that device.
* A device key only includes the information necessary to uniquely identify the
  device. TempoIQ does not automatically create attributes based on the content
  of the device key, so you have more flexibility in how you generate your device
  keys.
* Device metadata only includes attributes relevant to the overall device. The
  type of measurement becomes the sensor key. In addition, sensors have their
  own metadata which you can use for things like measurement unit or a calibration
  offset.

Finally, TempoIQ only supports attribute metadata; tags are no longer supported.
To emulate a tag, you can define an attribute key with an empty value string.


.. _tdb-write-interface:

Write Interface
---------------

TempoIQ's write interface has changed to accommodate the new device/sensor data
model. In addition, there is no longer a dedicated endpoint for writing data to
a single sensor, there is only a multi write interface. See the
:method:`API Documentation <writeData>` for more information on writing in
TempoIQ.


.. _tdb-read-interface:

Read Interface
--------------

TempoIQ's read interface has been enhanced to offer far more flexibility than
was possible in TempoDB. These enhancements are in two main areas: selecting
sensors to read and performing operations on the returned data.


.. _tdb-selector-interface:

Selector Interface
~~~~~~~~~~~~~~~~~~

In TempoDB, you could select series to read in one of two ways: specifying
a list of series keys, or specifying tags and attributes to match. TempoIQ's
selection interface works in much the same way, but with a few differences:

* You may explicitly *AND* and *OR* attributes together to form more complex
  criteria.
* You may specify criteria about the sensors themselves as well as their parent
  devices.

See the :class:`Search` reference for details.


.. _tdb-function-pipeline:

Function Pipeline
~~~~~~~~~~~~~~~~~

Both TempoDB and TempoIQ support the same historical analysis features: rollups,
interpolation, and aggregation. However, TempoIQ allows you to combine these
functions in any order, whereas TempoDB hardcoded the ordering.

Because of this increased flexibility, you must be conscious of the ordering
of your function pipelines. As you migrate to TempoIQ, to preserve the
same behavior in your application, simply order your pipeline
operations to correspond to the ordering in TempoDB: interpolate,
rollup, then aggregate.


Unsupported TempoDB features
----------------------------

While TempoIQ provides significantly more flexibility than TempoDB, it is not
at 100% feature parity. This section covers every TempoDB feature which is not
supported in TempoIQ.

.. _tdb-single-value:

Single Value Queries
~~~~~~~~~~~~~~~~~~~~

Currently, TempoIQ only supports a subset of the capabilities of TempoDB's
Single Value query. It is possible to read the latest value for a given
sensor, but you can't read points relative to an arbitrary timestamp.

If your application relies on the Single Value API, contact support@tempoiq.com
for suggestions of alternative approaches.


.. _tdb-aggregation:

Cross-Device Aggregation
~~~~~~~~~~~~~~~~~~~~~~~~

The current function pipeline semantics do not contain a concept of combining
data from different devices. Therefore, the aggregation function only allows you
to combine data from sensors on the same device. This limitation will be
addressed in a future update.


.. _tdb-summary-endpoint:

Summary Endpoint
~~~~~~~~~~~~~~~~

TempoIQ does not offer a special method for retreiving summary data over a
time range. However, this functionality can be replicated using a multi-function
rollup. Simply specify a rollup period greater than or equal to the time duration
between the start and end times. This will result in a single rolled up value
for the entire time range. Then specify all rollup functions that you wish to
calculate. The TempoDB summary function returned the following functions:
``count``\ , ``min``\ , ``max``\ , ``mean``\ , ``stddev``\ , and ``sum``\ .

