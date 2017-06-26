Responce description
===============================

After a merchant has posted RIS information to Kount, a key-value pair
string will be returned back to the merchant. The RIS response format
will be the same that was specified in the RIS request, with the default
being named pairs. Each data field must be invoked by getter methods on
the ``Response`` object from the SDK. The merchant can then use the RIS
response to automate the order management process by keying off of the
``AUTO`` field and can utilize any of the additional data returned for
internal processing.

An important use of the RIS response is the ability to view any warnings
or errors that were made during the RIS post from the merchant. All
warnings will be displayed in the response and if errors do occur the
RIS response will be returned with a ``MODE = E`` /if
inquiry.params["FRMT"] is not set/ or {"MODE": "E", "ERRO": "201"} /if
inquiry.params["FRMT"] = "JSON"/. More information on warnings and
errors can be found at the :ref:`Troubleshooting` section.

Response.get\_errors() returns error list.
