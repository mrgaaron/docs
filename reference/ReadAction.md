# ReadAction

Specifies the range of data to read in a `ReadRequest`.

See: `ReadRequest`

## Fields

| Name | Type | Description |
| ---- | ------ | -------- |
| start | DateTime | Required. The first timestamp to read (inclusive) |
| end | DateTime | Required. The last timestamp to read (exclusive) |

## Example

Read data from January 1 through January 10, 2014

```json
{
  "start": "2014-01-01T00:00:00Z",
  "end": "2014-01-11T00:00:00Z"
}
```
