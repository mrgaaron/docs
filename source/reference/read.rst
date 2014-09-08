ReadRequest
===========

.. default-domain:: tempoiq

.. class:: ReadRequest

   :arg read:
      read some stuff. Between the start and end time.

   :arg pipeline:

   Send info to TempoIQ. Do other stuff, maybe. *if you want to*\ .


.. method:: Client.read(readRequest)

   :endpoint: ``GET /v2/read/``

   :cursored: True

   :arg ReadRequest readRequest:

      The thing that you want to read. It's a :class:`ReadRequest`
