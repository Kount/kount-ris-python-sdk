#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


class Payment(object):
	"""RIS payment type object.
	Args:
		payment_token - Payment token
		payment_type - Payment type.
		last4 - Last 4 characters of payment token, LAST4_LENGTH
		khashed - Indicates whether payment token is khashed. True if payment token is khashed.
	"""
	def __init__(self, payment_token=None, payment_type=None, khashed=False):
		"Constructor for a payment that accepts the payment ID."
		self.payment_type = payment_type
		self.payment_token = payment_token
		if khashed:
			self.khashed = True
		else:
			self.khashed = False
		#Calculate and set the payment token LAST4 value.
		if (self.payment_token is not None and len(self.payment_token) >= 4):
			self.last4 = self.payment_token[-4:]
		else:
			self.last4 = None


class GiftCardPayment(Payment):
	"""A class representing a gift card payment.
		Sets the PTYP parameter to "GIFT".
		Args: gift_card_number - The gift card number
	"""
	def __init__(self, gift_card_number):
		super(payment_type="GIFT", payment_token=gift_card_number)


class GooglePayment(Payment):
	"""A class representing a google payment.
		Sets the PTYP parameter to "GIFT".
		Args: google_payment_id - Google payment ID
	"""
	def __init__(self, google_payment_id):
		super(payment_type="GOOG", payment_token=google_payment_id)


class GreenDotMoneyPakPayment(Payment):
	"""Green Dot MoneyPak payment
	Sets the PTYP parameter to "GDMP".
	param green_dot_mp_payment_id - Green Dot MoneyPak payment ID number
	"""
	 
	def __init__(self, green_dot_mp_payment_id):
		super(payment_type="GDMP", payment_token=green_dot_mp_payment_id)


class NoPayment(Payment):
	"""No payment type. A class representing no payment.
		Sets the PTYP parameter to "NONE".
	"""
	 
	def __init__(self):
		super(payment_type=None, payment_token=None)


class CheckPayment(Payment):
	"""Constructor for a check payment
	Sets the PTYP parameter to "CHEK".
	param micr - The MICR (Magnetic Ink Character Recognition) line on the check.
	"""
	 
	def __init__(self, micr):
		super(payment_type="CHEK", payment_token=micr)


class PaypalPayment(Payment):
	"""Constructor for a paypal payment that accepts the paypal payment ID.
	Sets the PTYP parameter to "PYPL".
	param paypal_payment_id - Paypal payment ID
	"""
	 
	def __init__(self, paypal_payment_id):
		super(payment_type="PYPL", payment_token=paypal_payment_id)


class CardPayment(Payment):
	"""Constructor for a credit card payment.
	Sets the PTYP parameter to "CARD".
	param card_number - The card number
	"""
	 
	def __init__(self, card_number):
		super(CardPayment, self).__init__(payment_type="CARD", payment_token=card_number)


class BillMeLaterPayment(Payment):
	"""A class representing a bill me later payment.
	Sets the PTYP parameter to "BLML".
	param payment_id - The payment ID
	"""
	 
	def __init__(self, payment_id):
		super(BillMeLaterPayment, self).__init__(payment_type="BLML", payment_token=str(payment_id))


print(BillMeLaterPayment(payment_id=1111111111111111111111))