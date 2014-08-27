# Client

The main entry point to the TempoIQ API.


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

### writeData(data)
Writes one or more data points to any device and sensor. This is the most
flexible write method, since it can accommodate a collection of points at
multiple timestamps, on multiple different devices.

Sometimes, it's not feasible for deployed devices to write data directly to
TempoIQ. A common solution is to use a gateway server to ingest and queue data
from all devices, and periodically forward the queued data to TempoIQ. This
method is well suited for that use case, because the gateway can simply maintain
a single queue for data from all devices, flushing the queue with a single
writeData call. For a more detailed description
of this design pattern, see the *Writing via a Gateway* guide.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| data | Array of `WriteableDataPoint` | Data points to write |


### writeDeviceData(device, data)
Writes one or more data points to one or more sensors on a given device.
This method is a special case of writeData, where the device is the same for
all points being written.

**Example:**

Every minute, a power meter logs its voltage, frequency, and energy readings and
immediately sends the data to TempoIQ.

```
reading = [ {
              "timestamp": "2014-08-22T12:45:00Z",
              "values": {
                          "voltage": 120.23,
                          "frequency": 59.9,
                          "energy": 4230
                        }
            } ]

client.writeDeviceData(THIS_DEVICE, reading)

```

Note that **reading** is an array. In this example it only contains one
`WriteableMultiPoint` but in general it could contain many.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| device | `Device` | The device to write to |
| data | Array of `WriteableMultiPoint` | Data points to write |

#### Returns
Nothing
