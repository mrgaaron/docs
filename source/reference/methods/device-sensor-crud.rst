======================
Device and Sensor CRUD
======================

.. contents::

Create device
-------------

.. method:: createDevice(device)

   :endpoint: ``POST /v2/devices``
   :arg Device device: The device to create
   :returns: The :class:`Device` that was created

   .. snippet-display:: create-device


Get device
----------

.. method:: getDevice(key)

   :endpoint: ``GET /v2/devices/:key``
   :arg String key: The key of the device to get
   :returns: The :class:`Device` with the given key

   .. snippet-display:: get-device


Find devices
------------

.. method:: findDevices(search)

  :endpoint: ``GET /v2/devices``
  :arg Search search:
  :returns: A :class:`Cursor` over the devices

Example
~~~~~~~

.. snippet-display:: get-devices

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

   A device's sensor configuration is currently also immutable.


Example
~~~~~~~

.. snippet-display:: update-device


Delete devices
--------------

.. method:: deleteDevice(key)

   :endpoint: ``DELETE /v2/devices/:key/``
   :arg String key: The key of the device to delete
   :returns: Nothing


.. method:: deleteDevices(search)

   :endpoint: ``DELETE /v2/devices/``
   :arg Search search: Selector defining which devices to delete
   :returns: The number of devices that were deleted

Example
~~~~~~~

.. snippet-display:: delete-devices
