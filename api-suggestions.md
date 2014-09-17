Selection/selector/search - single object (selector), flatten sensor/device selectors,
don't need a different object name for the combination. That's a special case.

Attributes selector is an implicit AND. Make an object for a single attribute,
combine with ANDs. e.g:
```
{ "search": {
  "and": [
    {"type": "sensor", "key": "temperature"},
    {"type": "device", "attribute": "building", "value": "12A"},
    {"type": "device", "attribute": "model", "value": {"in": {"v1", "v2", "v2.2"}}}
  ]
}}
```

ValueSelectors



end/stop terminology: use "start" and "end"; do something else in ruby


Monitoring:

* rename "alert" field to "grouping" or "grouping_scheme"
* default grouping to "device"
* filter has a type, but trigger has a name. Should be consistent (I prefer type)
* Does there need to be more than one action?
* Why can't a Streamfilter object be the top-level "filter"? It needs to be wrapped in an AND
* Devices and Sensors are capitalized in returned search
* concerning that re-serialized rule looks different. esp. condition filter
* Listing rules returns map of key to name. Not very useful. Status? ...



Bugs:

* POST new rule returns 500 if specifying a key
* get logs returns 500 when specifying range, weird 400 if not
* 500 when specifying freshness in a rule
