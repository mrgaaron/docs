ReadResponse
============

.. contents::

Definition
----------

.. class:: ReadResponse

   Object containing the results of a :method:`read` operation.

   Contains a sequence of :class:`MultiPoint`\ s. If the read operation contains
   data from multiple streams, the value of each DataPoint will contain data for
   every stream with a value defined at that timestamp. See :ref:`examples` below.

.. todo:: note about cursoring in readResponses

.. todo:: document MultiPoint format

.. _examples:

Examples
--------

#. Data from a single sensor

   .. code-block:: javascript

      {
        "data": [
          { "t": "2014-01-01T01:00:00.000Z",
            "v": {
              "dev1": { "temperature": 2.0 }
            }
          },
          { "t": "2014-01-01T01:01:00.000Z",
            "v": {
              "dev1": { "temperature": 1.4 }
            }
          },
          <...>
        ]
      }


#. Data from several sensors on several devices

   .. code-block:: javascript

      {
        "data": [
          { "t": "2014-01-01T01:00:00.000Z",
            "v": {
              "dev1": { "temperature": 23.0, "humidity": 45.0 },
              "dev2": { "temperature": 21.5, "humidity": 53.0 }
            }
          },
          { "t": "2014-01-01T01:01:00.000Z",
            "v": {
              "dev1": { "temperature": 22.0, "humidity": 43.0 },
              "dev2": { "temperature": 19.0, "humidity": 54.0 }
            }
          },
          <...>
        ]
      }

#. Data with mis-aligned timestamps

   .. code-block:: javascript

      {
        "data": [
          { "t": "2014-01-01T01:00:00.120Z",
            "v": {
              "dev1": { "humidity": 45.0 },
            }
          },
          { "t": "2014-01-01T01:00:00.490Z",
            "v": {
              "dev2": { "temperature": 21.5 },
            }
          },
          { "t": "2014-01-01T01:00:00.510Z",
            "v": {
              "dev1": { "temperature": 23.0 },
            }
          },
          { "t": "2014-01-01T01:00:00.620Z",
            "v": {
              "dev2": { "humidity": 53.0 }
            }
          },
          <...>
        ]
      }

   Note that the ``data`` array is always ordered by timestamp.
