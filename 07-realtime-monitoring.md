## Realtime monitoring

TempoIQ's realtime monitoring API allows you to define monitoring rules
for your devices. These rules will alert you as soon as a device writes data that
triggers the rule. For example, a monitoring rule could notify a user if their
thermostat records a temperature outside a certain range, or if humidity changes
abnormally quickly.

### Anatomy of a monitoring rule

Defining a monitoring rule is very similar to defining an analytics query. You
create a selector to indicate which sensors to monitor, then compose a pipeline
to define the criteria to monitor.

#### Boolean streams

In the previous sections, all the pipeline operations
operated on streams of numeric values. But in order to generate alerts, we need
to produce streams representing the state of the alert: is a sensor in the alert
condition or not?

TempoIQ supports several operations that treat stream values as booleans, such as:

* Output a boolean indicating if the input stream is greater or less than a given value
* *Combine* and *aggregate* operations that output the AND or OR of multiple boolean streams

#### Triggers

After you define the set of streams to monitor, and the pipeline to compute whether
a stream is in an alert state, you need some way of receiving the new alerts in realtime.
A trigger is exactly that: it converts the streams' state changes into something
that a user or your application can consume.

Currently, only webhooks are supported as triggers. You specify a URL,
and TempoIQ will issue an HTTP POST to that URL every time a stream changes state.

### Data contained in triggers

Just as historical analytics queries can process streams for multiple sensors and
devices, a single monitoring rule can monitor many sensors and devices. Therefore,
when you receive a webhook trigger, it's important that you have enough information
to determine what exactly triggered the alert.

A trigger message includes several fields:
* The name and ID of the rule which generated the message
* Whether the stream transitioned *into* the alert state (rising edge) or
*out of* the alert state (falling edge)
* The stream's metadata -- which sensor and device it came from, or the common
attributes if it's the result of combining or aggregating several streams together.


### Example
