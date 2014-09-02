# Sensor

A sensor corresponds to a single measurement coming from a specific device.
For example: internal temperature, DC voltage, or wind speed.

A sensor is required to have a key unique within its device. Sensors
are referenced by the combination of device key and sensor key. There
is no concept of a sensor that is not associated with a device.

In addition to a key, you can define additional attributes on a sensor.



## Fields

| Name | Type | Description |
|------|------|-------------|
| key | String | Required. Identifier for the sensor; unique within a device |
| name | String | Human-readable description |
| attributes | Map of String=>String | Key/value metadata describing the sensor |


### key

Sensor keys are immutable and must be unique. If you delete
a sensor with a given key, it is possible to create a new sensor on the device
with the same key, but the new sensor will not retain the historical data or
metadata of the deleted sensor.

As with all strings in TempoIQ, sensor keys support unicode characters.


### name

Optional field for storing a human-readable description of the sensor. Names
are not required to be unique and may be modified after creating the
sensor.


### attributes

Mutable key/value metadata describing the sensor. Attributes
behave similarly to fields in a schemaless document store like MongoDB.
It's possible to define different attribute keys on different sensors, and
TempoIQ does not enforce the existence of any attributes.

Sensor attributes are not always necessary, but can be useful when it's not
practical to address a sensor by key. For example, a refrigerator controller
device might have between 2 and 5 temperature sensors. To read from all
temperature sensors on a device, it would be easier to select all sensors with
a given attribute value (e.g. "type": "temp") than list all possible sensor
keys (e.g. ["temp1", "temp2", ... ]).

Sensor attributes should describe the specific sensor, rather than the
device as a whole. If the attribute isn't sensor-specific, it should be a
device attribute.
