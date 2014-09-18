================
Monitoring Rules
================

.. contents::

.. TODO:: write descriptions for monitoring methods

Create monitoring rule
----------------------

.. method:: createMonitor(rule)

   :endpoint: ``POST /v2/monitors``
   :arg MonitorRule rule:
   :returns: The created :class:`MonitorRule`


Get monitoring rule
-------------------

.. method:: getMonitor(key)

   :endpoint: ``GET /v2/monitors/:key``
   :arg String key: Key of the monitoring rule to get
   :returns: The :class:`MonitorRule` with the provided key

List monitoring rules
---------------------

.. method:: listMonitors()

   :endpoint: ``GET /v2/monitors``


Update monitoring rule
----------------------

.. method:: updateMonitor(rule)

   :endpoint: ``PUT /v2/monitors/:key``
   :arg MonitorRule rule: The updated rule
   :returns: The updated rule


.. method:: setMonitorStatus(key, status)

   :endpoint: ``PUT /v2/monitors/:key/status``
   :arg String status: 


Delete monitoring rule
----------------------

.. method:: deleteMonitor(key)

   :endpoint: ``DELETE /v2/monitors/:key``
