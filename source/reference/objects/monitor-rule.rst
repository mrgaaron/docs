===========
MonitorRule
===========

.. contents::

.. attention:: The JSON representation of MonitorRules has not yet been finalized.
  This page documents the format at the time of writing, but it may change in
  the future.

Description
-----------

.. class:: MonitorRule

  The complete representation of a monitoring rule. It consists of three
  parts: a *Search* to define which devices and sensors the rule should be applied
  to, the main *Rule* definition, and a *grouping scheme* to indicate how
  different sensors should be grouped together.

  .. list-table::
    :widths: 1 1 4
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
      - "device", "sensor", or "any"
      - Required. Grouping scheme for the rule. See :ref:`alert-groupings` below


.. class:: Rule

  The core of the MonitorRule definition.

  .. list-table::
    :widths: 1 1 4
    :header-rows: 1

    * - Name
      - Type
      - Description
    * - key
      - String
      - Optional. Unique identifier for the rule. If a key is not defined, one will be generated.
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
      :widths: 1 1 4
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
    :widths: 1 1 4
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



.. _alert-groupings:

Grouping schemes
----------------

The grouping scheme parameter indicates whether data from different sensors
and devices should go through a single rule instance, or be routed to
different instances. This affects behavior in several ways:

* If a rule contains conditions that filter for different sensors or devices,
  you must ensure that the scheme allows all relevant sensors to be grouped
  together. Otherwise the rule will never trigger because data for the different
  conditions won't go to the same rule instance.
* Webhooks contain the scope of the rule instance, so a more granular grouping
  allows for more detailed information in the alerts that your application
  receives.
* If a grouping and a condition's filter allows for multiple sensor streams to
  go through a single condition, the condition's moving average trigger would
  be calculated from all data points from all streams, not the average of each
  stream individually.


The supported groupings are:

any
  All sensors that meet the search criteria will be routed to a single rule
  instance. The webhook will not contain any information about which sensor or
  device an alert came from, but it's possible to create a rule with conditions
  that apply to different devices.

device
  Sensors from different devices will be routed to different rule instances,
  where each instance is scoped to a single device. The webhook will
  therefore contain information about which device an alert came from, but it's
  not possible to create a rule with conditions that apply to different devices.
  This is the most common setting.

sensor
  Every sensor will be routed to a different rule instance, where each instance
  is scoped to a single sensor and device. The webhook will therefore contain
  information about which sensor and device an alert came from, but it's not
  possible to create a rule with conditions that apply to different sensors or
  devices.



Search vs. Filter
-----------------

A MonitorRule contains two similar but distinct concepts: a search and
a filter. Understanding their differences and how they interact is important for
constructing more complex monitoring rules.

A search defines the overall set of devices relevant to the rule.
Typically it is not necessary to select specific sensors in a search; you can
simply use the "all" sensor selector.

A filter selects a subset of the search results that an individual condition
should apply to. This is important when a rule contains multiple conditions
that apply to different sensors.

For example, consider a rule that sends an alert when a device's temperature
sensor has a value below 50 **and** the humidity sensor has a value above 80.
The conditions for the rule would be as follows::

  [
    {
      "filter": { "operation": "select",
                  "type": "sensor_key",
                  "arguments": "temperature" },
      "trigger": { "name": "value",
                   "arguments": [ "static", "lt", 50 ] }
    },
    {
      "filter": { "operation": "select",
                  "type": "sensor_key",
                  "arguments": "humidity" },
      "trigger": { "name": "value",
                   "arguments": [ "static", "gt", 80 ] }
    }
  ]


For rules with a single condition, there is no practical difference between a
search and a filter. However, for clarity and performance, it is still
recommended to define the device selection in the search and the sensor selection
in the filter.



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
