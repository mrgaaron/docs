# Realtime monitoring

TempoIQ's realtime monitoring API allows you to define monitoring rules
for your devices. These rules will alert you as soon as a device writes data that
triggers the rule. For example, a monitoring rule could notify a user if their
thermostat records a temperature outside a certain range, or if humidity changes
abnormally quickly.

### Anatomy of a monitoring rule

Defining a monitoring rule is very similar to defining an analytics query. You
create a selector to indicate which sensors to monitor, then compose a pipeline
to define the criteria to monitor.

`[ graphic showing a selector, pipeline, and trigger ]`

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

Acme Thermostat wants to receive an alert whenever any thermostat's temperature
is below 55 degrees Fahrenheit.

The selector for this rule is straightforward; it should select the
temperature sensor for every device of type *thermostat*.

```
selector = { device: { attributes: { type: "thermostat" } },
             sensor: { key: "temp" } }
```

The pipeline simply takes each stream from the selector, and checks if the value
is less than 55 degrees:

```
pipe = Pipeline.start().lt(55)
```

Whenever the condition is met, we want to send a webhook to Acme's frontend application
so it can forward it to the relevant customer:

```
trigger = Trigger.webhook("https://app.example.com/webhooks")
```

Finally, use the TempoIQ client to create the complete monitoring rule
on the server:

```
resp = client.addMonitorRule(selector, pipe, trigger,
                             {key: "lowtemp", name: "Low Temperature"})
```
Every time a thermostat's temperature crosses the 55 degree threshold, the app's
webhook endpoint receives a JSON object via HTTP POST. The object
contains fields as described above in *Data contained in triggers*.

### Rule lifecycle

The TempoIQ API provides a way to list, modify, and delete existing rules. In
addition, you can temporarily disable a rule by setting its `state` field to
`pending`. For details on rule states and modifying rules, see the *Monitoring
rule reference*.

### Out-of-order writes

An out-of-order write occurs when you write a data point for a sensor where
the timestamp is before the sensor's last data point's timestamp.
TempoIQ supports out-of-order writes, but handling them in a realtime
context can produce unexpected results. This is because an out-of-order
write breaks the invariance that a stream of data points is strictly
chronological.

As a result, monitoring rules ignore out-of-order points. Points written
out-of-order are still stored and can be queried with the historical analytics
APIs.
