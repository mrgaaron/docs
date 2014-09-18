Credentials
===========

.. class:: Credentials

In order to send read or write requests to your TempoIQ backend, you must
supply a valid set of Credentials. A backend can have multiple credentials
with different permissions, for example, read-only or write-only. For
more information on issuing credentials, see the :doc:`Administration Guide
</guides/administration>`.

In the HTTP API, supply your credentials in each request via HTTP
Basic Authentication.
Provide the key as the username and the secret as the password.


Fields
------

=======  =======  ========
Name     Type     Description
=======  =======  ========
key      String   API key, typically a 32-character string
secret   String   API secret, typically a 32-character string
=======  =======  ========
