Here we discuss the request types supported by the Kount RIS Python SDK
and mandatory/optional parameters.

Request types
=============

There are two major ``Request`` types: ``Inquiry`` and ``Update``. Their
handling by the RIS service can be configured by setting the ``MODE``
parameter to the correct value.

``Inquiry`` type should be used for initial registration of the purchase
in the Kount system. It has four available values for the ``MODE``
parameter.

+-------------+-------------------------+---------------------------------------+
| ``Inquiry   | SDK Constant            | Description                           |
| MODE``      |                         |                                       |
+=============+=========================+=======================================+
| ``Q``       | ``INQUIRYMODE.DEFAULT`` | Default inquiry mode, internet order  |
|             |                         | type                                  |
+-------------+-------------------------+---------------------------------------+
| ``P``       | ``INQUIRYMODE.PHONE``   | Used to analyze a phone-received      |
|             |                         | order                                 |
+-------------+-------------------------+---------------------------------------+
| ``W``       | ``INQUIRYMODE.WITHTHRES | Kount Central full inquiry with       |
|             | HOLDS``                 | returned thresholds                   |
+-------------+-------------------------+---------------------------------------+
| ``J``       | ``INQUIRYMODE.JUSTTHRES | Kount Central fast inquiry with just  |
|             | HOLDS``                 | thresholds                            |
+-------------+-------------------------+---------------------------------------+

``Update`` type should be used whenever there are changes to a given
order and the merchant wants them reflected into the Kount system.
``Update`` has two available values for the ``MODE`` parameter.

+------------+--------------------+---------------------------------------------+
| ``Update   | SDK Constant       | Description                                 |
| MODE``      |                    |                                             |
+============+====================+=============================================+
| ``U``      | ``UPDATEMODE.NO_RE | Default update mode, only sends the update  |
|            | SPONSE``           | event                                       |
+------------+--------------------+---------------------------------------------+
| ``X``      | ``UPDATEMODE.WITH_ | Sends the update event and RIS service      |
|            | RESPONSE``         | returns a status response                   |
+------------+--------------------+---------------------------------------------+

Mandatory parameters
====================

+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
| Parameter name | Setter                      | Q        |   P      |   W      |  J       |  U       |  X       |
+================+=============================+==========+==========+==========+==========+==========+==========+
|  MODE          |   set_mode                  | Y        |        Y | Y        |   Y      |    Y     | Y        |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   VERS         | version_set                 | Y        |        Y | Y        |   Y      |    Y     | Y        |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   MERC         | merchant_set                | Y        |        Y | Y        |   Y      |    Y     | Y        |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   SITE         | website                     | Y        |        Y | Y        |          |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   SESS         | session_set                 | Y        |        Y | Y        |          |   Y      |  Y       |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   CURR         | currency_set                | Y        |        Y | Y        |     Y    |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   TOTL         |total_set                    | Y        |        Y | Y        |     Y    |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   MACK         | merchant_acknowledgment_set | Y        |        Y | Y        |          |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   CUSTOMER_ID  |kount_central_customer_id    |          |          | Y        |    Y     |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   PTYP         |                             | Y        |  Y       | Y        |    Y     |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   IPAD         |ip_address 	               |Y         |    Y     | Y        |    Y     |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   TRAN         |set_transaction_id           |          |          |          |          |     Y    |       Y  |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   PROD_TYPE    | :warning:                   |   Y      |  Y       |  Y       |          |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   PROD_ITEM    | :warning:                   |   Y      |  Y       |  Y       |          |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   PROD_QUANT   | :warning:                   |   Y      |  Y       |  Y       |          |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   PROD_PRICE   | :warning:                   |   Y      |  Y       |  Y       |          |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+
|   ANID         | :warning:                   |          |  Y       |          |          |          |          |
+----------------+-----------------------------+----------+----------+----------+----------+----------+----------+



