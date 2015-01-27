
# snippet-begin create-client
    require 'tempoiq/client'
    client = TempoIQ::Client.new("my-key", "my-secret", "my-company.backend.tempoiq.com")
# snippet-end

# snippet-begin create-device
device = client.create_device('thermostat.0', '',
                              'model' => 'v1',
                              TempoIQ::Sensor.new('temperature'), 
                              TempoIQ::Sensor.new('humidity'))
# snippet-end
# snippet-begin single-point

    ts = Time.utc(2014, 9, 15, 2, 0, 0)

    selection = {
      :devices => {:key => "device1"}
      :sensors => {:key => "temperature"}
    }

    cursor = client.single(selection, :before, ts).to_a
    puts cursor[0].value("device1", "temperature")
# snippet-end
