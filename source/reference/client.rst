Client
======

.. default-domain:: tempoiq

.. class:: Client

   The main entry point to the TempoIQ API.


.. method:: Client.createDevice(device)

   :endpoint: ``POST /v2/devices/``
   :arg Device device: The device to create
   :rtype: The :class:`Device` that was created

.. method:: Client.getDevice(key)

   :endpoint: ``GET /v2/devices/:key/``
   :arg String key: The key of the device to get
   :rtype: The :class:`Device` with the given key

.. method:: Client.updateDevice(device)

   :endpoint: ``PUT /v2/devices/:key/``
   :arg Device device: The updated device
   :rtype Device: The updated device

   Updates a device with the provided metadata and sensors. To safely modify just
   some of a device's properties, it is recommended to use this method in a
   *GET-modify-PUT* pattern. First, get the device object using getDevice or
   similar. Then, modify the metadata or sensors as desired. Finally, update the
   device on the server with this method.

   A device's key is immutable, so it is not possible to change a device
   key with this method. Calling updateDevice with a key that does not already
   exist in TempoIQ results in an error.




