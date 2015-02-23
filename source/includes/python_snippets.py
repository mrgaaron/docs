
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

    temp_sensor = Sensor("temperature")
    humid_sensor = Sensor("humidity")

    device = Device("thermostat.0",
                    attributes={"model": "v1"},
                    sensors=[temp_sensor, humid_sensor])
    response = client.create_device(device)

    if response.successful != tempoiq.response.SUCCESS:
        print("Error creating device!")

# snippet-end

# snippet-begin write-data
    import datetime
    from tempoiq.protocol.point import Point

    t1 = datetime.datetime(2015, 1, 1, 0, 0)
    t2 = t1 + datetime.timedelta(minutes=5)

    device_data = {"temperature": [Point(t1, 68), Point(t2, 67.5)],
                   "humidity": [Point(t1, 71.5), Point(t2, 70.0)]}

    response = client.write({"thermostat.0": device_data})

    if res.successful != tempoiq.response.SUCCESS:
        print("Error writing data!")
# snippet-end
# snippet-begin get-devices
    from tempoiq.protocol.device import Device
    from tempoiq.protocol.sensor import Sensor
    from tempoiq.protocol.query.selection import and_, or_

    regions = or_([Device.attributes["region"] == "south",
                  Device.attributes["region"] == "east"])

    result = client.query(Device) \
                   .filter(regions) \
                   .read()

    for dev in result.data:
        print("Got device with key: {}".format(dev.key))
# snippet-end

# snippet-begin update-device
from tempoiq.protocol.device import Device

result = client.query(Device).filter(Device.key == "thermostat.4").read()
device = result.data.next()

device.attributes["customer"] = "internal-test"
device.attributes["region"] = "east"

client.update_device(device)

# snippet-end

# snippet-begin delete-devices
from tempoiq.protocol.device import Device
result = client.query(Device).filter(Device.key == "thermostat.5").delete()
# snippet-ignore TODO: show how to access # of deleted devices
# snippet-end
# snippet-begin delete-data
from tempoiq.protocol.sensor import Sensor

start = datetime.datetime(2015, 1, 5, 0, 0)
end = datetime.datetime(2015, 1, 5, 1, 0)

response = client.query(Sensor).filter(Device.key == "thermostat.1") \
                               .filter(Sensor.key == "humidity") \
                               .delete(start, end)
# snippet-end
# snippet-begin single-point
    from tempoiq.protocol.device import Device
    from tempoiq.protocol.sensor import Sensor

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
    from tempoiq.protocol.device import Device
    from tempoiq.protocol.sensor import Sensor

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

# snippet-begin read-data-one-device
    from tempoiq.protocol.device import Device
    from tempoiq.protocol.sensor import Sensor

    result = client.query(Sensor) \
                   .filter(Device.key == "thermostat.0") \
                   .read(start=datetime.datetime(2015, 1, 1),
                         end=datetime.datetime(2015, 1, 2))

    for row in result.data:
        for ((device, sensor), value) in row:
            print(row.timestamp, device, sensor, value)
# snippet-end

# snippet-begin read-data-streams
    from tempoiq.protocol.device import Device
    from tempoiq.protocol.sensor import Sensor

    result = client.query(Sensor) \
                   .filter(Device.key == "device1") \
                   .read(start=datetime.datetime(2015, 1, 1),
                         end=datetime.datetime(2015, 2, 1))

    for stream in result.data.streams:
        for point in stream:
            print("Device: {}, sensor: {}".format(stream.device.key,
                                                  stream.sensor.key))
            print("Point: t={} v={}".format(point.timestamp, point.value))

# snippet-end
# snippet-begin device-ordering
    from tempoiq.protocol.device import Device

    #query by device key, descending order
    result = client.query(Device).order_by('key', 'desc').read()

    #query by when the device was created, ascending order
    result = client.query(Device).order_by('date_created', 'asc').read()

    #query by when the device was last modified, descending order
    result = client.query(Device).order_by('date_modified', 'desc').read()

# snippet-end

# snippet-begin pipeline
# Specify pipeline functions fluently in the QueryBuilder
from tempoiq.protocol.sensor import Sensor
result = client.query(Sensor).filter(filter) \
                             .rollup("max", "1hour") \
                             .read(start=start, end=end)
# snippet-end
