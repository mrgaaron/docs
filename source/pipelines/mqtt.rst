===============================
Pipelines MQTT Input and Topics
===============================

Thanks for participating in our Pipelines research project! This reference 
describs the MQTT brokering configuration in your Pipelines environment.

For a higher-level overview of Pipelines concepts, see :doc:`index`.

For a guide to getting started with Pipelines, see :doc:`getting-started`.

For a reference of Pipelines endpoints and responses, see :doc:`http`.

For more information about MQTT client libraries and brokers,
we recommend `Mosquitto <http://mosquitto.org/>`_ and `Paho <http://www.eclipse.org/paho/>`_ .

.. contents::
   :local:

Writing Events
--------------

To write an event, publish a valid event to ``tcp://$ENVIRONMENT.tempoiq.com:1883``,
under the topic ``/tempoiq/channels/$CHANNEL/event``.
Channels are namespaces for events. Currently, all events that you write get routed to channel ID 0.
A valid event is a JSON object. In addition, events must have a key matching the measurement
field you provided TempoIQ, mapped to a numeric value. In addition, except for the optional timestamp
field ``_$_ts``, TempoIQ reserves all keys beginning with the prefix ``_$_``.

If you send an event with some reserved fieldname ``_$_fieldname``, your Pipelines environment will ignore your published message.

If you send malformed JSON, your Pipelines environment will ignore your published message.

TempoIQ internally uses a quality of service (QoS) of 2 (once-only-semantics) for handling MQTT messages,
so if you publish a message with a QoS of 1 or 0, we will repeat that message however many times we receive it.
In the case of an aggregating function, that means that repitition or dropped messages (possible with a QoS of 1 or 0)
can lead to potentially inaccurate results.

At this time, Pipelines does not support authorization, TLS, bulk-writes, or reads via MQTT.

Index of Endpoints
------------------

   .. list-table::
      :header-rows: 1

      * - Endpoint URL
        - Description
      * - tcp://$ENVIRONMENT.pipelines.tepomiq.com:1883
        - the root url for your environment's MQTT broker.
      * - .../channels/``$CHANNEL``/event
        - publish an ``<event>`` to channel_id.

Where ``$CHANNEL`` is a system generated string (currently 0),
``<event>`` is a valid event as described above,
and a ``<bulk_write>`` is simply a JSON object of the form ``{ 'data':[(<event>,)* <event>] }``.

