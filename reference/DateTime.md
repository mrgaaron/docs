# DateTime

Working with time in software can be [surprisingly complex][1].
TempoIQ attempts to abstract away many of these complexities, but it's still
important for application developers to understand some specifics about how
TempoIQ treats time.

Internally, TempoIQ stores all DateTime values in UTC
with millisecond precision. In the HTTP API, DateTimes are represented in
ISO-8601 format, for example, `2014-06-29T00:00:01.000-0500`. 

Where applicable, TempoIQ uses language-specific DateTime implementations
in client libraries. This table shows the DateTime class used in each library:

| Client language | Class |
| ------ | ------- |
| Java | org.joda.time.DateTime |
| Python | datetime.datetime |

Some implementations support "timezone-naïve" DateTime objects. TempoIQ
treats these as UTC DateTimes. To avoid subtle bugs
and inconsistencies, it is always recommended to explicitly specify
time zone information in your application.


[1]: http://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time
