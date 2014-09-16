===========
MonitorRule
===========

.. attention:: The JSON representation of MonitorRules has not yet been finalized.
   This page documents the format at the time of writing, but it may change in
   the future.

Description
-----------

.. class:: MonitorRule

  The complete representation of a monitoring rule.

  .. list-table::
    :header-rows: 1

    * - Name
      - Type
      - Description
    * - rule
      - :class:`Rule`
      - Required. See definition below
    * - search
      - :class:`Search`
      - Required.
    * - alerts
      - "any", "device", or "sensor"
      - Required. See :ref:`alert-groupings` below


.. class:: Rule

  The core of the MonitorRule definition. Contains the following fields:

  .. list-table::
    :header-rows: 1

    * - Name
      - Type
      - Description
    * - key
      - String
      - Optional. If a key is not defined, one will be generated.
    * - name
      - String
      - Optional. Human-readable name
    * - conditions
      - List of :class:`Condition`\ s
      - Required. When all conditions are true, the rule is triggered
    * - actions
      - List of :class:`MonitorAction`\ s
      - Required. What to do when an alert is triggered
    * - status
      - :class:`RuleStatus`
      - Optional, default is 'pending'.
    * - freshness
      - Number (seconds)
      - Optional. The rule will ignore data points with timestamps more than this many seconds in the past


.. class:: Condition

    .. list-table::
       :header-rows: 1

       * - Name
         - Type
         - Description
       * - filter
         - :class:`StreamFilter`
         - Required
       * - trigger
         - :class:`Trigger`
         - Required


.. class:: StreamFilter

  Which sensors out of the overall Search should have this condition applied.
  Typically the search will select the devices, and the StreamFilter only needs
  to filter for a specific sensor key. This allows for creating rules with
  different conditions on different sensors. For example, alert when a device's
  temperature is over 50, and humidity is over 80.

  .. list-table::
    :header-rows: 1

    * - Name
      - Type
      - Description
    * - operation
      - "select" or "reject"
      - Required
    * - type
      - String
      - Required
    * - arguments
      - Array of String
      - Arguments to the filter type

  Supported filter types and their arguments are:

  sensor_key [ String ]
    Filter for sensors with the given key
  device_key [ String ]
    Filter for devices with the given key
  attribute_key [ String ]
    ??
  attributes [ ?? ]
    ??

  .. todo:: what are the filter arguments?


.. class:: Trigger

    Defines when a condition is true or false. Triggers have a *name*
    field, which indicates the type of trigger, and an *arguments* field, which
    contains the trigger's list of arguments.

    The following triggers are supported. Following each trigger name is
    the array of arguments that must be supplied.


    availability: [ :class:`Period` ]
      if the rule does not receive any data from a device within
      a timeout period, the rule triggers. Useful for alerting when a device goes
      offline and stops sending data.

    exp_moving_average: [ "static", *PositiveInteger* , "gt" or "lt", *Number* ]
      takes a positive integer representing the window of time
      for consideration in the moving average, a comparator (representing a
      greater-than or less-than relationship), and a number to compare datapoints to.
      Triggers when the moving average falls outside of the
      range indicated by the comparator and comparison.

    exp_moving_average: [ "deviation", *PositiveInteger*, *Number* ]
      as above, but triggers when the moving average is further
      than the second argument from the final argument (if the value of the average
      is more than 'Positive-Number' away from 'Number').

    value: [ "static", "gt" or "lt", *Number* ]
      triggers when the value is less than or greater than the number given.

    value: ["deviation", *dev: Number*, *center: Number* ]
      triggers when the value is more than *dev* away from *center*, either higher
      or lower.

    **Examples**

    * Trigger when a sensor's value is below 15:
      ``{"name": "value", "arguments": ["static", "lt", 15.0]}``

    * Trigger when a sensor hasn't received a value in the past hour:
      ``{"name": "availability", "arguments": ["1hour"] }``


.. class:: MonitorAction

  What action should be taken when a monitoring rule is triggered. Currently
  the only supported action is to send a webhook to a designated URL. Specify
  the webhook url as the *url* field in the MonitorAction object, such as::

    { "url": "https://example.com/app/webhooks"}


.. class:: RuleStatus

   Possible values:

   active
      The rule is actively monitoring data and sending alert actions when
      triggers occur.

   pending
      The rule is stored in TempoIQ but is not currently monitoring data. This
      is the default status when creating a new rule.

   logonly
      The rule is monitoring data and logging when triggers occur, but is not
      sending alert actions.




Search vs. Filter
-----------------

.. todo:: document search vs. filter


.. _alert-groupings:

Alert Groupings
---------------

.. todo:: document alert grouping parameter

Example
-------

A complete definition of a monitoring rule::

    {
      "rule": {
        "status" : "active",
        "conditions": [
          {
            "filter": {
              "and": [
                {
                  "operation": "select",
                  "type":  "attributes",
                  "arguments": ["building", "445 w. erie"]
                },
                {
                  "operation": "select",
                  "type":  "device_key",
                  "arguments": ["stuff"]
                }
              ]
            },
            "trigger": {
              "name": "exp_moving_average"
              "arguments": [
                "static",
                "300",
                "lt",
                "5"
              ]
            }
          }
        ],
        "actions": [
          {
            "url": "http://example.com/mywebhook"
          }
        ],
        "name": "Human-readable name",
        "key": "user-defined-unique-id"
      },
      "search": {
        "filters": {
          "devices": {
            "and": [
              {
                "attributes": {
                  "building": "445-w-Erie"
                }
              },
              {
                "attributes": {
                  "equipment": "heatpump"
                }
              }
            ]
          },
          "sensors": {
            "or": [
              {
                "key": "heat-1"
              },
              {
                "key": "heatpump-1"
              }
            ]
          }
        },
        "select": "sensors"
      },
      "alerts": "device"
    }