:warning: Parameters marked with this warning sign are the shopping
    cart parameters. They are bulk-set by the ``Inquiry.set_cart(cart)``
    method. If shopping cart contains more than one entry, values for
    each parameter are transformed to single concatenated strings and
    then set to the corresponding parameter.

Optional parameters
===================

The Kount RIS Python SDK provides a huge number of optional request
parameters to increase precision when making a decision about a given
purchase / order.

Only the most interesting parameters will be mentioned here. A
comprehensive listing of all SDK-set parameters can be found on the
python-doc pages for ``Request``, ``Inquiry``, and ``Update`` classes.

-  ``AUTH``: Authorization Status returned to merchant from processor.
   Acceptable values for the ``AUTH`` field are ``A`` for Authorized or
   ``D`` for Decline. In orders where ``AUTH = A`` will aggregate
   towards order velocity of the persona while orders where ``AUTH = D``
   will decrement the velocity of the persona.
-  ``AVST``: Address Verification System Street verification response
   returned to merchant from processor. Acceptable values are ``M`` for
   match, ``N`` for no-match, or ``X`` for unsupported or unavailable.
-  ``AVSZ``: Address Verification System Zip Code verification response
   returned to merchant from processor. Acceptable values are ``M`` for
   match, ``N`` for no match, or ``X`` for unsupported or unavailable.
-  ``CVVR``: Card Verification Value response returned to merchant from
   processor. Acceptable values are ``M`` for match, ``N`` for no-match,
   or ``X`` unsupported or unavailable.
-  ``LAST4``: Last 4 numbers of Credit Card Value.

User-defined fields
===================

Kount provides a way for merchants to include additional information
related to their business that may not be a standard field in Kount by
creating user defined fields. UDFs are created in the Agent Web Console
by browsing to the Fraud Control tab and clicking on User Defined
Fields. Once you have defined the UDF in the AWC you will be able to
pass this data into Kount via an array called UDF as key-value pairs
where the label is the key and the data passed in is the value. The
maximum number of UDFs that can be created is 500, and response time for
evaluating transactions will degrade as more UDFs are added. There are
four data types available for user defined fields.

+--------------------+------+----------------------------+------------------------+
| Attribute          | Size | Description                | Example                |
+====================+======+============================+========================+
| ``UDF[NUMERIC_LABE | 1-255| Numbers, negative signs,   | UDF[FREQUENCY] = 107.9 |
| L] = value``       |      | and decimal points         |                        |
+--------------------+------+----------------------------+------------------------+
| ``UDF[ALPHA_NUMERI | 1-255| Letters, numbers, or both  | UDF[COUPON] = BUY11    |
| C_LABEL = value``  |      |                            |                        |
+--------------------+------+----------------------------+------------------------+
| ``UDF[DATE_LABEL]  | 1-20 | Formatted as               |  UDF[FIRST_CONTACT] =  |
| = value``          |      | ``YYYY-MM-DD`` or          |  2017-04-25 17:12:30   |
|                    |      | ``YYYY-MM-DD HH:MM:SS``    |                        |
+--------------------+------+----------------------------+------------------------+
| ``UDF[AMOUNT_LABEL | 1-255| Integers only, no decimal  |   UDF[BALANCE] = 1100  |
| ] = value``        |      | points, signs or symbols   |                        |
+--------------------+------+----------------------------+------------------------+

Table: warning: UDF labels can be up to 28 characters in length. UDF
labels cannot begin with a number.

--------------

Predictive Response
===================

Predictive Response is a mechanism that can be used by Kount merchants
to submit test requests and receive back predictable RIS responses. This
means that a merchant, in order to test RIS, can generate a particular
request that is designed to provide one or more specific RIS responses
and/or errors. The predictive response inquiries are not actual RIS
inquiries, which means the data will never be submitted to the Kount
internal database.

Please, check the dedicated `Predictive Response <https://github.com/Kount/kount-ris-python-sdk/wiki/Predictive-response.rst>`__ page.
