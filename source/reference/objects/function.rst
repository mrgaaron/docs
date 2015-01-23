================
PipelineFunction
================

.. class:: PipelineFunction

Transforms data streams in a pipeline.

.. snippet-display:: pipeline

.. class:: Rollup

   A rollup downsamples sensor data by applying a folding function over all
   points that fall within a given time period. For example, the maximum within
   each 1-hour period.

   Rollups are defined by a folding function and a time period.


   **Name:** ``rollup``

   **Arguments:**

   =======  =====================  ===========
   Name     Type                   Description
   =======  =====================  ===========
   fold     :class:`Fold`          Folding function to apply
   period   :class:`Period`        Time period for performing the rollup
   start    :class:`DateTime`      Same as the start time in the read interval
   =======  =====================  ===========

.. todo:: note about start param in rollups


.. class:: MultiRollup

   The multi-rollup function applies several folds to the same sensor data. The
   result will contain multiple streams for each sensor, one per rollup function.

   **Name:** ``multi_rollup``

   **Arguments:**

   =======  ======================  ===========
   Name     Type                    Description
   =======  ======================  ===========
   folds    Array of :class:`Fold`  The list of folding functions to apply
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
