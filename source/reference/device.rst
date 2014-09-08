Device
======

.. default-domain:: tempoiq

Definition
----------

.. class:: Device

   The device is the core business object in TempoIQ. All data is stored
   within a device, and analytics can be performed on a device or by
   comparing across several devices.

   A device generally corresponds to a discrete physical unit that has one
   or more associated sensors. For example: a solar panel, vehicle, or activity
   monitor.

   A device contains the following fields:

   .. list-table::
      :header-rows: 1
      
      * - Name
        - Type
        - Description
      * - key
        - String
        - Required. Unique identifier for the device
      * - name
        - String
        - Human-readable name
      * - attributes
        - Attributes hash
        - Key/value metadata describing the device
      * - sensors
        - Array of :class:`Sensor`
        - The sensors attached to the device

Field details
-------------

key
~~~

Device keys are immutable and must be globally unique. If you delete
a device with a given key, it is possible to create a new device with
the same key, but the new device will not retain the metadata and sensors
from the deleted device.

Good choices for device keys include serial numbers, UUIDs, and other
identifiers that will not change or conflict with other devices.

As with all strings in TempoIQ, device keys support unicode characters.


name
~~~~

Optional field for storing a human-readable description of the device. Names
are not required to be unique and may be modified after creating the
device.


attributes
~~~~~~~~~~

Mutable key/value metadata describing the device. Attributes
behave similarly to fields in a schemaless document store like MongoDB.
It's possible to define different attribute keys on different devices, and
TempoIQ does not enforce the existence of any attributes.

Defining meaningful attributes allows you to construct
powerful queries using :class:`Selector`\ s. For example, a *thermostat* device might
define attributes **building** and **floor**. This would let you query for
the average temperature on each floor in a given building.


sensors
~~~~~~~

List of :class:`Sensor` objects attached to the device. Sensors may be added
and deleted after creating a device, but keep in mind that deleting a
sensor will remove all of its historical data.

If sensors are frequently created or removed from a device, it might
make sense to split up sensors into multiple smaller devices that each
have a more consistent configuration.

TempoIQ's storage engine is optimized for devices with relatively few
long-living sensors. You may find yourself frequently creating/deleting
sensors on a device, or having devices with more than 30-50 sensors.
If this is the case, consider splitting your sensors across several
devices with smaller, more consistent configurations.


Considerations
--------------

Attributes vs. sensors
~~~~~~~~~~~~~~~~~~~~~~

Attributes and sensors are both fields for storing data
associated with a device, but they are fundamentally different. A sensor
represents a measured value or state from the device that changes over time.
An attribute represents a grouping that the device is a part
of, and should rarely change. TempoIQ also does not store a history of past
attribute values.
