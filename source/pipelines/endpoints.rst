==============================
Pipelines Input and Endpoints
==============================

Thanks for participating in our Pipelines research project! This reference 
describes the endpoints present in your Pipelines environment.

For a higher-level overview of Pipelines concepts, see :doc:`index`.

For a guide to getting started with Pipelines, see :doc:`getting-started`.

.. contents::
   :local:

Writing Events
--------------

To write an event, POST a valid event to ``http://ingest-$ENVIRONMENT.tempoiq.com/users/$KEY/event``.
A valid event is a JSON object. In addition, events must have a key matching the measurement
field you provided TempoIQ, mapped to a numeric value. In addition, except for the optional timestamp
field ``_$_ts``, TempoIQ reserves all keys beginning with the prefix ``_$_``.

If you send an event with some reserved fieldname ``_$_fieldname``, your Pipelines environment will return a
422 (Unprocessable Entity) response with a JSON object representing the error ::

    {
      "error": "reserved name",
      "reason": "'_$_fieldname' is an invalid key name; TempoIQ reserves all fields beginning with '_$_'"
    }

If you send malformed JSON, your Pipelines environment will return a 400 (Bad Request) response
with a JSON object representing the error ::

    {
      "error": "invalid json"
      "reason": "<Whatever linting information we can derive>"
    }

Latest Values
-------------
To view the latest events, GET from ``http://latest-$ENVIRONMENT.tempoiq.com/latest/``.
Your environment will return a JSON array containing the most recently emitted event
for each grouping. For example, if you had a pipeline aggregating daily energy consumption
grouped by meter_id::

    [
      {
        "meter_id": "house1",
        "energy": 245.0
      },
      {
        "meter_id": "house2",
        "energy": 1734.2
      },
      ...
    ]

