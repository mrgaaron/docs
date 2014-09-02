# DateTime

Where applicable, TempoIQ uses language-specific DateTime implementations
in client libraries.

In the HTTP API, DateTimes are represented in ISO 8601 format, with timezone specified.
For example, `2014-06-29T00:00:01.000-0500`

This table shows the DateTime class used in each library:

| Client language | Class | Remarks |
| ------ | ------- | ----- |
| Java | org.joda.time.DateTime | |
| Python | datetime.datetime | Timezone-naive timestamps are treated as UTC |
