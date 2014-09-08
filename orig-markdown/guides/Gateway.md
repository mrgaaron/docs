# Writing via a gateway

TODO: Guide on the gateway pattern of writing to TempoIQ.


Sometimes, it's not feasible for deployed devices to write data directly to
TempoIQ. A common solution is to use a gateway server to ingest and queue data
from all devices, and periodically forward the queued data to TempoIQ. This
method is well suited for that use case, because the gateway can simply maintain
a single queue for data from all devices, flushing the queue with a single
writeData call. 
