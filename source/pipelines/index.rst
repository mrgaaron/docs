:orphan:

=================
TempoIQ Pipelines
=================


*Pipelines* is a new service from TempoIQ, and we are inviting you
to be among the first to try it.

Pipelines enable you to analyze and visualize your sensor data in realtime.

.. image:: /images/pipelines.png

The process is simple:

1. Define a pipeline to calculate a streaming metric based on your live sensor data, 
   such as average temperature in a building or total energy generated today.
2. Get push updates in a graph or via an API as your devices
   write new data. That's it!

We'll go into a few specific examples shortly, but first we'll cover the three
basic components of the Pipelines system: events, analytics, and publishers.

Events
------

You send data to the Pipelines system as a sequence of events. An event is
a JSON object, which can contain any number of attributes containing measurements, 
metadata, or nested objects.

For example:

.. code::

   {
     "deviceType": "thermostat",
     "serialNumber": "X3251821",
     "userInfo": {
       "id": 1423,
       "region": "south"
     },
     "currentTemp": 71.0,
     "currentHumidity": 65.0
   }

There are very few limitations on how you structure events---they're meant
to work seamlessly with data formats that you already use in your application.
There's no need to pre-define devices or channels with this event model. All
data is contained within the event itself.

When you send an event to TempoIQ, we automatically add a timestamp. If you
want to provide your own timestamp, for instance, if you are batching events
over time and writing many at once, you can override it through a special timestamp
field. 


Analytics
---------

Analytics calculate specific metrics from the raw stream of input
events. They can filter for a subset of events, group into 
sub-streams based on data in the events, and aggregate values
over time or across devices. 

Example: For each *userInfo.region*, find the average *currentTemp* of all
events so far this hour.

Analytics are persistent operations. In other words, after you've 
defined an analytic, it will continue to process new events and emit 
updated results.

.. note:: For the initial trial program, TempoIQ engineers will manually configure
   analytics in your Pipelines environment. Future releases will allow you to
   define your own analytics through a web UI or API.


Publishers
----------

Once you set up your analytics, you can subscribe to updates through a publisher.
We support a graphical publisher--a dashboard website with a streaming graph--
and a websocket publisher for your applications to consume directly. In either case, 
you receive updates continously as long as you're subscribed. 

If you have analytics that group the input events into sub-streams, you can subscribe to
just a single stream. Using the example above, you could stream a graph showing
only the average temperature for the *south* region.


.. comment
   Pipeline sifts through all data as it comes in
   Collector?
   Broadcast outputs? Publish?
   Word for output? value, result, calculation


Examples
--------

A solar company collects data from its inverters and sends it to TempoIQ in the following format:

.. code::

   {
     "_$_ts": "2015-04-29T13:01:00Z",  // Optional
     "inverter_id": "asdf12345", 
     "installation": "3425",
     "measurements": {
       "voltage": 118.2,
       "ac_power": 410.0,
       "dc_power": 429.5,
       "energy": 0.35
     }
   }

They want to have access to several realtime metrics:

Single device dashboard
~~~~~~~~~~~~~~~~~~~~~~~

A dashboard for an inverter which continuously updates with the latest value for 
each measurement. Given an inverter ID, they can subscribe to raw events to display
in gauges or graphs.

Instantaneous totals
~~~~~~~~~~~~~~~~~~~~

Track the total power being generated for the entire install base by summing the latest 
*ac_power* value across all devices.


Cumulative production
~~~~~~~~~~~~~~~~~~~~~

A feed showing an installation's total energy production for the day. Given an 
installation ID, sums all *energy* values from events today from that installation. 
This will continuously increase throughout the day and reset at midnight.


Next steps
----------

.. toctree::
   :titlesonly:

   getting-started
   http
   mqtt
   konekt
