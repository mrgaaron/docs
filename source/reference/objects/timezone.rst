=========
TimeZone
=========

.. class:: TimeZone

TempoIQ supports the full list of time zones provided in the
`Olson database <http://www.twinsun.com/tz/tz-link.htm>`_.
A list of supported time zones is given below.

Note that the colloquial North American time zones (EDT, EST, CDT, CST, MDT,
MST, PDT, PST) are not directly supported because they are not specified by
ISO 8601. These are ambiguous. For instance, CST can either mean Central
Standard Time in the United States or China Standard Time in China. For this
reason, the Olson naming conventions are used. If the colloquial abbreviations
are required, a lookup table is recommended for conversion.

See: :class:`DateTime`
