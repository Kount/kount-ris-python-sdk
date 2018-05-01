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
	import uuid
	import logging
	from kount.util.khash import Khash
	from kount.util.address import Address
	from kount.inquiry import Inquiry
	from kount.request import (ASTAT, BCRSTAT, INQUIRYMODE,
									   CURRENCYTYPE, MERCHANTACKNOWLEDGMENT)
	from kount.util.payment import CardPayment, Payment, GiftCardPayment
	from kount.util.cartitem import CartItem
	from kount.client import Client
	from kount.response import Response
	from kount.settings import configurationKey as iv

	Khash.set_iv(iv)

	#CUSTOMER SETTINGS
	MERCHANT_ID = 999999 
	EMAIL_CLIENT = "leon.test@email.com"
	SHIPPING_ADDRESS = Address("567 West S2A1 Court North", "","Gnome", "AK", "99762", "US")
	PTOK = "0007380568572514"
	CUSTOMER_IP= "192.168.32.16"
	#END CUSTOMER

	#ENVIRONMENT SETTINGS 
	API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5OTk5OTkiLCJhdWQiOiJLb3VudC4xIiwiaWF0IjoxNTI0NjkzNTE2LCJzY3AiOnsia2EiOnRydWUsImtjIjp0cnVlLCJhcGkiOmZhbHNlLCJyaXMiOnRydWV9fQ.WFcgpCkG9M1-7nemy2FbCsoXQmy4haezQUtYf70ySAk"
	URL_API = "https://risk.intg2.kount.net"
	VERSION = "0695"
	#END ENVIRONMENT


	def evaluate_inquiry():
		session_id = generate_unique_id()[:32]
		setup_logging()
		inquiry = Inquiry()
		inquiry.version_set(VERSION)

		# set merchant information, see default_inquiry() in test_basic_connectivity.py
		inquiry.merchant_set(MERCHANT_ID)
		inquiry.request_mode(INQUIRYMODE.DEFAULT)
		inquiry.merchant_acknowledgment_set(MERCHANTACKNOWLEDGMENT.TRUE)
		inquiry.website("DEFAULT")
		inquiry.session_set(session_id)

		#~ set customer information
		inquiry.unique_customer_id(session_id[:20])
		inquiry.ip_address(CUSTOMER_IP)
		#payment = CardPayment(PTOK, khashed=False)   # credit-card-number
		#~ or for khashed token:
		payment = CardPayment(PTOK)   # credit-card-number, khashed=True *default value*
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
		response = client.process(params=inquiry.params)
		response_params = Response(response).params
		print(response_params)
		# do stuff with response


	def generate_unique_id():
		return str(uuid.uuid4()).replace('-', '').upper()

	def setup_logging():

		req = logging.getLogger('kount.request')
		req.setLevel(logging.DEBUG)
		reqh = logging.FileHandler('request.log')
		reqh.setLevel(logging.DEBUG)
		req.addHandler(reqh)

		cli = logging.getLogger('kount.client')
		cli.setLevel(logging.DEBUG)
		clih = logging.FileHandler('client.log')
		clih.setLevel(logging.DEBUG)
		cli.addHandler(clih)

		resp = logging.getLogger('kount.response')
		resp.setLevel(logging.DEBUG)
		resph = logging.FileHandler('response.log')
		resph.setLevel(logging.DEBUG)
		resp.addHandler(resph)

	#Make call out to RIS 
	evaluate_inquiry()


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
