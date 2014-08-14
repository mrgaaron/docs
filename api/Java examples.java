class Collection {

}


class Pipeline {

}

class PipelineBuilder<T> {
    /**
     * Create a new empty pipeline
     */
    public PipelineBuilder();

    /**
     * Begin a new pipeline path with a given sensor.
     */
    static PipelineBuilder<Value> getSensor(String key);

    /**
     * Begin a new pipeline path with sensors matching the given filter.
     */
    static PipelineBuilder getSensors(Filter f);

    /**
     * Combine pipelines with the specified CombineOperation. Some operations
     * only support a certain number of input PipelineBuilders.
     */
    static PipelineBuilder combine(CombineOperation op, PipelineBuilder... pipes);

    /**
     * Converts this PipelineBuilder to a Pipeline object that can be
     * evaluated by TempoIQ
     */
    Pipeline<T> compile();

    /**
     * Computes the exponential moving average of a stream.
     */
    PipelineBuilder<Value> expAvg(Period p);

    /**
     * Converts a value stream into a boolean stream, where the result will be
     * True if the input stream's value is above V.
     */
    PipelineBuilder<Boolean> gt(Value v);

    /**
     * Converts a value stream into a boolean stream, where the result will be
     * True if the input stream's value is below V.
     */
    PipelineBuilder<Boolean> lt(Value v);

    /**
     *
     */
    PipelineBuilder aggregate(Aggregation agg, Grouping grp)

}

class Grouping {
    /**
     * Group together streams belonging to the same device.
     */
    static Grouping byDevice();

    /**
     * Group streams across devices according to their sensor key.
     */
    static Grouping bySensorKey();

    static Grouping byDeviceAttribute(String attr);

    static Grouping bySensorAttribute(String attr);
}

/**
 * Aggregations are type-specific. These only make sense for values.
 */
enum Aggregation {
    SUM, MAX, MIN, MEAN, STDDEV, LAST
}


/*** Example 1 - port blake's monitoring example ***/

// Version 1 - name each pipeline stage
PipelineBuilder<Value> voltage = PipelineBuilder.getSensor("voltage");
PipelineBuilder<Value> vSmoo = voltage.expAvg(Period.minutes(15));

PipelineBuilder<Value> current = PipelineBuilder.getSensor("current");

PipelineBuilder<Boolean> overVoltage = voltage.gt(128);
PipelineBuilder<Boolean> underCurrent = current.lt(2.3);

PipelineBuilder<?> query = new PipelineBuilder();

Pipeline<Boolean> out = PipelineBuilder.combine(CombineOperation.AND,
                                                overVoltage,
                                                underCurrent).compile();

MonitorRule rule = Monitor.getBuilder()
                        .setDevices(devices)
                        .setPipeline(out)
                        .setTrigger(Trigger.webhook("http://example.com/alerts"))
                        .setName("weGotAProblemHere")


// Version 2: Less verbose
Pipeline<Boolean> out = PipelineBuilder().combine(
        CombineOperation.AND,
        PipelineBuilder.getSensor("voltage")
                .expAvg(Period.minutes(15))
                .gt(128),
        PipelineBuilder.getSensor("current").
                .lt(2.3)
    ).compile();


// Version 3: AST
{
    pipeline: {
        $and: [{
            "current": {
                $lt: 2.3
            }
        },
        {
            "voltage": [
                { $expAvg: {period: "PT15M"} }, // pipeline operations are expressed
                { $gt: 128 }                    // as ordered elements in an array.
            ]
        }]
    }
}







/*** Example 2: Total output across each installation in a region ***/

// If collections have types, how to express?
Collection devices = Collection.getBuilder()
        .filter(Filter.withAttribute("region", "evanston"))
          .and(Filter.withAttribute("type", "inverter")).compile();

// I think this is just as valid as the above selection?
Collection devices = Collection.getBuilder()
                        .and(
                            Filter.withAttribute("region", "evanston"),
                            Filter.withAttribute("type", "inverter")
                        ).compile();




PipelineBuilder<Value> pipeline = PipelineBuilder.getSensor("ac_power")
                            .aggregate(Aggregation.SUM,
                                       Grouping.byDeviceAttribute("installation"));


// Historical read:
Pipeline<Value> rolledUp = pipeline.rollup(Period.hours(1), Fold.MEAN).compile();
Response<?> = client.historical(devices, rolledUp, start, end);
    // Result is a table where columns are the installation IDs and rows are timestamps

// Alert when above fixed value
Pipeline<Boolean> monitor = pipeline.gt(450).holdTrue(Period.minutes(10)).compile();

MonitorRule rule = Monitor.getBuilder()
                        .setDevices(devices)
                        .setPipeline(monitor)
                        .setTrigger(Trigger.webhook("http://example.com/alerts"))
                        .setName("OverCapacity")
                        .setAttribute("severity", "warning")    // Monitor attributes are useful for
                                                                // retreiving monitor rules later on
                                                                // and providing context to webhooks
                        .build();
Response<None> = client.enableMonitor(rule);    // normal CRUD on MonitorRule objects

