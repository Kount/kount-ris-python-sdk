Making requests to the Kount RIS
=======================================

Configuration prerequisites and requirements
============================================

Before you make your RIS call, you need to have received (or created)
the following data from Kount: 

* Merchant ID, 6-digit integer, referenced as ``MERCHANT_ID`` in code snippets 

* Site ID, *url*

* URL for (test) RIS calls - ``url_api``, currently ``url_api = "https://risk.beta.kount.net"`` in `test\_api\_kount.py <https://github.com/Kount/kount-ris-python-sdk/blob/master/tests/test_api_kount.py>`__

* Hashing configurationKey used to encrypt sensitive data, configurationKey - must be configured in ``kount.settings``:

    * as environment variable | K_KEY or 
    * any convenient file /like local\_settings.py for Django users/

* API key, a JWT key used for authentication, *key* parameter in class Client `client.py <https://github.com/Kount/kount-ris-python-sdk/blob/master/kount/client.py>`__, used to perform communication with the RIS server.



Currently: **configurationKey = b'fake configurationKey'** in `settings.py <https://github.com/Kount/kount-ris-python-sdk/blob/master/kount/settings.py>`__

Creating request objects
========================

There are two types of requests that can be performed through the SDK -
``Inquiry`` and ``Update``. Those have various modes which will be
discussed later on.

The usual structure of a ``Request`` usually consists of three parts: 

* Information about **the merchant and processing instructions** for the RIS service 

* Information about **the customer making a purchase**: personal data, geo-location, etc. 

* Information about **the purchase**: product name, category, quantity, price

Let's create a sample ``Inquiry`` object and then send it to the RIS
service. /**see test\_inquiry.py**/

::

    #python
    from kount.util.khash import Khash
    from kount.settings import configurationKey as iv

    Khash.set_iv(iv)

    MERCHANT_ID = 999667
    EMAIL_CLIENT = "customer.name@email.com"
    SHIPPING_ADDRESS = Address("567 West S2A1 Court North", "",
                               "Gnome", "AK", "99762", "US")
    PTOK = "0007380568572514"
    SITE_ID = "192.168.32.16"
    URL_API = "https://kount.ris/url"
    API_KEY = "real api key"

    def evaluate_inquiry():
        session_id = generate_unique_id()[:32]
        inquiry = Inquiry()

        # set merchant information, see default_inquiry() in test_basic_connectivity.py
        inquiry.merchant_set(MERCHANT_ID)
        inquiry.request_mode(INQUIRYMODE.DEFAULT)
        inquiry.merchant_acknowledgment_set(MERCHANTACKNOWLEDGMENT.TRUE)
        inquiry.website("DEFAULT")
        
        #~ set customer information
        inquiry.unique_customer_id(session_id[:20])
        inquiry.ip_address(SITE_ID)
        payment = CardPayment(PTOK, khashed=False)   # credit-card-number
        #~ or for khashed token:
        #~ payment = CardPayment(PTOK)   # credit-card-number, khashed=True *default value*
        inquiry.payment_set(payment) 
        inquiry.customer_name("SdkTestFirstName SdkTestLastName")
        inquiry.email_client(EMAIL_CLIENT)
        inquiry.shipping_address(SHIPPING_ADDRESS)

        # set purchase information
        inquiry.currency_set(CURRENCYTYPE.USD)
        inquiry.total_set('123456')
        cart_item = []
        cart_item.append(CartItem("SPORTING_GOODS", "SG999999",
                                  "3000 CANDLEPOWER PLASMA FLASHLIGHT",
                                  '2', '68990'))
        inquiry.shopping_cart(cart_item)

        client = Client(URL_API, API_KEY)
        response = client.process(params=self.inq.params)
        response_params = Response(response).params
        
        # do stuff with response

Explanation of the request
==========================

Here is a short description of what's going on during request creation,
following the numbered comments in code

#. Creating the communication client, requires the RIS service url and provided API key. The API key is set as request header for the network request.

#. Setting the request mode. As mentioned previously, there are several request modes and **INQUIRYMODE.INITIAL_INQUIRY** is the most  used one. Please check the :ref:`Advanced` page for more information on request modes.


#. Setting a session identifier. This ID should be unique for a 30-day span and is used to track all changes regarding the purchase   described in the request. More information on the :ref:`Advanced` page.

#. IP address of the customer. The merchant can discover it or it can be obtained through the :ref:`Data Collector` service.

#. Set this to a correct credit number or select another payment  method (for test purposes).

#. The total purchase amount represented in the lowest possible currency denomination (*example: cents for US Dollars*)

#. Different payment types /user defined/ can be created with **NewPayment** or **Payment**:

::

    NewPayment(payment_type="PM42", payment_token=token, khashed=True) 
    Payment("PM42", token, False)
    Payment("PM42", token, True)

Good examples - `test_bed_examples.py <https://github.com/Kount/kount-ris-python-sdk/blob/master/tests/test_bed_examples.py>`__
