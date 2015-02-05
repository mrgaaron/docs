=======
Webhook
=======

.. class:: Webhook

   A webhook is the JSON representation of one of TempoIQ's realtime alerts.
   Webhooks are the most straightforward way to interact with realtime alerts programmatically.

   .. list-table::
      :header-rows: 1

      * - Name
        - Type
        - Description
      * - trigger
        - :class:`Trigger`
        - details on the rule's trigger; why it entered or exited an alert state
      * - edge
        - String
        - Whether the rule is beginning to alert (rising) or returning to a normal state (falling)
      * - instigator
        - :class:`Instigator`
        - The `DataPoint` which triggered the webhook, alongside its device and sensor keys
      * - rule_name
        - String
        - The rule's name
      * - rule_key
        - String
        - The rule's unique identifier
      * - rule_address
        - String
        - The URL at which the rule can be accessed

.. class:: Instigator

  The instigator field inside a webhook contains the data point which triggered the alert, and the relevant device and sensor keys

   .. list-table::
      :header-rows: 1

      * - Name
        - Type
        - Description
      * - datapoint
        - :class:`DataPoint`
        - The data point which triggered the rule
      * - device
        - String
        - The key from ``datapoint``'s :class:`Device`
      * - sensor
        - String
        - The key from ``datapoint``'s :class:`Sensor`

.. class:: Trigger

  The comparator and threshold value for sending rule alerts

   .. list-table::
      :header-rows: 1

      * - Name
        - Type
        - Description
      * - comparator
        - String
        - Either "gt", for greater-than, or "lt", for less-than
      * - threshold
        - Number
        - The value at which the trigger activates, depending on the comparator

Example
_______

Alert from a rule detecting negative voltage from a turbine::

    {
      "trigger": {
        "comparator": "lt",
        "threshold": 0
      },
      "instigator": {
        "datapoint": {
          "t": "2012-01-01T12:15:45Z",
          "v": -1
        },
        "device": "turbine.1",
        "sensor": "voltage"
      },
      "edge": "rising",
      "rule_name": "negative_voltage",
      "rule_key": "f05ab8db6cd240579b22543c6c0f06c7"
      "rule_address": "https://developers.tempoiq.com/monitoring/rule/f05ab8db6cd240579b22543c6c0f06c7/"
    }

