# TempoIQ introduction

TempoIQ is an analytics backend for sensor data. Connected devices can write data directly to TempoIQ via HTTP, or the data can be aggregated through a proxy or gateway.

You can construct realtime and historical data queries using TempoIQ's analytics API. 


## Data objects

TempoIQ uses a very simple data hierarchy, consisting of Devices and Sensors.

    [[ Simple high-level graphic showing backend ]]
    [[ with many devices; devices with many sensors ]]

### Devices

A device generally corresponds to a discrete physical unit that has one or more associated measurements. For example: solar panels, vehicles, or activity monitors. 

A device is required to have a key. It is a globally unique identifier for each device. Good choices for device keys include serial numbers, UUIDs, and other identifiers that will not change or conflict with other devices.

In addition to a key, you may define additional attributes on a device. Attributes allow you to construct powerful analytics queries by analyzing many devices at once. Examples of possible attributes include user ID, geographic region, and device model number.


### Sensors

A sensor corresponds to a single measurement coming from a specific device. For example: internal temperature, DC voltage, or wind speed.

A sensor is required to have a key. It must be unique within its device. Sensors can be referenced by the combination of device key and sensor key. There is no concept of a sensor that is not associated with a device.

In addition to a key, you man define additional attributes on a sensor. Sensor attributes should describe the specific sensor, rather than the device as a whole. Examples of possible sensor attributes include measurement unit, calibration offset, or sensor location (if the location doesn't apply to the overall device).

### Example

To better illustrate the relationship between the different data objects, we will model a simple sensor installation. 

Acme Homes manufactures a smart thermostat. Every minute, the thermostat logs the following values to TempoIQ:

- `temp1` - Main floor temperature
- `temp2` - Second floor temperature (if applicable)
- `hum` - Main floor humidity

An individual thermostat corresponds to a device in TempoIQ. Each device will have two or three sensors, depending on if `temp2` is configured.

Here's one way a thermostat device, sensors, and attributes could be modeled in TempoIQ:

```javascript
{
  key: "v1-123456",
  attributes: {
    user_id: "321",
    neighborhood: "444"
  },
  sensors: [
    {
      key: "temp1",
      attributes: {
        unit: "degC",
        type: "temperature"
      }
    },
    {
      key: "temp2",
      attributes: {
        unit: "degC",
        type: "temperature"
      }
    },
    {
      key: "hum",
      attributes: {
        type: "humidity"
      }
    }
  ]
}
```

Some final notes:
* Devices in a backend may have different sensor configurations. You may find that you have several completely different types of devices; it's easy to differentiate between them by setting meaningful attributes.

## Writing sensor data

Now that we've covered the basics of the device and sensor objects, let's take a closer look at how to work with actual measured data in TempoIQ.

Every sensor stores its data as a sequence of data points. A data point consists of a timestamp and a value. To write a single data point, specify the sensor to write to (device key+sensor key), and the data point to write. A JSON representation of this data structure would be:

```javascript
{ "device": "v1-123456", 
  "sensor": "temp1", 
  "dp": { 
    "ts": "2014-08-20T00:22:30Z",
    "v": 23.5
  }
}
```

In concept, any write request is simply a collection of one or more `(deviceKey, sensorKey, timestamp, value)` tuples. In practice, there are several specialized endpoints for handling common write operations more efficiently. One example of this is for writing data for several sensors on the same device at the same timestamp:

```javascript
{ "device": "v1-123456",
  "ts": "2014-08-20T00:22:30Z",
  "data": {
      "temp1": 23.5,
      "hum": 46
  }
}
```

### Properties of sensor data

TempoIQ's write APIs are designed to be as flexible and easy-to-use as possible. A few notes to help you make the most of them:
* A sensor can only have one value for a given timestamp. If you write a data point for the same timestamp as an existing point, the new value will overwrite the old one.
* A sensor's data points are allowed to be written out of order. However, points written out of order may be ignored by realtime analytics pipelines. See the section on realtime analytics for more details.

