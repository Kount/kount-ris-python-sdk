#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"class Khash"

from __future__ import (absolute_import, unicode_literals,
                        division, print_function)

import hashlib
import logging
import re
import string

from kount.resources.correct_key_cryp import correct_key_cryp
from kount.version import VERSION
from .a85 import a85decode
from kount.config import SDKConfig

__author__ = SDKConfig.SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDKConfig.SDK_MAINTAINER
__email__ = SDKConfig.MAINTAINER_EMAIL
__status__ = SDKConfig.STATUS

LOG = logging.getLogger('kount.khash')


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
        invalid = curr_len < 6 or curr_len > 100 or current is None
        try:
            current = int(current)
            is_digit = True
        except (TypeError, ValueError):
            is_digit = False
        if is_digit and int(current) <= 0:
            raise ValueError("incorrect arg: [%s]" % current)
        elif invalid or not is_string:
            raise ValueError("incorrect arg: [%s]" % current)
    return [str(i) for i in args]


class Khash(object):

    re_khashed = re.compile(r"^[0-9a-zA-Z]{6}[0-9A-Z]{14}$")
    __instance = None

    @staticmethod
    def get():
        """ Static access method. """
        SDKConfig.setup(SDKConfig._CONFIGURATION_KEY)
    
        return Khash.__instance

    """
    Class for creating Kount RIS KHASH encoding payment tokens.
    """
    def __init__(self, key):
        """ Virtually private constructor. """
        hash_salt_key = a85decode(key)
        self.config_key = hash_salt_key.decode("utf-8")
        self.verify()
        self.salt_key = hash_salt_key
        Khash.__instance = self

    def verify(self):
        key = self.config_key.encode('utf-8')
        sha_key = hashlib.sha256(key).hexdigest()
        if sha_key != correct_key_cryp:
            mesg = "Configured config_key key is incorrect"
            LOG.error(mesg)
            raise ValueError(mesg)
        
        LOG.info("Configured config_key is correct.")
        return True

    def hash_payment_token(self, token):
        """Create a Kount hash of a provided payment token. Payment tokens
        that can be hashed via this method include: credit card numbers,
        Paypal payment IDs, Check numbers, Google Checkout IDs, Bill Me
        Later IDs, and Green Dot MoneyPak IDs.

        Args: token - String to be hashed
        returns: String hashed
        if len(token) < 6 - need to clarify the expected behaviour
        """
        token_valid = validator(token)[0]
        return "%s%s" % (token_valid[:6], self.hash(plain_text=token_valid))

    def hash_gift_card(self, merchant_id, card_number):
        """ Hash a gift card payment token using the Kount hashing algorithm.
        Args: merchant_id - Merchant ID number
        card_number - Card number to be hashed
        returns: String hashed
        """
        merchant_id, card_number = validator(merchant_id, card_number)
        return "%s%s" % (merchant_id, self.hash(plain_text=card_number))

    def hash(self, plain_text):
        """
        Compute a Kount hash of a given plain text string.
        Preserves the first six characters of the input
        so that hashed tokens can be categorized
        by Bank Identification Number (BIN).
        Args: plain_text - String to be hashed
        returns: String hashed
        """
        if isinstance(plain_text, int):
            plain_text = str(plain_text)
        if validator(plain_text):
            legal_chars = string.digits + string.ascii_uppercase
            loop_max = 28
            hex_chunk = 7
            length = len(legal_chars)
            hashed = []
            plain_text_bytes = plain_text.encode('utf-8')  # Python 3.x
            sha1 = hashlib.sha1(plain_text_bytes + ".".encode('utf-8') +
                                self.salt_key).hexdigest()
            for i in range(0, loop_max, 2):
                hashed.append(legal_chars[int(sha1[i: i + hex_chunk], 16)
                                          % length])
            return ''.join(hashed)
        else:
            raise ValueError("incorrect arg: [%s]" % plain_text)

    @classmethod
    def khashed(cls, val):
        """ Arg: val - String, Token that may or may not be khashed
         return: Boolean, True if token is already khashed
        """
        return cls.re_khashed.match(val)
