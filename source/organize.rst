Organize your Sensors
======================

.. contents::
   :depth: 1
   :local:

Data objects
------------

TempoIQ uses a simple two-level data hierarchy, consisting of Devices and Sensors.

.. image:: /images/device_model.png


Devices
~~~~~~~

A :class:`Device` generally corresponds to a discrete physical unit that has one
or more associated sensors. For example: solar panels, vehicles, or activity
monitors.

Each device is required to have a globally unique key. Good choices for
device keys include serial numbers, UUIDs, and other identifiers that will
not change or conflict with other devices.

In addition to a key, you can define attributes on a device. Attributes
allow you to add additional metadata to a device, and construct powerful
analytics queries by analyzing many devices at once. Examples of possible
attributes include user ID, geographic region, and device model number.

Finally, a device can optionally have a human-readable name. The name is not
used internally in TempoIQ, but you can use it in your application for
user-facing displays.


Sensors
~~~~~~~

A :class:`Sensor` corresponds to a single measurement coming from a specific device.
For example: internal temperature, DC voltage, or wind speed.

A sensor is required to have a key unique within its device. Sensors
are referenced by the combination of device key and sensor key. It's 
not possible to have a sensor that is not associated with a device.

In addition to a key, you can define additional attributes on a sensor.
Sensor attributes should describe the specific sensor, rather than the
device as a whole. Examples of possible sensor attributes include
measurement unit, calibration offset, or sensor location (if the location
doesn't apply to the overall device).

Example
~~~~~~~

To better illustrate the relationship between the different data objects, we
will model a simple sensor installation.

Acme Homes manufactures a smart thermostat. Every minute, the thermostat logs
the following values to TempoIQ:

- ``temp1`` - Main floor temperature
- ``temp2`` - Second floor temperature (if applicable)
- ``hum`` - Main floor humidity

An individual thermostat corresponds to a device in TempoIQ. Each device will
have two or three sensors, depending on if ``temp2`` is configured.

Here's one way a thermostat device, sensors, and attributes could be modeled in
TempoIQ:

.. image:: /images/device-attributes.png

Create device
-------------

.. method:: createDevice(device)

   :endpoint: ``POST /v2/devices``
   :arg Device device: The device to create
   :returns: The :class:`Device` that was created

   .. snippet-display:: create-device


Get devices
-----------

.. method:: findDevices(search)

  :endpoint: ``GET /v2/devices``
  :arg Search search:
  :returns: A :class:`Cursor` over the devices

  .. snippet-display:: get-devices

Some libraries also support a special method to retrieve a single
device by its key:

.. method:: getDevice(key)

   :endpoint: ``GET /v2/devices/:key``
   :arg String key: The key of the device to get
   :returns: The :class:`Device` with the given key

   .. snippet-display:: get-device

Ordering
~~~~~~~~

Devices can be queried with a configurable ordering parameter.  Ordering by 
key, date created, and date last modified in either ascending or descending 
direction is possible:

.. snippet-display:: device-ordering


Update device
-------------

.. method:: updateDevice(device)

   :endpoint: ``PUT /v2/devices/:key``
   :arg Device device: The updated device
   :returns: The updated :class:`Device`

   Updates a device with the provided metadata and sensors. To safely modify just
   some of a device's properties, it is recommended to use this method in a
   *GET-modify-PUT* pattern. First, get the device object using getDevice or
   similar. Then, modify the metadata or sensors as desired. Finally, update the
   device on the server with this method.

   A device's key is immutable, so it is not possible to change a device
   key with this method. Calling updateDevice with a key that does not already
   exist in TempoIQ results in an error.

   .. snippet-display:: update-device


Delete devices
--------------

.. method:: deleteDevices(search)

   :endpoint: ``DELETE /v2/devices/``
   :arg Search search: Selector defining which devices to delete
   :returns: The number of devices that were deleted

   .. snippet-display:: delete-devices

.. method:: deleteDevice(key)

   :endpoint: ``DELETE /v2/devices/:key/``
   :arg String key: The key of the device to delete
   :returns: Nothing

Some final notes:

* Devices in a backend may have different sensor configurations. You may find
  that you have several completely different types of devices; it's easy to
  differentiate between them by setting meaningful attributes.
