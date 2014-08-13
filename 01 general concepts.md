# Intro to TempoIQ

TempoIQ is an analytics backend for sensor data. Connected devices write data directly to TempoIQ via HTTPS, or through an intermediate proxy or gateway.

You can construct realtime and historical queries using TempoIQ's Analytics API.


## Data objects

TempoIQ uses a simple two-level data hierarchy, consisting of Devices and Sensors.

    [[ Simple high-level graphic showing backend ]]
    [[ with many devices; devices with many sensors ]]

### Devices

A device generally corresponds to a discrete physical unit that has one or more associated sensors. For example: solar panels, vehicles, or activity monitors.

Each device is required to have a globally unique key. Good choices for device keys include serial numbers, UUIDs, and other identifiers that will not change or conflict with other devices.

In addition to a key, you can define attributes on a device. Attributes allow you to add additional metadata to a device, and construct powerful analytics queries by analyzing many devices at once. Examples of possible attributes include user ID, geographic region, and device model number.


### Sensors

A sensor corresponds to a single measurement coming from a specific device. For example: internal temperature, DC voltage, or wind speed.

A sensor is required to have a key unique within its device. Sensors can be referenced by the combination of device key and sensor key. There is no concept of a sensor that is not associated with a device.

In addition to a key, you can define additional attributes on a sensor. Sensor attributes should describe the specific sensor, rather than the device as a whole. Examples of possible sensor attributes include measurement unit, calibration offset, or sensor location (if the location doesn't apply to the overall device).

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
    building: "444",
    floor: "main"
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
