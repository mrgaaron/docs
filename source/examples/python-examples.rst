
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