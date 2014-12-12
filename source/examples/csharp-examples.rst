
.. snippet:: create-client csharp

    using TempoIQ;
    var client = new Client(<TEMPO_KEY>, <TEMPO_SECRET>, <TEMPO_HOST>);

.. snippet:: create-device csharp 

    attributes = new Dictionary<String, String>();
    attributes.Add("building", "1234");

    sensor1Attributes = new Dictionary<String, String>();
    sensor1Attributes.Add("unit", "F");

    sensor2Attributes = new Dictionary<String, String>();
    sensor2Attributes.Add("unit", "C");

    sensor1 = new Sensor("sensor1", sensor1Attributes);
    sensor2 = new Sensor("sensor2", sensor1Attributes);
    sensors = new List<Sensor> {sensor1, sensor2};

    device = new Device("key1234", "My Awesome Device", attributes, sensors)

    client.CreateDevice(device);

.. snippet:: single-point ruby

    var selection = new Selection()
                        .Add(Select.Type.Devices, Select.Key("device1"))
                        .Add(Select.Type.Sensors, Select.Key("temperature"));

    var timestamp = UTC.AtStrictly(new LocalDateTime(2014, 9, 15, 2, 0, 0, 0));
    var single = new SingleValueAction(DirectionFunction.Before, timestamp);

    client.Single(selection, single);
