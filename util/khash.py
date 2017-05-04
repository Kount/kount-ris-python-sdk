#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.

import hashlib
import re
from string import digits, ascii_uppercase
from ..local_settings import salt

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


def validator(*args):
	"""check is list with arguments is valid - positive integer or length of the string
	Args: list with integers or strings
	returns: list with args as strings
	"""
	for current in args:
		is_string = isinstance(current, str)
		is_digit = isinstance(current, (int, long))
		if ((is_digit and current <= 0) or (not is_digit and not is_string) or
				current is None or len(str(current))<6):
			raise ValueError("incorrect arg: [%s]"%current)
	return [str(current) for current in args]


class Khash(object):
	"""
	Uninstantiable class constructor.
	Class for creating Kount RIS KHASH encoding payment tokens.
	"""

	@classmethod
	def hash_payment_token(cls, token):
		"""Create a Kount hash of a provided payment token. Payment tokens
		that can be hashed via this method include: credit card numbers,
		Paypal payment IDs, Check numbers, Google Checkout IDs, Bill Me
		Later IDs, and Green Dot MoneyPak IDs.
		
		Args: token - String to be hashed
		returns: String hashed
		if len(token) < 6 - need to clarify the expected behaviour
		"""
		token_valid = validator(token)[0]
		return "%s%s"%(token_valid[:6], cls.hash(token_valid))

	@classmethod
	def hash_gift_card(cls, merchant_id, card_number):
		""" Hash a gift card payment token using the Kount hashing algorithm.
		Args: 	merchant_id - Merchant ID number
				card_number - Card number to be hashed
		returns: String hashed
		"""
		merchant_id, card_number = validator(merchant_id, card_number)
		return "%s%s"%(merchant_id, cls.hash(card_number))

	@staticmethod
	def hash(plain_text):
		"""
		Compute a Kount hash of a given plain text string.
		Preserves the first six characters of the input 
		so that hasked tokens can be categorized
		by Bank Idenfication Number (BIN).
		Args: plain_text - String to be hashed
		returns: String hashed
		"""
		if isinstance(plain_text, (int, long)):
			plain_text = str(plain_text)
		if validator(plain_text):
			legal_chars = digits + ascii_uppercase
			loop_max = 28
			hex_chunk = 7
			length = len(legal_chars)
			hashed = []
			plain_text_bytes = plain_text.encode('utf-8') #Python 3.x
			salt_bytes = salt.encode('utf-8')
			sha1 = hashlib.sha1(plain_text_bytes + ".".encode('utf-8') + salt_bytes).hexdigest()
			for i in range(0, loop_max, 2):
				hashed.append(legal_chars[int(sha1[i: i+hex_chunk], 16) % length])
			return ''.join(hashed)
		else:
			raise ValueError("incorrect arg: [%s]"%plain_text)

	@staticmethod
	def khashed(val):
		""" Arg: val - String, Token that may or may not be khashed
		 return: Boolean, True if token is already khashed
		"""
		regex = r"^[0-9]{6}[0-9A-Z]{14}$"
		#regex = r"^[0-9a-zA-Z]{6}[0-9A-Z]{14}$"
		return re.match(regex, val)
