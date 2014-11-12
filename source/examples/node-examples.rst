
.. snippet:: create-client javascript

    var tempoiq = require('tempoiq');
    var client = tempoiq.Client(<TEMPO_KEY>,
                                <TEMPO_SECRET>,
                                <TEMPO_HOST>);


.. snippet:: create-device javascript

    client.createDevice(new tempoiq.Device("device", {
        name: "My Awesome Device",
        attributes: {building: "1234"},
        sensors: [
          new tempoiq.Sensor("sensor1", {
            name: "My Sensor",
            attributes: {unit: "F"}
          }),
          new tempoiq.Sensor("sensor2", {
            name: "My Sensor2",
            attributes: {unit: "C"}
          })
        ]
      }),
      function(err, device) {
        if (err) throw err;
        callback(device);
      }
    );
