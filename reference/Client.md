# Client

The main entry point to the TempoIQ API.


 * Retrieve a filtered list of `Sensor`s
 * Retrieve a Sensor by key
 * Retrieve datapoints for a single sensor in a specific time interval
 * Write datapoints for a single sensor
 * Retrieve datapoints aggregated across multiple Sensors
 * Write datapoints to multiple Sensor

## Fields

| Name | Type | Description |
|------|------|-------------|
| credentials | `Credentials` | API key and secret |
| host | String | URL prefix for the TempoIQ backend, in the format "https://cust-id.backend.tempoiq.com" |

## Methods

* Device CRUD methods
* Data write methods
* Historical read and analysis methods
* Monitoring rule CRUD methods

---

### createDevice(device)
Creates a device. Creating a device with the same key as an existing device
results in an error. If the device does not contain a key, one will be
generated.

#### Arguments

| Name | Type | Description |
| -------- | ---- | ----------- |
| device | `Device` | The device to create |

#### Returns
The `Device` that was created.


### getDevice(key)
Gets a device.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| key | String | The key of the device to get |

#### Returns
The `Device` with the provided key.


### updateDevice(device)
Updates a device with the provided metadata and sensors. To safely modify just
some of a device's properties, it is recommended to use this method in a
*GET-modify-PUT* pattern. First, get the device object using getDevice or
similar. Then, modify the metadata or sensors as desired. Finally, update the
device on the server with this method.

A device's key is immutable, so it is not possible to change a device
key with this method. Calling updateDevice with a key that does not already
exist in TempoIQ results in an error.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| device | `Device` | The updated device |

#### Returns
The updated `Device`


### deleteDevice(device)
Deletes all the device's metadata, sensors, and sensor data.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| device | `Device` | The device to delete |

#### Returns
Nothing

---

### writeDeviceData(device, data)
Writes one or more data points to one or more sensors on the given device.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| device | `Device` | The device to write |
| data | Array of `MultiDataPoint` |

#### Returns
Nothing


### writeData(data)
