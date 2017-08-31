#!/usr/bin/env python
"class Payment - RIS payment type object"
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
from __future__ import absolute_import, unicode_literals, division, print_function
import re
from kount.util.khash import Khash
from kount.version import VERSION

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class Payment(object):
    """RIS payment type object.
    Args:
    payment_type - Payment type.
    payment_token - Payment token
    khashed - Indicates whether payment token is khashed.
    True if payment token is khashed.
    """
    def __init__(self, payment_type=None, payment_token=None, khashed=True):
        """Constructor for a payment that accepts the payment ID.
        Calculate and set the payment token LAST4 value.
        last4 - Last 4 characters of payment token"""
        self.last4 = "NONE"
        self.payment_token = None
        if payment_type is not None:
            self.payment_type = str(payment_type)
        else:
            self.payment_type = "NONE"
        if payment_token is not None:
            self.payment_token = str(payment_token)
            if len(str(payment_token)) >= 4:
                self.last4 = self.payment_token[-4:]
            if khashed:
                self.khashed = self.khash_token()
        if khashed or Khash.khashed(self.payment_token):
            self.khashed = True
        else:
            self.khashed = False

    def khash_token(self):
        "hash the payment_token, return True if khashed, else raise ValueError"
        k = Khash()
        self.payment_token = k.hash_payment_token(
            token=self.payment_token)
        if k.khashed(self.payment_token):
            return True
        raise ValueError("payment_token [%s] is not khashed" %
                         self.payment_token)


def GiftCardPayment(gift_card_number, khashed=True):
    """Sets the PTYP parameter to GIFT,
    params: gift_card_number,
            khashed - boolean"""
    return Payment(payment_type="GIFT", payment_token=str(gift_card_number),
                   khashed=khashed)


def GooglePayment(google_payment_id, khashed=True):
    """Sets the PTYP parameter to "GIFT".
    params: google_payment_id - Google payment ID
                khashed - boolean"""
    return Payment(payment_type="GOOG", payment_token=str(google_payment_id),
                   khashed=khashed)


def GreenDotMoneyPakPayment(green_dot_mp_payment, khashed=True):
    """Sets the PTYP parameter to "GDMP".
    params: green_dot_mp_payment - Green Dot MoneyPak payment ID number
            khashed - boolean"""
    return Payment(payment_type="GDMP", payment_token=str(green_dot_mp_payment),
                   khashed=khashed)


def NoPayment():
    """No payment type. Sets the PTYP parameter to "NONE", not khashed"""
    return Payment(payment_type=None, payment_token=None)


def CheckPayment(micr, khashed=True):
    """Sets the PTYP parameter to "CHEK".
    params: micr - The MICR (Magnetic Ink Character Recognition) line on the check.
            khashed - boolean
    """
    return Payment(payment_type="CHEK", payment_token=str(micr),
                   khashed=khashed)


def PaypalPayment(paypal_payment_id, khashed=True):
    """paypal payment - accepts the paypal payment ID.
    Sets the PTYP parameter to "PYPL".
    params: paypal_payment_id - Paypal payment ID
            khashed - boolean
    """
    return Payment(payment_type="PYPL", payment_token=paypal_payment_id,
                   khashed=khashed)


def CardPayment(card_number, khashed=True):
    """credit card payment
    Sets the PTYP parameter to "CARD".
    params: card_number - The card number
            khashed - boolean
    """
    return Payment(payment_type="CARD", payment_token=card_number,
                   khashed=khashed)


def BillMeLaterPayment(payment_id, khashed=True):
    """bill me later payment
    Sets the PTYP parameter to "BLML".
    params: payment_id - The payment ID,
            khashed - boolean
    """
    return Payment(payment_type="BLML", payment_token=str(payment_id),
                   khashed=khashed)

def ApplePay(payment_id, khashed=True):
    """Apple Pay
    Sets the PTYP parameter to "APAY".
    params: payment_id - apay,
            khashed - boolean
    """
    return Payment(payment_type="APAY", payment_token=str(payment_id),
                   khashed=khashed)

