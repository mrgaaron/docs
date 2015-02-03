===============
Realtime Alerts
===============

This guide shows you how to use TempoIQ's Realtime Alert system to
actively monitor your device infrastructure. At the moment, The
TempoiQ Alerting system supports the following alerting criteria:

- Simple threshold *above* a static value
- Simple threshold *below* a static value

The Alert system features the following supported alert scopes:

- Alert on all sensors with a given key
- Alert on any sensor from a subset of devices

Notification Methods
--------------------

The TempoIQ Alerting system supports the following notification
methods for receiving alerts:

- Email

For each notification method, you can expect to receive two event
types:

1. *ALERT*: Sent when a datapoint from a sensor meets the criteria of
   the rule. 
2. *OK*: Sent when a datapoint from a sensor recovers to within the
   rule's criteria.

Examples
--------

To work with Realtime Alerts, click the "Rule List" link under the
Realtime header in your developer console.

.. image:: /images/dev_console.png

From there, you'll see a list of your active rules, which you can view
and edit by clicking on them. Otherwise, you can create a new Realtime
Alert.

.. image:: /images/rule_list.png

Sensor Type Monitoring
~~~~~~~~~~~~~~~~~~~~~~

If you want to monitor all sensors of a specific key, fill out only
the "Sensor Key" form field from the Rule Create page:

.. image:: /images/temp_simple.png

For example, if you want to receive an alert whenever a temperature sensor
from any thermostat falls below a certain threshold, the input values
might look something something like this:

- Sensor Key: *temp*
- Sensor value: *less than*
- Threshold: *80*

When any one of your power sensors dips below the prescribed
threshold, you will receive a triggered email with the alert:

.. image:: /images/alert_email.png

When the sensor returns to normal, you will receive another email
giving the all clear:

.. image:: /images/ok_email.png

Device Subset Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~

You can limit your alerts to a subset of devices within your
infrastructure. From the Rule Create page, create a rule that looks
something like this:

- Sensor Key: *temp*
- Device Attribute: *building*, *16*
- Sensor value: *less than*
- Threshold: *80*

.. image:: /images/temp_device_filtering.png

