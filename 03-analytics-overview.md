# Analytics API Overview

With TempoIQ's analytics API, you can analyze historical or realtime data
in a variety of ways. Continuing with our smart thermostat example,
some possible uses for the analytics API include:

* For the past month, calculate min/max daily temperatures for one or more
thermostats.
* Send an SMS alert to a customer if their home's temperature is outside
a given range, or if it changes abnormally quickly.


### Anatomy of an analytics request

An analytics request in TempoIQ is made up of three components: a selector,
a processing pipeline, and an executor.

The selector specifies which devices and sensors are part of the analysis;
the pipeline defines the computations to be carried out;
and the executor runs the analysis over a specified time range (realtime or historical)
and formats the output as requested.

The following sections describe these parts in more detail.

### Selectors

A selector filters the devices in your environment down to the group
that you are actually performing the analysis on. It is roughly equivalent to the WHERE
clause of a SQL SELECT statement.

Devices can be selected using several criteria:

* By device key
* By attribute value
* By attribute existence

Multiple criteria can be combined using boolean AND and OR operations.

#### Example
A customer owns an apartment building where each unit has a thermostat installed.
She wishes to compare the temperature and humidity between apartment 1A and
apartment 2A.
The apartment number is stored in the thermostat's `site` attribute.

The selector in this case must select thermostat devices where the site ID is either
1A or 2A.

Or, in pseudocode:
```
attr["device_type"] == "thermostat" AND (attr["site"] == "1A" OR attr["site"] == "2A")
```

### Pipelines
TODO: update

The processing pipeline is the heart of an analysis operation.
The pipeline defines the stream
lookup(s) and operations that are performed for each device.



### Executors
TODO: update

There are two main types of stream handlers, realtime and historical:
- Realtime handlers continuously pass new incoming sensor data through the analytics
pipeline and push realtime updates to clients, e.g. via websocket, HTTP post, or SMS.
- Historical handlers use stored historical sensor data to compute the stream over
a specified time range and return the result, typically as a JSON object over HTTP.

In addition to the actual (timestamp, value) pairs of the streams themselves, stream
handlers also provide some context about where the data came from. This consists
of a stream descriptor describing the pipeline, and a scope, typically the device
that generated that particular stream. The format in which this context is provided
varies from handler to handler.
