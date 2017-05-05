
from util.merchant_acknowledgment import merchant_acknowledgment
from util.payment import (BillMeLaterPayment, CardPayment, CheckPayment, GiftCardPayment, GooglePayment,
	GreenDotMoneyPakPayment, NoPayment, Payment, PaypalPayment)
from util.khash import Khash
from util.authorization_status import authorization_status
from util.bankcard_reply import bankcard_reply


class Request(object):
	"""RIS Request superclass for Inquiry and Update."""
	
	def __init__(self):
		"Map containing data that will be sent to RIS."
		self.params = {}
		self.params['VERS'] = '1.0.0'
		self.khash_payment_encoding(True)
		self.params["SDK"] = "Python 3.6"

	def khash_payment_encoding(self, enabled=True):
		"""Set KHASH payment encoding.
		Arg: enabled Boolean
		"""
		if enabled:
			self.params["PENC"] = "KHASH"
		else:
			elf.params["PENC"] = ""

	def params_set(self, key, value):
		"""Set a parm for the request.
		Args:
		   key - The key for the parm
		   value - The value for the parm
		"""
		self.params[key] = value

	def version_set(self, version):
		"""Set the version number.
		Args: version - The SDK version
		"""
		self.params["VERS"] = version

	def session_set(self, session_id):
		"""Set the session id. Must be unique over a 30-day span
		Args: session_id -  Id of the current session
		"""
		self.params["SESS"] = session_id

	def merchant_set(self, merchant_id):
		"""Set the merchant id.
		Args: merchant_id - Merchant ID
		"""
		self.params["MERC"] = merchant_id

	def kount_central_customer_id(self, customer_id):
		"""Set the Kount Central Customer ID.
		Args: customer_id - KC Customer ID
		"""
		self.params["CUSTOMER_ID"] = customer_id

	def order_number(self, order_number):
		"""Set the order number.
		Args: order_number - Merchant unique order number
		"""
		self.params["ORDR"] = order_number

	def merchant_acknowledgment_set(self, ma_type):
		"""Set the merchant acknowledgment.
		Merchants acknowledgement to ship/process the order.
		The MACK field must be set as 'Y' if personal data is to be
		collected to strengthen the score.
		Args: ma_type - merchant acknowledgment type
		"""
		self.params["MACK"] = merchant_acknowledgment(ma_type)

	def authorization_status(self, autho_status):
		"""Set the Authorization Status.
		Authorization Status returned to merchant from processor. Acceptable values for the 
		AUTH field are A for Authorized or D for Decline. In orders where AUTH=A will 
		aggregate towards order velocity of the persona while orders where AUTH=D will 
		decrement the velocity of the persona.
		Args: auth_status - Auth status by issuer
		"""
		self.params["AUTH"] = authorization_status(auth_status)

	def avs_zip_reply(self, avs_zip_reply):
		"""Set the Bankcard AVS zip code reply.
		Address Verification System Zip Code verification response returned to merchant from 
		processor. Acceptable values are M for match, N for no match, or X for unsupported 
		or unavailable.
		Args: avs_zip_reply - Bankcard AVS zip code reply
		"""
		self.params["AVSZ"] = bankcard_reply(avs_zip_reply)

	def avs_address_reply(self, avs_address_reply):
		"""Set the Bankcard AVS street addres reply.
		Address Verification System Street verification response returned to merchant from 
		processor. Acceptable values are M for match, N for no-match, or X for 
		unsupported or unavailable.
		Args: avs_address_reply - Bankcard AVS street address reply
		"""
		self.params["AVST"] = bankcard_reply(avs_address_reply)

	def avs_address_reply(self, cvv_reply):
		"""Set the Bankcard CVV/CVC/CVV2 reply.
		Card Verification Value response returned to merchant from processor. Acceptable 
		values are M for match, N for no-match, or X unsupported or unavailable.
		Args: cvv_reply -  Bankcard CVV/CVC/CVV2 reply
		"""
		self.params["CVVR"] = bankcard_reply(cvv_reply)

	def payment_set(self):
		"""Set a payment.
		Depending on the payment type, various request parameters are set: PTOK, PTYP, LAST4.
		If payment token hashing is not possible, the PENC parameter is set to empty string.
		Args: payment -  Payment
		"""
		if self.params["PENC"] and not (isinstance(self.payment, NoPayment)) and not self.payment.khashed:
			try:
				if isinstance(self.payment, GiftCardPayment):
					merchant_id = int(self.params["MERC"])
					token = Khash.hash_gift_card(merchant_id, self.payment.payment_token);
				else:
					token = Khash.hash_payment_token(self.payment.payment_token)
				self.payment.khashed = true
			except ValueError as nfe:
				"""logger.error("Error converting Merchant ID to integer" + " value. Set a valid Merchant ID.", nfe);"""
				raise nfe
			except Exception as nsae:
				"""logger.error("Unable to create payment token hash. Caught "
						+ "exception java.security.NoSuchAlgorithmException." + " KHASH payment encoding disabled");
				// Default to plain text payment tokens"""
				self.params["PENC"] = ""
		self.params["PTOK"] = self.payment.payment_token
		self.params["PTYP"] = self.payment.payment_type
		self.params["LAST4"] = self.payment.last4

	def payment_masked(self):
		"""Sets a card payment and masks the card number in the following way:
		First 6 characters remain as they are, following characters up to the last 4 are 
		replaced with the 'X' character, last 4 characters remain as they are.
		If the provided Payment parameter is not a card payment, standard encoding 
		will be applied.
		This method sets the following RIS Request fields: PTOK, PTYP, LAST4, PENC.
		Args: payment - card payment
		"""
		self.params["CVVR"] = cvv_reply
		if isinstance(self.payment, CardPayment) and not self.payment.khashed:
			token = mask_token(token)
			self.params["PTOK"] = self.payment.payment_token
			self.params["PTYP"] = self.payment.payment_type
			self.params["LAST4"] = self.payment.last4
			self.params["PENC"] = "MASK"
		else:
			"""logger.warn("setPaymentMasked: provided payment is not a CardPayment, applying khash instead of masking");"""
			return set_payment(self.payment)

	def mask_token(self, token):
		"""Encodes the provided payment token according to the MASK encoding scheme
		   Args: token -  the Payment token for this request
		   return - MASK-encoded token
		"""
		encoded = token[0:6]
		for i in range(6, len(token) - 4, 1):
			encoded.append('X')		
		encoded.append(token[-4:])
		return encoded

	def set_payment(self, ptyp, ptok):
		"""Set a payment by payment type and payment token.
			The payment type parameter provided is checked if it's one of the predefined payment types
			and Payment is created appropriately
			Args: ptyp - See SDK documentation for a list of accepted payment types
				  ptok - The payment token
		"""
		payment_dict = {
			"BLML": BillMeLaterPayment(ptok),
			"CARD": CardPayment(ptok),
			"CHEK": CheckPayment(ptok),
			"GIFT": GiftCardPayment(ptok),
			"GOOG": GooglePayment(ptok),
			"GDMP": GreenDotMoneyPakPayment(ptok),
			"NONE": NoPayment(ptok),
			"PYPL": PaypalPayment(ptok)
			}
		if ptyp in payment_dict:
			self.payment = payment_dict[ptyp]
		else:
			self.payment = Payment(ptyp, ptok)

	def payment_set(self):
		"""Set a payment.
		Depending on the payment type, various request parameters are set: PTOK, PTYP, LAST4.
		If payment token hashing is not possible, the PENC parameter is set to empty string.
		Args: payment -  Payment
		"""
		if self.params["PENC"] and not (isinstance(self.payment, NoPayment)) and not self.payment.khashed:
			try:
				if isinstance(self.payment, GiftCardPayment):
					merchant_id = int(self.params["MERC"])
					token = Khash.hash_gift_card(merchant_id, self.payment.payment_token);
				else:
					token = Khash.hash_payment_token(self.payment.payment_token)
				self.payment.khashed = true
			except ValueError as nfe:
				"""logger.error("Error converting Merchant ID to integer" + " value. Set a valid Merchant ID.", nfe);"""
				raise nfe
			except Exception as nsae:
				"""logger.error("Unable to create payment token hash. Caught "
						+ nsae + " KHASH payment encoding disabled");
				Default to plain text payment tokens"""
				self.params["PENC"] = ""
		self.params["PTOK"] = payment.payment_token
		self.params["PTYP"] = payment.payment_type
		self.params["LAST4"] = payment.last4

	def expiration_date(self, month, year):
		"""Set Card Expiration Date.
		Args: month - String Month in two digit format: MM.
		      year - String Year in four digit format: YYYY.
		"""
		self.params["CCMM"] = month
		self.params["CCYY"] = year

	def is_set_khash_payment_encoding(self):
		"""Check if KHASH payment encoding has been set.
		   return boolean TRUE when set.
		"""
		encoded =  "PENC" in self.params and self.params["PENC"] == "KHASH"
		return encoded

	def set_close_on_finish(self, close_on_finish):
		"""Set a flag for the request transport.
		Arg: close_on_finish - Sets the close_on_finish flag
		   return boolean TRUE when set.
		"""
		self.close_on_finish =  close_on_finish


if __name__ == "__main__":
	r = Request()
	print(Request().params)