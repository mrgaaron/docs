## Aggregation operations

An aggregation operation combines streams in a pipeline, by computing the average,
min, max, or other function across several streams. Aggregations can either combine all streams,
resulting in a pipeline with a single stream, or can aggregate streams into several
resulting streams by grouping them by device or attribute.

An aggregation takes two parameters: a grouping and a folding function.

### Groupings

A grouping is similar to a GROUP BY statement in SQL.
It indicates which of the input streams should be combined together, based
on the stream's metadata. The following table lists the supported groupings
and a use case for each one based on a `MEAN` aggregation for the smart thermostat example:

| Grouping    | Use case |
| ------------| ---------|
| `all`         | Results in one stream outputting the average value across every thermostat.
| `device`      | Results in one stream per device, each outputting the average temperature across all sensors on the device. |
| `device_attribute("site")` | Results in one stream for each value of the **site** attribute. Each stream outputs the average temperature across all sensors and devices with that **site** value.

Since an aggregation combines many streams into fewer streams, the resulting
streams generally do not originate from a single device or sensor. Therefore,
the streams' metadata only includes fields that are the same for all streams in
a group. For example, if you're grouping streams from many devices by the "site" attribute,
the metadata is only guaranteed to contain the "site" attribute value.


### Folding functions

After the input streams are grouped, the folding function combines all their values
into a single output value. All common statistical functions are supported as folding
functions: *mean, sum, max, min, stddev,* etc.

NOTE: The folding function computes the aggregation across all of the
input streams that have a data point at the same timestamp.
This can pose a problem if the timestamps of the input streams do not line up,
or if some data is missing. Therefore, it's common to use the **interpolate**
pipeline operation before an aggregation to produce streams with data points at
the same regular interval.
