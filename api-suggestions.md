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

Monitoring... 
