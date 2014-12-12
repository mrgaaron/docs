
.. snippet:: create-client ruby

    require 'tempoiq/client'
    client = TempoIQ::Client.new("key", "secret", "backend.tempoiq.com")

.. snippet:: create-device ruby

    device = client.create_device('heatpump4789', 'Basement Heat Pump',
                                  'building' => '445 W Erie', 'model' => '75ZX',

                                  TempoIQ::Sensor.new('temp-1'), TempoIQ::Sensor.new('pressure-1'))

.. snippet:: single-point ruby

    ts = Time.utc(2014, 9, 15, 2, 0, 0)

    selection = {
      :devices => {:key => "device1"}
      :sensors => {:key => "temperature"}
    }

    client.single(selection, :before, ts)
