#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"class Khash"

from __future__ import absolute_import, unicode_literals, division, print_function
import hashlib
import re
import logging
from string import digits, ascii_uppercase
from kount.settings import SALT
from resources.correct_salt_cryp import correct_salt_cryp

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"

logger = logging.getLogger('kount.khash')

def validator(*args):
    """check is list with arguments is valid -
    positive integer or length of the string
    Args: list with integers or strings
    returns: list with args as strings
    """
    for current in args:
        try:
            str(current)
            is_string = True
        except ValueError:
            is_string = False
        curr_len = len(str(current))
        invalid = curr_len not in range(6, 100) or current is None
        try:
            current = int(current)
            is_digit = True
        except (TypeError, ValueError):
            is_digit = False
        if is_digit and int(current) <= 0:
            raise ValueError("incorrect arg: [%s]" % current)
        elif invalid or not is_string:
            raise ValueError("incorrect arg: [%s]" % current)
    return [str(current) for current in args]


class Khash(object):
    """
    Uninstantiable class constructor.
    Class for creating Kount RIS KHASH encoding payment tokens.
    """
    iv = SALT

    @classmethod
    def verify(cls):
        current_crypted = hashlib.sha256(cls.salt.encode('utf-8')).hexdigest()
        if current_crypted != correct_salt_cryp:
            mesg = "Configured SALT phrase is incorrect."
            logger.error(mesg)
            raise ValueError(mesg)
        logger.info("Configured SALT phrase is correct.")
        return True

    @classmethod
    def set_iv(cls, iv):
        """
        initialize the SALT phrase used in hashing operations.
        Khash.set_salt(salt)"""
        cls.salt = iv
        cls.verify()

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
        return "%s%s" % (token_valid[:6], cls.hash(cls, plain_text=token_valid))

    @classmethod
    def hash_gift_card(cls, merchant_id, card_number):
        """ Hash a gift card payment token using the Kount hashing algorithm.
            Args:   merchant_id - Merchant ID number
                    card_number - Card number to be hashed
            returns: String hashed
        """
        merchant_id, card_number = validator(merchant_id, card_number)
        return "%s%s" % (merchant_id, cls.hash(cls, plain_text=card_number))

    @staticmethod
    def hash(cls, plain_text):
        """
        Compute a Kount hash of a given plain text string.
        Preserves the first six characters of the input
        so that hasked tokens can be categorized
        by Bank Idenfication Number (BIN).
        Args: plain_text - String to be hashed
        returns: String hashed
        """
        if isinstance(plain_text, (int)):
            plain_text = str(plain_text)
        if validator(plain_text):
            legal_chars = digits + ascii_uppercase
            loop_max = 28
            hex_chunk = 7
            length = len(legal_chars)
            hashed = []
            plain_text_bytes = plain_text.encode('utf-8') #Python 3.x
            sha1 = hashlib.sha1(plain_text_bytes + ".".encode('utf-8') +
                                cls.iv.encode('utf-8')).hexdigest()
            for i in range(0, loop_max, 2):
                hashed.append(legal_chars[int(sha1[i: i+hex_chunk], 16)
                                          % length])
            return ''.join(hashed)
        else:
            raise ValueError("incorrect arg: [%s]" % plain_text)

    @staticmethod
    def khashed(val):
        """ Arg: val - String, Token that may or may not be khashed
         return: Boolean, True if token is already khashed
        """
        regex = r"^[0-9a-zA-Z]{6}[0-9A-Z]{14}$"
        return re.match(regex, val)
