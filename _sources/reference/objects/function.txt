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


.. TODO:: Create custom object for pipelinefunctions.


.. class:: Rollup

   **Name:** ``rollup``

   **Arguments:**

   =======  ================  ===========
   Name     Type              Description
   =======  ================  ===========
   fold     :class:`Fold`     Folding function to apply
   period   :class:`Period`   Time period for performing the rollup
   =======  ================  ===========


.. class:: MultiRollup

   **Name:** ``multi_rollup``

   **Arguments:**

   =======  ======================  ===========
   Name     Type                    Description
   =======  ======================  ===========
   folds    Array of :class:`Fold`  The list of folding functions to apply
   period   :class:`Period`         Time period for performing the rollup
   =======  ======================  ===========


.. class:: Interpolate

   **Name:** ``interpolate``

   **Arguments:**

   ========  ==================  ===========
   Name      Type                Description
   ========  ==================  ===========
   function  "linear" or "zoh"   The interpolation function to use
   period    :class:`Period`     Period to interpolate to
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

   **Name:** ``find``

   **Arguments:**

   ========  ================================  ===========
   Name      Type                              Description
   ========  ================================  ===========
   function  "max", "min", "first", or "last"  The point to find in each period
   period    :class:`Period`                   Time period to find each point
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
