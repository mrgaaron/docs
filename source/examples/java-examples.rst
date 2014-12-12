
.. snippet:: create-client java

    import com.TempoIQ;

    Credentials creds = new Credentials(<TEMPO_KEY>, <TEMPO_SECRET>);
    Client client = new Client(creds, <TEMPO_HOST>, "https");

.. snippet:: create-device java

    Map<String, String> attributes = new HashMap<String, String>();
    attributes.put("building", "1234");

    Map<String, String> sensor1Attributes = new HashMap<String, String>();
    sensor1Attributes.put("unit", "F");

    Map<String, String> sensor2Attributes = new HashMap<String, String>();
    sensor2Attributes.put("unit", "C");

    Sensor sensor1 = new Sensor("sensor1", sensor1Attributes);
    Sensor sensor2 = new Sensor("sensor2", sensor1Attributes);
    List<Sensor> sensors = new ArrayList<Sensor>();
    sensors.add(sensor1, sensor2);

    Device device = new Device("key1234", "My Awesome Device", attributes, sensors)

    client.createDevice(device);

.. snippet:: single-point node

    DateTime timestamp = new DateTime(2014, 9, 15, 2, 0, 0, 0, DateTimeZone.UTC);

    Selection sel = new Selection()
                        .addSelector(Selector.Type.DEVICES, Selector.key("device1"))
                        .addSelector(Selector.Type.SENSORS, Selector.key("temperature"));

    client.single(sel, new Pipeline(), new Single(DirectionFunction.BEFORE, new DateTime(2012, 1, 1, 3, 0, 0, 0, timezone)));
