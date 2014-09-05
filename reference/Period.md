# Period

TempoIQ supports two different formats for expressing time periods as strings:
Simple format and ISO 8601 durations.

## Simple Format

Specify a period with a number and a unit of time, e.g. `6hour` or `1day`.
The supported time units are:

* min - Minutes
* hour - Hours
* day - Days
* month - Months
* year - Years


## ISO 8601 Durations

ISO 8601's duration format allows for specifying more complex periods.
For example:

* 6hour is represented as `PT6H`
* 1day is represented as `P1D`
* 1 minute and 15 seconds is represented as `PT1M15S`, or more concisely `PT75S`
* 2 weeks is represented as `P2W`

For a detailed description of the duration format, see the
[ISO 8601 Wikipedia page](http://en.wikipedia.org/wiki/ISO_8601#Durations).


## API Libraries

TempoIQ's libraries may use language-specific Period implementations. See the
library's documentation for details.


See: `DateTime`
