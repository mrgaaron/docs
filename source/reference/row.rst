===
Row
===

.. class:: Row

    A timestamp with associated values for one or more data streams.
    When reading data, results are returned as a cursor of rows.

    Sensor values are contained in a nested dictionary in the form
    devicekey => sensorkey => value, for example::

        {
          "device1": {
            "sensorA": 5.4,
            "sensorB": 0.35
          },
          "device2": {
            "sensorA": 24.3,
            "sensorC": 0.0
          }
        }


Fields
------

======  =================  =============
Name    Type               Description
======  =================  =============
t       :class:`DateTime`  Timestamp
data    Dictionary         Values
======  =================  =============


See: :class:`ReadResponse`

