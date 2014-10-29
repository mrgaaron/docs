================
PipelineFunction
================

.. class:: PipelineFunction

Transforms data in a pipeline. The arguments below are listed in the order
that they should be specified when constructing the request. For example::

    "functions": [
      {
        "name": "rollup",
        "arguments": ["max", "1day"]      // [Fold, Period]
      }
    ]


.. class:: Rollup

   A rollup downsamples sensor data by applying a folding function over all
   points that fall within a given time period. For example, the maximum within
   each 1-hour period.

   Rollups are defined by a folding function and a time period.


   **Folding Functions**

   The folding function specifies how the datapoints are reduced within each
   period. The following folding functions are supported:

   * mean - Simple average of values in each period
   * sum - Sum of values
   * min - Minimum value
   * max - Maximum value
   * stddev - Standard deviation
   * variance - Variance, or sum of squares
   * count - Total number of datapoints in each period
   * range - Maximum value less the minimum value
   * first - First data point in each period
   * last - Last data point in each period

   **Name:** ``rollup``

   **Arguments:**

   =======  =====================  ===========
   Name     Type                   Description
   =======  =====================  ===========
   fold     Fold as defined above  Folding function to apply
   period   :class:`Period`        Time period for performing the rollup
   start    :class:`DateTime`      Same as the start time in the read interval
   =======  =====================  ===========


.. class:: MultiRollup

   The multi-rollup function applies several folds to the same sensor data.

   **Name:** ``multi_rollup``

   **Arguments:**

   =======  ======================  ===========
   Name     Type                    Description
   =======  ======================  ===========
   folds    Array of Folds          The list of folding functions to apply
   period   :class:`Period`         Time period for performing the rollup
   start    :class:`DateTime`       Same as the start time in the read interval
   =======  ======================  ===========


.. only:: dev

  .. todo:: Decide if interpolate/aggregate are ready to be exposed publicly

  .. class:: Interpolate

     **Name:** ``interpolate``

     **Arguments:**

     ========  ==================  ===========
     Name      Type                Description
     ========  ==================  ===========
     function  "linear" or "zoh"   The interpolation function to use
     period    :class:`Period`     Period to interpolate to
     start     :class:`DateTime`   Same as the start time in the read interval
     stop      :class:`DateTime`   Same as the stop time in the read interval
     ========  ==================  ===========


  .. class:: Aggregate

     **Name:** ``aggregation``

     **Arguments:**

     ========  ==================  ===========
     Name      Type                Description
     ========  ==================  ===========
     function  :class:`Fold`       The aggregation function to use
     ========  ==================  ===========


.. class:: Find

   Find is similar to a rollup, but it returns an actual data point from each
   period, based on the predicate function.

   **Name:** ``find``

   **Arguments:**

   ========  ================================  ===========
   Name      Type                              Description
   ========  ================================  ===========
   function  "max", "min", "first", or "last"  The point to find in each period
   period    :class:`Period`                   Time period to find each point
   start     :class:`DateTime`                 Same as the start time in the read interval
   ========  ================================  ===========


.. class:: ConvertTZ

   Convert the DataPoints into the specified time zone.

   **Name:** ``convert_tz``

   **Arguments:**

   ========  ==================  ===========
   Name      Type                Description
   ========  ==================  ===========
   Timezone  :class:`TimeZone`   Time zone to convert to
   ========  ==================  ===========
