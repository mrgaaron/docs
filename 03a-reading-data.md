# Reading sensor data

Sensor data can be read in a variety of ways. You can request historical data over
a specified time range, read just the latest value, or even subscribe to realtime
updates as your devices write new data points.

Regardless of the type of read request, the general components are the same.

A selector specifies which devices and sensors to read;
and an executor reads the data streams from the sensors over a specified time
range (realtime or historical), and formats the result as requested.

```
[ Graphic of the relationship between executor, selector, and streams ]
```

Let's take a closer look at these components:

## Selectors

A selector returns a set of sensors from your environment based on provided
search criteria, such as:

* Device keys
* Device attributes
* Sensor keys
* Sensor attributes

Multiple criteria can be combined using boolean AND and OR operations.

#### Example
Customer 123 has thermostats installed at several different sites.
She wishes to compare the humidity across the sites.

The selector in this case must select the 'hum' sensor on thermostat devices where
the customer attribute is '123'.

Or, in pseudocode:

```
device_attr["type"] == "thermostat"
AND device_attr["customer"] == "123"
AND sensor_key["hum"]
```

A selector is only valid if it includes both device criteria and sensor criteria.
If you want to select all sensors on a device, or all devices in your environment,
you must use special wildcard statements. See the API reference for the actual syntax.

## Executors

Executors orchestrate the read query, reading the relevant portion of the data stream
from each sensor in the selector and returning the result.

The executor defines the time range for your read request and how the data will be returned.
There are different executors for accessing historical, current value, and future
realtime data, each with their own relevant parameters and options for returning data.

[ add info about different executors ]

## Streams
