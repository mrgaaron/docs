==============================
Getting Started with Pipelines
==============================

Thanks for participating in our Pipelines research project! This guide 
describes how to start working with your Pipelines environment: writing
events and subscribing to analytics.

Prerequisites
-------------

You should have already received a set of Pipelines credentials from us.
This is composed of an *environment name*, *key*, and *secret*.
For example:

* Environment: ``abc1``
* Key: ``1234567890abcdef1234567890abcdef``
* Secret: ``fedcba0987654321fedcba0987654321``

In addition, you should have already discussed a Pipelines configuration with us,
which includes a *Group By* field and a *Value* field, as well as some additional
information such as aggregation function. These two fields are important, as they
are how we know which data in the events we are using in the computation.


Writing Events
--------------

To write an event, POST a JSON object to ``http://ingest-$ENV.tempoiq.com/users/$KEY/event``. 
Authenticate to the endpoint by providing your key and secret as the username 
and password via HTTP Basic Authentication. To send an event from the command line, 
you can use ``curl``:

.. code-block:: bash

    curl -X POST -i 
        -u "$KEY:$SECRET" \
        -d '{"field1": "val1", "field2": 1.3}' \
        "http://ingest-$ENV.tempoiq.com/users/$KEY/event"

For example:

.. code-block:: bash

    curl -X POST -i \
        -u "1234567890abcdef1234567890abcdef:fedcba0987654321fedcba0987654321" \
        -d '{"field1": "val1", "field2": 1.3}' \
        "http://ingest-abc1.tempoiq.com/users/1234567890abcdef1234567890abcdef/event"

Note that currently we only support plain HTTP; HTTPS endpoints will be added shortly.


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

Events are automatically timestamped when the ingest server receives them. If 
you wish to override the generated timestamp, you can provide an 
ISO 8601-formatted time in a top-level field called ``_$_ts``. Depending on your pipeline
configuration, events may not be processed if they have timestamps too far in the past or
future.

Output Graph
------------

Track your resulting analytics with the provided realtime graph. The URL format for 
the graph is:

.. code-block:: none

    http://app-$ENV.tempoiq.com/index.html?groupBy=<groupingfield>&valueField=<valfield>&<groupingfield>=<group>

This is best illustrated with the example above. If we want to view the graph of max power for
*house1*, the URL would be:

.. code-block:: none

    http://app-abc1.tempoiq.com/index.html?groupBy=meter_id&valueField=power&meter_id=house1

To view the output for a different meter, simply change the value of the *meter_id=* argument in the URL. 
You shouldn't ever need to modify any other parts of the URL.

Embedding Graphs
~~~~~~~~~~~~~~~~

This graph can also be embedded in a larger web application using an iframe. Simply replace ``index.html`` with
``widget.html``, and set that URL as the iframe source. For example::

    <iframe src="http://app-abc1.tempoiq.com/widget.html?..." frameborder="0" scrolling="no"></iframe>

