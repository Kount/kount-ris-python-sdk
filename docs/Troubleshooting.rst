An important use of the RIS response is the ability to verify if the
decision-making process was successful and view any warnings or errors
that were made during the RIS post from the merchant. All warnings will
be displayed in the response and if errors do occur the RIS response
will be returned with a ``MODE = E``.

Here's a list of all used RIS warning and error codes.

                        
An important use of the RIS response is the ability to verify if the
decision-making process was successful and view any warnings or errors
that were made during the RIS post from the merchant. All warnings will
be displayed in the response and if errors do occur the RIS response
will be returned with a ``MODE = E``.

Here's a list of all used RIS warning and error codes.

RIS Warning and Error Codes
===========================

+---------------+-----------------------+-----------------------------------------------------+
| Response Code | Warning/Error Label   | Response Code Description                           |
+===============+=======================+=====================================================+
| 201           | ``MISSING_VERS``      | Missing version of Kount, this is built into SDK    |
|               |                       | but must be supplied by merchant if not using       |
|               |                       | the SDK                                             |
+---------------+-----------------------+-----------------------------------------------------+
| 202           | ``MISSING_MODE``      | The mode type for post is missing. Refer to the     |
|               |                       |`Request Types <Request-types-and-Parameters.html>`__|
+---------------+-----------------------+-----------------------------------------------------+
| 203           | ``MISSING_MERC``      | The six digit Merchant ID was not sent              |
+---------------+-----------------------+-----------------------------------------------------+
| 204           | ``MISSING_SESS``      | The unique session ID was not sent                  |
+---------------+-----------------------+-----------------------------------------------------+
| 205           | ``MISSING_TRAN``      | Transaction ID number                               |
+---------------+-----------------------+-----------------------------------------------------+
| 211           | ``MISSING_CURR``      | The currency was missing in the RIS submission      |
+---------------+-----------------------+-----------------------------------------------------+
| 212           | ``MISSING_TOTL``      | The total amount was missing                        |
+---------------+-----------------------+-----------------------------------------------------+
| 221           | ``MISSING_EMAL``      | The email address was missing                       |
+---------------+-----------------------+-----------------------------------------------------+
| 222           | ``MISSING_ANID``      | For ``MODE = P`` RIS inquiries the caller ID is     |
|               |                       | missing                                             |
+---------------+-----------------------+-----------------------------------------------------+
| 223           | ``MISSING_SITE``      | The website identifier that was created in the      |
|               |                       | Agent Web Console (``DEFAULT`` is the default       |
|               |                       | website ID) is missing                              |
+---------------+-----------------------+-----------------------------------------------------+
| 231           | ``MISSING_PTYP``      | The payment type is missing. Refer to the           |
|               |                       | `RIS Payment Types <PaymentTypes.html>`__           |
+---------------+-----------------------+-----------------------------------------------------+
| 232           | ``MISSING_CARD``      | The credit card information is missing              |
+---------------+-----------------------+-----------------------------------------------------+
| 233           | ``MISSING_MICR``      | Missing Magnetic Ink Character Recognition          |
|               |                       | string                                              |
+---------------+-----------------------+-----------------------------------------------------+
| 234           | ``MISSING_PYPL``      | The PayPal Payer ID is missing                      |
+---------------+-----------------------+-----------------------------------------------------+
| 235           | ``MISSING_PTOK``      | The payment token is missing.                       |
+---------------+-----------------------+-----------------------------------------------------+
| 241           | ``MISSING_IPAD``      | The IP address is missing                           |
+---------------+-----------------------+-----------------------------------------------------+
| 251           | ``MISSING_MACK``      | The merchant acknowledgement is missing             |
+---------------+-----------------------+-----------------------------------------------------+
| 261           | ``MISSING_POST``      | The RIS query submitted to Kount contained no       |
|               |                       | data                                                |
+---------------+-----------------------+-----------------------------------------------------+
| 271           | ``MISSING_PROD_TYPE`` | The shopping cart data array attribute is           |
|               |                       | missing.                                            |
+---------------+-----------------------+-----------------------------------------------------+
| 272           | ``MISSING_PROD_ITEM`` | The shopping cart data array attribute is           |
|               |                       | missing.                                            |
+---------------+-----------------------+-----------------------------------------------------+
| 273           | ``MISSING_PROD_DESC`` | The shopping cart data array attribute is           |
|               |                       | missing.                                            |
+---------------+-----------------------+-----------------------------------------------------+
| 274           | ``MISSING_PROD_QUANT``| The shopping cart data array attribute is           |
|               |                       | missing.                                            |
+---------------+-----------------------+-----------------------------------------------------+
| 275           | ``MISSING_PROD_PRICE``| The shopping cart data array attribute is           |
|               |                       | missing.                                            |
+---------------+-----------------------+-----------------------------------------------------+
| 301           | ``BAD_VERS``          | The version of Kount supplied by merchant does      |
|               |                       | not fit the four integer parameter                  |
+---------------+-----------------------+-----------------------------------------------------+
| 302           | ``BAD_MODE``          | The mode type is invalid. Refer to the              |
|               |                       | [RIS  Inquiry Service Modes]-kount/inquiry.py       |
+---------------+-----------------------+-----------------------------------------------------+
| 303           | ``BAD_MERC``          | The six digit Merchant ID is malformed or wrong     |
+---------------+-----------------------+-----------------------------------------------------+
| 304           | ``BAD_SESS``          | The unique session ID is invalid. Refer to the      |
|               |                       | `Data Collector <Data-Collector.html>`__            |
+---------------+-----------------------+-----------------------------------------------------+
| 305           | ``BAD_TRAN``          | Transaction ID number is malformed                  |
+---------------+-----------------------+-----------------------------------------------------+
| 311           | ``BAD_CURR``          | The currency was wrong in the RIS submission        |
+---------------+-----------------------+-----------------------------------------------------+
| 312           | ``BAD_TOTL``          | The total amount is wrong. ``TOTL`` is the whole    |
|               |                       | number amount charged to customer                   |
+---------------+-----------------------+-----------------------------------------------------+
| 321           | ``BAD_EMAL``          | The email address does not meet required format     |
|               |                       | or is greater than 64 characters in length          |
+---------------+-----------------------+-----------------------------------------------------+
| 322           | ``BAD_ANID``          | For ``MODE = P`` RIS inquiries the caller ID is     |
|               |                       | malformed                                           |
+---------------+-----------------------+-----------------------------------------------------+
| 323           | ``BAD_SITE``          | The website identifier that was created in the      |
|               |                       | Agent Web Console (``DEFAULT`` is the default w     |
|               |                       | website ID) does not match what was created in      |
|               |                       | the AWC.                                            |
+---------------+-----------------------+-----------------------------------------------------+
| 324           | ``BAD_FRMT``          | The specified format is wrong. Format options       |
|               |                       | are key value pairs, XML, JSON, YAML                |
+---------------+-----------------------+-----------------------------------------------------+
| 331           | ``BAD_PTYP``          | The payment type is wrong. Refer to the             |
|               |                       | `RIS Payment Types <PaymentTypes.html>`__           |
+---------------+-----------------------+-----------------------------------------------------+
| 332           | ``BAD_CARD``          | The credit card information is malformed or         |
|               |                       | wrong, test cards do not work in the production     |
|               |                       | environment                                         |
+---------------+-----------------------+-----------------------------------------------------+
| 333           | ``BAD_MICR``          | Malformed or improper Magnetic Ink Character        |
|               |                       | Recognition string.                                 |
+---------------+-----------------------+-----------------------------------------------------+
| 334           | ``BAD_PYPL``          | The PayPal Payer ID is malformed or corrupt.        |
+---------------+-----------------------+-----------------------------------------------------+
| 335           | ``BAD_GOOG``          | Malformed or improper Google Checkout Account ID    |
|               |                       | string.                                             |
+---------------+-----------------------+-----------------------------------------------------+
| 336           | ``BAD_BLML``          | Malformed or improper Bill Me Later account         |
|               |                       | number.                                             |
+---------------+-----------------------+-----------------------------------------------------+
| 337           | ``BAD_PENC``          | The encryption method specified is wrong.           |
|               |                       |                                                     |
+---------------+-----------------------+-----------------------------------------------------+
| 338           | ``BAD_GDMP``          | The GreenDot payment token is not a valid           |
|               |                       | payment token                                       |
+---------------+-----------------------+-----------------------------------------------------+
| 339           | ``BAD_HASH``          | When payment type equals ``CARD``,                  |
|               |                       | ``PTYP = CARD`` and payment encryption type         |
|               |                       | equals ``KHASH``, ```PENC = KHASH`` the value       |
|               |                       | must be 20 characters in length.                    |
+---------------+-----------------------+-----------------------------------------------------+
| 340           | ``BAD_MASK``          | Invalid or excessive characters in the ``PTOK``     |
|               |                       | field                                               |
+---------------+-----------------------+-----------------------------------------------------+
| 341           | ``BAD_IPAD``          | The IP address does not match specifications        |
+---------------+-----------------------+-----------------------------------------------------+
| 342           | ``BAD_GIFT``          | The Gift Card payment token is invalid due to       |
|               |                       | invalid characters, null, or exceeding character    |
|               |                       | length                                              |
+---------------+-----------------------+-----------------------------------------------------+
| 351           | ``BAD_MACK``          | The merchant acknowledgement must be ``Y`` or       |
|               |                       | ``N``                                               |
+---------------+-----------------------+-----------------------------------------------------+
| 362           | ``BAD_CART``          | There is a discrepancy in the shopping cart key     |
|               |                       | count and the number of items actually being        |
|               |                       | sent in the cart                                    |
+---------------+-----------------------+-----------------------------------------------------+
| 371           | ``BAD_PROD_TYPE``     | The shopping cart data array attribute is           |
|               |                       | missing.                                            |
+---------------+-----------------------+-----------------------------------------------------+
| 372           | ``BAD_PROD_ITEM``     | The shopping cart data array attribute is           |
|               |                       | corrupt or missing.                                 |
+---------------+-----------------------+-----------------------------------------------------+
| 373           | ``BAD_PROD_DESC``     | The shopping cart data array attribute is           |
|               |                       | corrupt or missing.                                 |
+---------------+-----------------------+-----------------------------------------------------+
| 374           | ``BAD_PROD_QUANT``    | The shopping cart data array attribute is           |
|               |                       | corrupt or missing.                                 |
+---------------+-----------------------+-----------------------------------------------------+
| 375           | ``BAD_PROD_PRICE``    | The shopping cart data array attribute is           |
|               |                       | corrupt or missing.                                 |
+---------------+-----------------------+-----------------------------------------------------+
| 399           | ``BAD_OPTN``          | A UDF has been mistyped or does not exist in the    |
|               |                       | Agent Web Console                                   |
+---------------+-----------------------+-----------------------------------------------------+
| 401           | ``EXTRA_DATA``        | RIS keys submitted by merchant were not part of     |
|               |                       | SDK                                                 |
+---------------+-----------------------+-----------------------------------------------------+
| 404           | ``UNNECESSARY_PTOK``  | When ``PTYP`` equals ``NONE`` and a ``PTOK`` is     |
|               |                       | submitted                                           |
+---------------+-----------------------+-----------------------------------------------------+
| 413           | ``REQUEST_ENTITY_TOO_ | The RIS Post to Kount exceeded the 4K limit.        |
|               | LARGE``               |                                                     |
+---------------+-----------------------+-----------------------------------------------------+
| 501           | ``UNAUTH_REQ``        | Error regarding certificate - Using test            |
|               |                       | certificate in prod                                 |
+---------------+-----------------------+-----------------------------------------------------+
| 502           | ``UNAUTH_MERC``       | Invalid Merchant ID has been entered                |
+---------------+-----------------------+-----------------------------------------------------+
| 601           | ``SYS_ERR``           | Unspecified system error - Contact Merchant         |
|               |                       | Services                                            |
+---------------+-----------------------+-----------------------------------------------------+
| 602           | ``SYS_NOPROCESS``     | Kount will not process particular transaction       |
+---------------+-----------------------+-----------------------------------------------------+
| 701           | ``NO_HDR``            | No header found with ``merchantId = [XXXXX]``,      |
|               |                       | ``session_id = [htot2kk5khpamo45f777q455]``,        |
|               |                       | ``trans=[122347]`` This error occurs when a RIS     |
|               |                       | request goes to the database and there is no        |
|               |                       | data available in the reply. The Update post had    |
|               |                       | an invalid transaction ID#. Check all required      |
|               |                       | fields for update post and confirm they are         |
|               |                       | being passed correctly.                             |
+---------------+-----------------------+-----------------------------------------------------+

-  **Missing**: When this designation appears, the customer has failed
   to complete a required field.
-  **Bad**: When this designation appears, some data was sent but failed
   to meet specifications. This could also be explained as malformed
   data or bad code that did not meet specifications, such as
   ``AVS = W`` instead of ``AVS = M``.
