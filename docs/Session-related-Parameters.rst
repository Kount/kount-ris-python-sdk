Session related Parameters
==================================

There are a few parameters responsible for maintaining connection
between linked interactions with the RIS. They are transported as a part
of the ``Request/Response`` objects during standard RIS communication.

-  ``SESS`` parameter
   This parameter should be created by the merchant at the start of each
   new customer purchase. ``SESS`` is used to join the customer device
   data with the order data sent with the RIS request. If the merchant
   uses the Kount [[Data Collector]] service to obtain customer device
   information, then the same ``SESS`` value must be used for all RIS
   calls starting with the one to the Data Collector service.
   Requirements for the parameter value are:
-  alpha-numeric
-  length: 1-32 characters
-  value should be unique over a thirty-day period of time ``SESS`` is a
   mandatory parameter set by ``Request.session_set(string)`` method.

-  ``TRAN`` parameter The ``TRAN`` parameter is required for ``Update``
   calls to Kount RIS. Its value is created by Kount and is returned
   within the ``Response`` object for the first RIS ``Inquiry``. For all
   subsequent events, modifying this particular customer order, the
   'TRAN\` parameter should be set to the Kount-created value.
