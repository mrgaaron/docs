
// snippet-begin create-client
    using TempoIQ;
    var client = new Client("my-key", "my-secret", 
                            "my-company.backend.tempoiq.com");

// snippet-end

// snippet-begin create-device

    attributes = new Dictionary<String, String>();
    attributes.Add("model", "v1");

    sensor1 = new Sensor("temperature");
    sensor2 = new Sensor("humidity");
    sensors = new List<Sensor> {sensor1, sensor2};

    device = new Device("thermostat.0", "", attributes, sensors)

    client.CreateDevice(device);
// snippet-end

// snippet-begin single-point
    var selection = new Selection()
                        .Add(Select.Type.Devices, Select.Key("device1"))
                        .Add(Select.Type.Sensors, Select.Key("temperature"));

    var timestamp = UTC.AtStrictly(new LocalDateTime(2014, 9, 15, 2, 0, 0, 0));
    var single = new SingleValueAction(DirectionFunction.Before, timestamp);

    client.Single(selection, single);
    foreach (var row in cursor) {
      Console.WriteLine(String.Format("The latest point for 'device1.temperature` is: {0}", row.getValue("device1", "temperature")));
    }
// snippet-end
