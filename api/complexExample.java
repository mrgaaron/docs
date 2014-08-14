/*

Solar microinverter devices convert DC electricity to AC. Several microinverters
are grouped together in an installation, and installations belong to a region.

device schema:
{ attributes: {
    installation: "abc",
    region: "zzz"
  },
  sensors: [
    dcPower,
    acPower,
    dcVoltage,
    acVoltage,
    frequency
  ]
}
 */

/********
Detecting systemic errors from unreliable sensors:
freq sensor is inaccurate, but if 3 inverters in an installation have freq outside
typical range, then there's likely a real problem.
Resulting alerts are scoped to the installation ID.
*/

Selector s = Selector.init()  // All devices

Pipeline pipeline = PipelineBuilder.getSensor("frequency")
                                   .outsideRange(58, 62)
                                   .aggregate(Aggregation.SUM,  // Booleans are 1/0 so sum to get the count of active alerts
                                              Grouping.byDeviceAttribute("installation"))
                                   .gte(3)
                                   .compile();

client.createMonitor(Monitor.getBuilder()
                     .setSelector(s)
                     .setPipeline(pipeline)
                     .setName("frequencyError")
                     .setTrigger(Trigger.webhook("http://example.com/alerts"))
                     .build());


/********
- Underperforming relative to expected efficiency:
The "megamicro" installation is testing a new inverter model, and the engineers
want to be sure the efficiency (acPower / dcPower) is in line with expectations.

If the inverter receives DC power of 10 watts or more, and its efficiency is
below 80%, send an alert.

Device-scope computation. Sensor(s) from a single device yield a new data stream scoped to the same device.
*/

Selector s = Selector.init().filter(Filter.withDeviceAttribute("installation", "megamicro"));

Pipeline pipeline = PipelineBuilder.and(
                          PipelineBuilder.getSensor("dcPower").gt(10),
                          PipelineBuilder.divide(
                                PipelineBuilder.getSensor("acPower"),
                                PipelineBuilder.getSensor("dcPower")  // binding to the same sensor in multiple places
                          ).lt(0.8)
                    ).compile();

// Same Monitor construction as above

/*******
- Underperformance relative to other panels in installation:

If a panel's AC power is 20% below the installation's average for 30 minutes, send an alert.
*/

Selector s = Selector.init(); // All devices

PipelineBuilder installationMean = PipelineBuilder.getSensor("acPower")
                                                  .aggregate(Aggregation.MEAN,
                                                             Grouping.byDeviceAttribute("installation"))

PipelineBuilder deviceOutput = PipelineBuilder.getSensor("acPower")

Pipeline pipe = PipelineBuilder.relativeDifference(deviceOutput, installationMean)
                               .lt(-0.2)
                               .holdTrue(Period.minutes(30))
                               .compile();

// Same monitor construction as above


/*
- Underperforming relative to measured irradiance. Given a solar irradiance value (measured outside the device), we know how much DC power should be generated (panel efficiency).
    * Device-scoped computation with external inputs. Result is scoped to a device, but requires sensor from outside the device.
    * How to find external input for a given device?


- Performance vs. max potential irradiance. Given lat/lng, datetime, and panel orientation, we can model expected irradiance and therefore production.
If deviation between expected production and actual is > X% AND if expected prod is > Y Watts, then alert.
    * Modeled production is scoped to device, but with no inputs from device. All fixed parameters. When to recompute?

- Installation underperforms relative to nearby installs: Each installation has a set of other installations that are nearby (region attribute).
They should be subject to roughly the same weather, sun exposure, etc. so energy production should be correlated. Each region has an expected
production (normalized... per sqft panel). Mean, max, or 90% of production in the region. Highlight installations which are < E% of expected production.
    * ?!?!?! comparing one aggregation computation to another with a different scope!!
*/
