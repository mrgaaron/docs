# Selector

Criteria for selecting objects in a Search.

See: Search, ValueDescriptor

### and
Select an object if it matches all the provided selectors.

Arguments: list of Selectors

### or
Select an object if it matches any of the provided selectors.

Arguments: list of Selectors


### not
Select an object if it does not match the provided selector.

Arguments: Selector


### all
Select all objects in the environment.

Applies to: Device, Sensor

Arguments: none


### key
Select an object if its key matches the provided ValueDescriptor.

Arguments: ValueDescriptor


### attribute
Select an object based on an attribute.
If a value is provided, selects objects where the attribute matches the
ValueDescriptor.
If a value is omitted, select all objects which define the provided
attribute key.

Arguments: key (String, required); value (ValueDescriptor, optional)
