# ReadRequest

Describes a read operation to perform.

## Fields

| Name | Type | Description |
| -----| ----- | ----- |
| search | `Search` | Required. Selects the sensors to read |
| action | `ReadAction` | Required. Parameters for specifying the time range of data to read |
| pipeline | `Pipeline` | Optional. A sequence of operations to transform the raw sensor data |


## Examples

Read two days of raw data from temperature sensors on devices in the "foo" region:

```json
{
  "search": {
    "devices": {
      "attributes": {
        "region": "foo"
      }
    },
    "sensors": {
      "key": "temperature"
    }
  },
  "action": {
    "start": "2014-09-01T00:00:00Z",
    "end": "2014-09-03T00:00:00Z"
  }
}
```
