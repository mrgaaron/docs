==============================
Getting Started with Pipelines
==============================

Thanks for participating in our Pipelines research project! This guide 
describes how to start working with your Pipelines environment: writing
events and subscribing to analytics via HTTP.

For a higher-level overview of Pipelines concepts, see :doc:`index`.

For a reference of Pipelines endpoints and responses, see :doc:`http`.

For a guide to our MQTT interface for Pipelines, see :doc:`mqtt`.

.. contents::
   :local:
   :depth: 1

Prerequisites
-------------

You should have already received a set of Pipelines credentials from us.
This is composed of an *environment*, *key*, and *secret*.
For example:

* Environment: ``abc1``
* Key: ``1234567890abcdef1234567890abcdef``
* Secret: ``fedcba0987654321fedcba0987654321``

In addition, you should have already discussed a Pipelines configuration with us,
which includes a *Group By* field and a *Value* field, as well as some additional
information such as aggregation function. These two fields are important, as they
are how we know which data in the events we are using in the computation.

Domains
~~~~~~~

To use your pipelines environment, you'll send requests to: ``$ENVIRONMENT.tempoiq.com``

Channels
--------

Channels are namespaces for events. Currently, all events that you write get routed to channel ID 0. In the future we may support multiple ingest channels, or channels for computed values.

Writing Events
--------------

To write an event, POST a JSON object to ``http://$ENVIRONMENT.tempoiq.com/channels/$CHANNEL/event``. 
Authenticate to the endpoint by providing your key and secret as the username 
and password via HTTP Basic Authentication. To send an event from the command line, 
you can use ``curl``:

.. code-block:: bash

    curl -X POST -i \
        -u "$KEY:$SECRET" \
        -d '{"field1": "val1", "field2": 1.3}' \
        "http://$ENVIRONMENT.tempoiq.com/channels/$CHANNEL/event"

For example:

.. code-block:: bash

    curl -X POST -i \
        -u "1234567890abcdef1234567890abcdef:fedcba0987654321fedcba0987654321" \
        -d '{"field1": "val1", "field2": 1.3}' \
        "http://abc1.tempoiq.com/channels/0/event"

Pipeline Calculation
--------------------

Currently pipeline calculations can only be configured by TempoIQ engineers. If you would
like to change the configuration, please `contact us <support@tempoiq.com>`_.

Suppose your pipeline calculates the minutely maximum of the ``power`` field in the event,
grouped by ``meter_id``. In this case, events must include both of these fields in order
to be handled correctly. For example::

    {
      "meter_id": "house1",
      "power": 1241.0
    }

Events are automatically timestamped when we receive them. If 
you wish to override the generated timestamp, you can provide an 
`ISO 8601 <http://en.wikipedia.org/wiki/ISO_8601>`_-formatted time in a 
field called ``_$_ts``::

    {
      "_$_ts": "2015-06-01T12:05:00Z",
      "meter_id": "house1",
      "power": 1241.0
    }

Depending on your pipeline configuration, events may not be processed if they 
have timestamps too far in the past or future.

Output Graph
------------

Track your resulting analytics with the provided realtime graph. The URL format for 
the graph is:

.. code-block:: none

    http://$ENVIRONMENT.tempoiq.com/index.html?groupBy=$GROUPFIELD&valueField=$VALUEFIELD&$GROUPFIELD=$GROUPVAL

This is best illustrated with the example above. If we want to view the graph of max power for
*house1*, the URL would be:

.. code-block:: none

    http://abc1.tempoiq.com/index.html?groupBy=meter_id&valueField=power&meter_id=house1

To view the output for a different meter, simply change the value of the *meter_id=* argument in the URL. 
You shouldn't ever need to modify any other parts of the URL.

.. image:: /images/pipelines_viz.png
   

Embedding Graphs
~~~~~~~~~~~~~~~~

This graph can also be embedded in a larger web application using an iframe. Simply replace ``index.html`` with
``widget.html``, and set that URL as the iframe source. For example::

    <iframe src="http://abc1.tempoiq.com/widget.html?..." frameborder="0" scrolling="no"></iframe>

