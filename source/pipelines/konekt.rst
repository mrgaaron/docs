=======================
Integrating with Konekt
=======================

Thanks for participating in our Pipelines research project! This reference 
describes the endpoints present in your Pipelines environment.

For a higher-level overview of Pipelines concepts, see :doc:`index`.

For a guide to getting started with Pipelines, see :doc:`getting-started`.

.. contents::
   :local:

Background
----------

TempoIQ Pipelines provides an integration to receive data written to Konekt's 
device connectivity platform.  This integration is turned on by default in every 
Pipelines environment, and requires only some configuration in your Konekt 
dashboard to use.

Steps to Activate
----------------

1.  Log into your Konekt dashboard.  On the left side of the screen, 
    click the *Topics* link.

.. image:: /images/konekt_dashboard1.png

2.  You will see a list an installed apps recognized by Konekt.  Click the 
    *Add App* button.

.. image:: /images/konekt_dashboard2.png

3.  In the *Add App Form* that appears, input a comma separated list of channel 
    names you would like to forward to TempoIQ into the *Topic channels to 
    subscribe to* field.

4.  In the *Select App* drop down, choose the *Custom Webhook URL (Your Own
    App* option.

5.  In the *Destination URL* field, enter::

      http://$ENVIRONMENT.tempoiq.com/channels/$CHANNEL/event

    where *$ENVIRONMENT* is the name of your TempoIQ Environment and *$CHANNEL* 
    is the identifier for your Pipelines channel. 

6.  In the *Webhook Key* field, enter the value *tempoiq-konekt*.

7.  Click the *Install* button.

Below is a sample of a validly completed form:

.. image:: /images/konekt_dashboard3.png

Once the new app has been installed, your devices' messages to the specified 
Konekt topics should automatically begin to be forwarded to your TempoIQ 
Pipelines environment.

Expected Input
--------------

The TempoIQ Konekt plugin will extract the `data` field from the JSON blob that 
Konekt sends and base64 decode it.  The plugin assumes that the decoded payload 
from this field is a valid JSON event as described in :doc:`getting-started`.  
If it is not, your environment will return a 400-class status code describing 
the specific problem encountered in parsing your message.  For example, an 
invalid JSON blob will return a 400, while a valid JSON blob with fields of 
invalid types will return a 422.
