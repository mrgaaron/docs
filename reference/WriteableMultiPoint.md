# WriteableMultiPoint

An object containing data from several sensors on a device at a single
timestamp. It is not required to specify a value for every Sensor on a
device.

See `Client.writeDeviceData`

## Fields
| **Name** | **Type** | **Description** |
| ---- | ----- | ---- |
| timestamp | DateTime | The time of the measurements |
| values | Map of Sensor=>Number | A collection associating sensors to their respective measured values |