def BPayPayment(payment_id, khashed=True):
    """BPay Payment
    Sets the PTYP parameter to "BPAY".
    params: payment_id - bpay,
            khashed - boolean
    """
    return Payment(payment_type="BPAY", payment_token=str(payment_id),
                   khashed=khashed)


def CarteBleuePayment(payment_id, khashed=True):
    """Carte Bleue Payment
    Sets the PTYP parameter to "CARTE_BLEUE".
    params: payment_id - Carte Bleue id,
            khashed - boolean
    """
    return Payment(payment_type="CARTE_BLEUE", payment_token=str(payment_id),
                   khashed=khashed)

def ELVPayment(payment_id, khashed=True):
    """ELV Payment
    Sets the PTYP parameter to "ELV".
    params: payment_id - ELV id,
            khashed - boolean
    """
    return Payment(payment_type="ELV", payment_token=str(payment_id),
                   khashed=khashed)

def GiroPayPayment(payment_id, khashed=True):
    """GIROPAY Payment
    Sets the PTYP parameter to "GIROPAY".
    params: payment_id - id,
            khashed - boolean
    """
    return Payment(payment_type="GIROPAY", payment_token=str(payment_id),
                   khashed=khashed)

def InteracPayment(payment_id, khashed=True):
    """Interac Payment
    Sets the PTYP parameter to "INTERAC".
    params: payment_id - id,
            khashed - boolean
    """
    return Payment(payment_type="INTERAC", payment_token=str(payment_id),
                   khashed=khashed)

def MercadoPagoPayment(payment_id, khashed=True):
    """Mercado Pago Payment
    Sets the PTYP parameter to "MERCADE_PAGO".
    params: payment_id - id,
            khashed - boolean
    """
    return Payment(payment_type="MERCADE_PAGO", payment_token=str(payment_id),
                   khashed=khashed)


def NetellerPayment(payment_id, khashed=True):
    """Neteller Payment
    Sets the PTYP parameter to "NETELLER".
    params: payment_id - id,
            khashed - boolean
    """
    return Payment(payment_type="NETELLER", payment_token=str(payment_id),
                   khashed=khashed)


def PoliPayment(payment_id, khashed=True):
    """POLi Payment
    Sets the PTYP parameter to "POLI".
    params: payment_id - id,
            khashed - boolean
    """
    return Payment(payment_type="POLI", payment_token=str(payment_id),
                   khashed=khashed)


def SEPAPayment(payment_id, khashed=True):
    """Single Euro Payments Area Payment
    Sets the PTYP parameter to "SEPA".
    params: payment_id - id,
            khashed - boolean
    """
    return Payment(payment_type="SEPA", payment_token=str(payment_id),
                   khashed=khashed)


def SofortPayment(payment_id, khashed=True):
    """Sofort Payment
    Sets the PTYP parameter to "SOFORT".
    params: payment_id - id,
            khashed - boolean
    """
    return Payment(payment_type="SOFORT", payment_token=str(payment_id),
                   khashed=khashed)

def TokenPayment(payment_id, khashed=True):
    """Token Payment
    Sets the PTYP parameter to "TOKEN".
    params: payment_id - id,
            khashed - boolean
    """
    return Payment(payment_type="TOKEN", payment_token=str(payment_id),
                   khashed=khashed)

def SkrillPayment(payment_id, khashed=True):
    """Skrill/Moneybookers Payment
    Sets the PTYP parameter to "SKRILL".
    params: payment_id - id,
            khashed - boolean
    """
    return Payment(payment_type="SKRILL", payment_token=str(payment_id),
                   khashed=khashed)

def NewPayment(payment_type, payment_token, khashed=True):
    """User-defined payment type
    Sets the PTYP parameter to desired parameter.
    params: payment_type
            payment_token
            khashed - boolean
    """
    return Payment(payment_type, payment_token, khashed=khashed)
