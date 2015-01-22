
# snippet-begin create-client

    import tempoiq.session

    client = tempoiq.session.get_session(
                                "https://your-url.backend.tempoiq.com",
                                "your-key",
                                "your-secret")

# snippet-end
# snippet-begin create-device

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

# snippet-end
# snippet-begin single-point

    result = client.query(Sensor) \
                   .filter(Device.key == "device1") \
                   .filter(Sensor.key == "temperature") \
                   .single("before",
                           timestamp=datetime.datetime(2014, 9, 15, 0, 0))

    rows = [row for row in result.data]
    if len(rows) == 0:
        print("No point found!")
    else:
        var row = rows[0]
        var point_time = row.timestamp
        var point_value = row.values['device1']['temperature']
        print("Found point: t={} v={}".format(point_time, point_value))

# snippet-end
# snippet-begin bind-single-stream

    result = client.query(Sensor) \
                   .filter(Device.key == "device1") \
                   .read(start=datetime.datetime(2015, 1, 1),
                         end=datetime.datetime(2015, 1, 1))
    stream1 = result.data.bind_stream(sensor_key='temperature')
    for point in stream1:
        print("Temperature: t={} v={}".format(point.timestamp, point.value))

    stream2 = result.data.bind_stream(sensor_key='humidity')
    for point in stream2:
        print("Humidity: t={} v={}".format(point.timestamp, point.value))


# snippet-end
# snippet-begin bind-all-streams

    result = client.query(Sensor) \
                   .filter(Device.key == "device1") \
                   .read(start=datetime.datetime(2015, 1, 1),
                         end=datetime.datetime(2015, 1, 1))

    for stream in result.data.streams:
        for point in stream:
            print("Device: {}, sensor: {}".format(stream.device.key,
                                                  stream.sensor.key))
            print("Point: t={} v={}".format(point.timestamp, point.value))

# snippet-end
# snippet-begin device-ordering-key

    result = client.query(Device).order_by('key', 'desc').read()

# snippet-end
# snippet-begin device-ordering-date-created

    result = client.query(Device).order_by('date_created', 'asc').read()

# snippet-end
# snippet-begin device-ordering-date-modified

    result = client.query(Device).order_by('date_modified', 'desc').read()

# snippet-end
