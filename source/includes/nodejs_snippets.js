// snippet-begin create-client
var tempoiq = require('tempoiq');
var client = tempoiq.Client("my-key", "my-secret", "my-company.backend.tempoiq.com");
// snippet-end

// snippet-begin pipeline-concept

    var pipe = new tempoiq.Pipeline.rollup("mean", "1hour", start);
    client.read(selector, start, end, pipe, callback);

// snippet-end
