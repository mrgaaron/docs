==========================
Frequently Asked Questions
==========================

**Can I query TempoIQ directly from Javascript in the browser?**

Currently, our cross-origin policy does not allow this. This is because it would
require you to send your backend credentials to the user's browser. In the future
TempoIQ will allow you to create read-only credentials for client-side usage.

**How many data points can I write in a single request?**

The exact number can vary based on the length of sensor and device keys, but
typically it's possible to write several thousand points in a single request.
