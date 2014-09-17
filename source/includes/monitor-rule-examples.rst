========================
Monitoring rule examples
========================

Create device::

  {
	"key": "untest3",
	"name": "untest device number three",
	"attributes": {
		"type": "untest"},
	"sensors": [
		{"key": "temperature",
		"attributes": {"unit": "DegC"}},
		{"key": "humidity",
		"attributes": {"unit": "percent"}},
		{"key": "pressure"}
	]
}

List devices::

  {
    "search": {
      "select": "devices",
      "filters": {}
    }
  }

Working create monitoring rule::

  {
  "search": {
    "select": "sensors",
    "filters": {
      "devices": {
        "key": "test1"
      },
      "sensors": {
        "key": "temperature"
      }
    }
  },
  "rule": {
    "name": "TempGT52",
    "status": "active",
    "conditions": [ {
      "filter": {
        "and": [ {
          "operation": "select",
          "type": "sensor_key",
          "arguments": ["temperature"]
        } ]
      },
      "trigger": {
        "name": "exp_moving_average",
        "arguments": [
          "static",
          2,
          "gt",
          46
        ]
      }
    } ],
    "actions": [
      {"url": "http://requestb.in/10fbyud1"}
    ]
  },
  "alerts": "sensor"
  }
