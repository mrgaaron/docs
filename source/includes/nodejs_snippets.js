// snippet-begin pipeline-concept

    var pipe = new tempoiq.Pipeline.rollup("mean", "1hour", start);
    client.read(selector, start, end, pipe, callback);

// snippet-end
