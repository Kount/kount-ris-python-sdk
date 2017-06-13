#!/usr/bin/env python
"class Payment - RIS payment type object"
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
from __future__ import absolute_import, unicode_literals, division, print_function
import re
from kount.util.khash import Khash

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
    khashed - Indicates whether payment token is khashed.
    True if payment token is khashed.
    """
    def __init__(self, payment_type=None, payment_token=None):
        """Constructor for a payment that accepts the payment ID.
        Calculate and set the payment token LAST4 value.
        last4 - Last 4 characters of payment token"""
        self.last4 = "NONE"
        self.payment_token = None
        if payment_type is not None:
            self.payment_type = str(payment_type)
        else:
            self.payment_type = "NONE"
            self.khashed = False
        if payment_token is not None:
            self.payment_token = str(payment_token)
            if len(str(payment_token)) >= 4:
                self.last4 = self.payment_token[-4:]

    def khashed(self):
        """Token that may or may not be khashed
         return: Boolean, True if token is already khashed
        """
        regex = r"^[0-9a-zA-Z]{6}[0-9A-Z]{14}$"
        return re.match(regex, str(self.payment_token))

    def khash_token(self):
        self.payment_token = Khash().hash_payment_token(
            token=self.payment_token)
        return self.khashed()


def GiftCardPayment(gift_card_number):
    """Sets the PTYP parameter to GIFT"""
    return Payment(payment_type="GIFT", payment_token=str(gift_card_number))


def GooglePayment(google_payment_id):
    """Sets the PTYP parameter to "GIFT".
        Args: google_payment_id - Google payment ID"""
    return Payment(payment_type="GOOG", payment_token=str(google_payment_id))


def GreenDotMoneyPakPayment(green_dot_mp_payment):
    """Sets the PTYP parameter to "GDMP".
    param green_dot_mp_payment - Green Dot MoneyPak payment ID number"""
    return Payment(payment_type="GDMP", payment_token=str(green_dot_mp_payment))


def NoPayment():
    """No payment type. Sets the PTYP parameter to "NONE"."""
    return Payment(payment_type=None, payment_token=None)


def CheckPayment(micr):
    """Sets the PTYP parameter to "CHEK".
    arg: micr - The MICR (Magnetic Ink Character Recognition) line on the check.
    """
    return Payment(payment_type="CHEK", payment_token=str(micr))


def PaypalPayment(paypal_payment_id):
    """paypal payment - accepts the paypal payment ID.
    Sets the PTYP parameter to "PYPL".
    param paypal_payment_id - Paypal payment ID
    """
    return Payment(payment_type="PYPL", payment_token=paypal_payment_id)


def CardPayment(card_number):
    """credit card payment.
    Sets the PTYP parameter to "CARD".
    param card_number - The card number
    """
    return Payment(payment_type="CARD", payment_token=card_number)


def BillMeLaterPayment(payment_id):
    """bill me later payment.
    Sets the PTYP parameter to "BLML".
    param payment_id - The payment ID
    """
    return Payment(payment_type="BLML", payment_token=str(payment_id))

def NewPayment(payment_type, payment_token):
    """New payment type.
    Sets the PTYP parameter to desired parameter.
    """
    return Payment(payment_type, payment_token)
