Predictive Response
======================

Predictive Response is a mechanism that can be used by Kount merchants
to submit test requests and receive back predictable RIS responses. This
means that a merchant, in order to test RIS, can generate a particular
request that is designed to provide one or more specific RIS responses
and/or errors. The predictive response inquiries are not actual RIS
inquiries, which means the data will never be submitted to the Kount
internal database.

An example would be if a merchant wanted to submit a RIS request that
would return the very specific responses ``SCOR = 71``, ``AUTO = E``,
and ``GEOX = CA``.

Predictive Responses are created using the UDF (User Defined Fields)
override option. These User Defined Fields do not need to be created
through the Agent Web Console, they can be simply passed in as
additional fields in the Predictive Response RIS inquiry.

*:warning:*
In order to create a Predictive Response RIS Inquiry, the
request must contain a specific email parameter in the EMAL field:
``predictive@Kount.com``.

All other elements of the RIS request you submit must be valid elements
and contain the minimum set of required RIS keys.

The basic syntax is: ``UDF[~K!_label]="foo"`` ``~K!_`` is the prefix,
``label`` is the desired field for which you want a response, such as
``SCOR`` or ``ERRO``, and after the equal sign (``=``), enter the
specific value you want returned. The ``~K!_`` prefix is required to
trigger the UDF to become a predictive response field.

-  Example 1: You want to send in a request that will result in a Kount
   Score of ``18``, an Auto Decision of ``E``, and a
   ``601 System Error`` code.

Request:

::

        UDF[~K!_SCOR]=18
        UDF[~K!_AUTO]=E
        UDF[~K!_ERRO]=601

Response:

::

        SCOR=18
        AUTO=E
        ERRO=601

-  Example 2: You want to pass in a request that will result in a Kount
   Score of ``42``, an Auto Decision of ``Decline`` and a ``GEOX`` of
   ``Nigeria``.

Request:

::

        UDF[~K!_SCOR]=42
        UDF[~K!_AUTO]=D
        UDF[~K!_GEOX]=NG

Response:

::

        SCOR=42
        AUTO=D
        GEOX=NG

You can use UDF overrides to pass in an unlimited number of mock
requests but all of the fields you pass in that are not overrides must
be valid. In the response, all of the other elements, besides the UDF
overrides will be the default values, including ``MODE`` and ``MERC``.
