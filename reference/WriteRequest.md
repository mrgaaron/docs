# WriteRequest

Contains sensor data to write to TempoIQ.

A WriteRequest is a map of device keys to their associated
sensor data. Each device's sensor data is itself a map from
the sensor key to an array of DataPoints for that sensor. In JSON,
this looks like:

```json
{
  "device1": {
    "sensor1": [
      { "t": "2014-04-01T05:00:00.000Z", "v": 17.2 },
      { "t": "2014-04-01T05:01:00.000Z", "v": 33.4 },
      { "t": "2014-04-01T05:02:00.000Z", "v": 38.5 }
    ],
    "sensor2": [
      { "t": "2014-04-01T05:00:00.000Z", "v": 3.2 },
      { "t": "2014-04-01T05:01:00.000Z", "v": 24.5 },
      { "t": "2014-04-01T05:02:00.000Z", "v": 19.3 }
    ]
  }
}
```

Client libraries may offer convenience methods and shortcuts for
constructing WriteRequests.

A single WriteRequest can contain DataPoints for many devices and sensors.
When possible, it's recommended to aggregate many DataPoints into a single
WriteRequest instead of sending many small requests. This can increase write
throughput dramatically.

See: `Client.writeData`
