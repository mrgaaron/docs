
// snippet-begin create-client
    import com.TempoIQ;

    Credentials creds = new Credentials("my-key", "my-secret");
    Client client = new Client(creds, "my-company.backend.tempoiq.com", "https");

// snippet-end

// snippet-begin create-device
    Map<String, String> attributes = new HashMap<String, String>();
    attributes.put("model", "v1");

    Sensor sensor1 = new Sensor("temperature");
    Sensor sensor2 = new Sensor("humidity");
    List<Sensor> sensors = new ArrayList<Sensor>();
    sensors.add(sensor1, sensor2);

    Device device = new Device("thermostat.0", "", attributes, sensors)

    client.createDevice(device);
// snippet-end

// snippet-begin single-point
    DateTime timestamp = new DateTime(2014, 9, 15, 2, 0, 0, 0, DateTimeZone.UTC);

    Selection sel = new Selection()
                        .addSelector(Selector.Type.DEVICES, Selector.key("device1"))
                        .addSelector(Selector.Type.SENSORS, Selector.key("temperature"));

    Cursor<Row> cursor = client.single(sel, new Pipeline(), new Single(DirectionFunction.BEFORE, new DateTime(2012, 1, 1, 3, 0, 0, 0, timezone)));
    for (Row row : cursor) {
      System.out.println("The latest point for 'device1.temperature` is: " + row.getValue("device1", "temperature").toString());
    }
// snippet-end
