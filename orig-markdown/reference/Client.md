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
* Historical read methods
* Monitoring rule CRUD methods

---

### createDevice(device)
`POST /v2/devices/`

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
`GET /v2/devices/:key/`

Gets a device.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| key | String | The key of the device to get |

#### Returns
The `Device` with the provided key.


### updateDevice(device)
`PUT /v2/devices/:key/`

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
`DELETE /v2/devices/:key/`

Deletes all the device's metadata, sensors, and sensor data.

| Argument | Type | Description |
| -------- | ---- | ----------- |
| device | `Device` | The device to delete |

#### Returns
Nothing

---

### writeData(data)

`POST /v2/write/`

Writes data points to one or more devices and sensors.

If a sensor already has a DataPoint at a given timestamp, writing a new
DataPoint with the same timestamp overwrites the old DataPoint's
value. This means that writes are idempotent, in other words, repeatedly
writing the same data to a sensor does not change what's stored. This
can often simplify your application's write logic, because there's
no risk of data corruption if you happen to write data multiple times.


| Argument | Type | Description |
| -------- | ---- | ----------- |
| data | WriteRequest | Data points to write |

#### Returns
Nothing.

#### Errors
If you attempt to write to a sensor or device that does not exist, or
specify an invalid DataPoint format, a MultiStatus will be returned
indicating which Devices succeeded and which failed in writing.

---

### readData(readRequest)

`GET /v2/read/`

Reads data points from one or more devices and sensors.

| Argument | Type | Description |
| ----- | ------ | ------- |
| readRequest | `ReadRequest` | Parameters for the read operation |
