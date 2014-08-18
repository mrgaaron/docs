# Reading sensor data

Using TempoIQ's analytics APIs, you can read, analyze, and perform complex
calculations with your sensor data.

## Basic historical read

A basic read operation takes a sensor selector, and a start and end datetime.
It returns streams of data points for the selected sensors over the specified time
range.

`[ schematic diagram of relationship between selectors, streams, sensors, and a read request ]`


### Selectors

A selector defines a set of sensors from your environment by matching
search criteria, such as:

* Device keys
* Device attributes
* Sensor keys
* Sensor attributes

Multiple criteria can be combined using boolean AND and OR operations.

A selector is only valid if it includes both device criteria and sensor criteria.
If you want to select all sensors on a device, or all devices in your environment,
you must use special wildcard statements. See the API reference for the actual syntax.


### Streams

A stream is an ordered sequence of data points (i.e. `timestamp, value` tuples)
along with some context describing the source of the data points.
When you read data from several sensors, TempoIQ returns one stream per sensor,
where each stream's context describes the device and sensor that the data stream
originated from.


### Example
Customer 123 has thermostats installed at three different sites: A, B, and C.
She wishes to compare the humidity across all her sites between 2014-06-01 and 2014-06-06.

The selector in this case must select the 'hum' sensor on thermostat devices where
the customer attribute is '123'.

```
sensors = {
            device: {
              attributes: {
                type: "thermostat",
                customer: "123"
              }
            },
            sensor: {
              key: "hum"
            }
          };

start = "2014-06-01T00:00:00Z";
end = "2014-06-06T00:00:00Z";

response = client.read(sensors, start, end);

// TODO: example code for iterating over sensor metadata and data points
```

## Latest value

Sometimes you just need the latest value for a sensor, not a whole range of historical data points.
The `latest` method is similar to the `read` call, but returns a single data point
for each sensor instead of a stream. There are no 'start' or 'end' parameters, but
the selector parameter acts exactly as in the `read` call.

### Example
A dashboard application shows the current value for a given thermostat's temperature
and humidity.

```
sensors = {
            device: { key: thermostatKey },  // As supplied by user or database lookup
            sensor: "ALL"
          };

response = client.latest(sensors);
```
