
.. snippet:: create-client python

    import tempoiq.session

    client = tempoiq.session.get_session(
                                "https://your-url.backend.tempoiq.com",
                                "your-key",
                                "your-secret")


.. snippet:: create-device python

    from tempoiq.protocol.device import Device
    from tempoiq.protocol.sensor import Sensor
    import tempoiq.response

    temp_sensor = Sensor("temperature", attributes={"unit": "degC"})
    humid_sensor = Sensor("humidity", attributes={"unit": "percent"})

    device = Device("thermostat-12345",
                    attributes={"type": "thermostat", "building": "24"},
                    sensors=[temp_sensor, humid_sensor])
    response = client.create_device(device)

    if response.successful != tempoiq.response.SUCCESS:
        print("Error creating device!")


.. snippet:: single-point python

    result = client.query(Sensor) \
                   .filter(Device.key == "device1") \
                   .filter(Sensor.key == "temperature") \
                   .single("before",
                           timestamp=datetime.datetime(2014, 9, 15, 0, 0))

    rows = [row for row in result.data]
    if len(rows) == 0:
        print("No point found!")
    else:
        var row = rows[0];
        var point_time = row.timestamp;
        var point_value = row.values['device1']['temperature']
        print("Found point: t={} v={}".format(point_time, point_value))
    

