================
PipelineFunction
================

.. class:: PipelineFunction

Transforms data in a pipeline.


.. TODO:: Create custom object for pipelinefunctions.

.. class:: rollup

   Arguments:

   =======  ================  ===========
   Name     Type              Description
   =======  ================  ===========
   Fold     :class:`Fold`     Folding function to apply
   Period   :class:`Period`   Time period for performing the rollup
   =======  ================  ===========


.. class:: convert_tz

   Convert the DataPoints into the specified time zone.

   Arguments:

   ========  ==================  ===========
   Name      Type                Description
   ========  ==================  ===========
   Timezone  :class:`TimeZone`   Time zone to convert to
   ========  ==================  ===========
