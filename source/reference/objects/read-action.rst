==========
ReadAction
==========

.. class:: ReadAction

Specifies the range of data to read in a :class:`ReadRequest`.


Fields
-------

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - start
     - :class:`DateTime`
     - Required. The first timestamp to read (inclusive)
   * - stop
     - :class:`DateTime`
     - Required. The last timestamp to read (exclusive)


Example
-------

Read data from January 1 through January 10, 2014::

    {
      "start": "2014-01-01T00:00:00Z",
      "stop": "2014-01-11T00:00:00Z"
    }
