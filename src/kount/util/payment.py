#!/usr/bin/env python
"class Payment - RIS payment type object"
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.

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
            self._payment_type = str(payment_type)
        else:
            self._payment_type = "NONE"

        if payment_token is not None:
            self.payment_token = str(payment_token)
            if len(self.payment_token) >= 4:
                self.last4 = self.payment_token[-4:]
            if khashed:
                self.khashed = self.khash_token()
        self.khashed = khashed and Khash.khashed(self.payment_token)

    @property
    def payment_type(self):
        return self._payment_type

    def khash_token(self):
        "hash the payment_token, return True if khashed, else raise ValueError"
        k = Khash.get()
        self.payment_token = k.hash_payment_token(
            token=self.payment_token)
        if k.khashed(self.payment_token):
            return True
        raise ValueError("payment_token [%s] is not khashed" %
                         self.payment_token)


class GiftCardPayment(Payment):
    """Sets the PTYP parameter to GIFT,
    params: gift_card_number,
     khashed - boolean"""
    def __init__(self, gift_card_number, khashed=True):
        super(GiftCardPayment, self).__init__(
            payment_type="GIFT",
            payment_token=gift_card_number,
            khashed=khashed)


class GooglePayment(Payment):
    """Sets the PTYP parameter to "GIFT".
    params: google_payment_id - Google payment ID
                khashed - boolean"""
    def __init__(self, google_payment_id, khashed=True):
        super(GooglePayment, self).__init__(
            payment_type="GOOG",
            payment_token=google_payment_id,
            khashed=khashed)


class GreenDotMoneyPakPayment(Payment):
    """Sets the PTYP parameter to "GDMP".
    params: green_dot_mp_payment - Green Dot MoneyPak payment ID number
            khashed - boolean"""
    def __init__(self, green_dot_mp_payment, khashed=True):
        super(GreenDotMoneyPakPayment, self).__init__(
            payment_type="GDMP",
            payment_token=green_dot_mp_payment,
            khashed=khashed)


class NoPayment(Payment):
    """No payment type. Sets the PTYP parameter to "NONE", not khashed"""
    def __init__(self, *args, **kwargs):
        super(NoPayment, self).__init__(
            payment_type=None,
            payment_token=None,
            khashed=False)


class CheckPayment(Payment):
    """Sets the PTYP parameter to "CHEK".
    params: micr - The MICR (Magnetic Ink Character Recognition)
                line on the check.
            khashed - boolean
    """
    def __init__(self, micr, khashed=True):
        super(CheckPayment, self).__init__(
            payment_type="CHEK",
            payment_token=micr,
            khashed=khashed)


class PaypalPayment(Payment):
    """paypal payment - accepts the paypal payment ID.
    Sets the PTYP parameter to "PYPL".
    params: paypal_payment_id - Paypal payment ID
            khashed - boolean
    """
    def __init__(self, paypal_payment_id, khashed=True):
        super(PaypalPayment, self).__init__(
            payment_type="PYPL",
            payment_token=paypal_payment_id,
            khashed=khashed)


class CardPayment(Payment):
    """credit card payment
    Sets the PTYP parameter to "CARD".
    params: card_number - The card number
            khashed - boolean
    """

    def __init__(self, card_number, khashed=True):
        super(CardPayment, self).__init__(
            payment_type="CARD",
            payment_token=card_number,
            khashed=khashed)


class BillMeLaterPayment(Payment):
    """bill me later payment
    Sets the PTYP parameter to "BLML".
    params: payment_id - The payment ID,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(BillMeLaterPayment, self).__init__(
            payment_type="BLML",
            payment_token=payment_id,
            khashed=khashed)


class ApplePay(Payment):
    """Apple Pay
    Sets the PTYP parameter to "APAY".
    params: payment_id - apay,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(ApplePay, self).__init__(
            payment_type="APAY",
            payment_token=payment_id,
            khashed=khashed)


class BPayPayment(Payment):
    """BPay Payment
    Sets the PTYP parameter to "BPAY".
    params: payment_id - bpay,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(BPayPayment, self).__init__(
            payment_type="BPAY",
            payment_token=payment_id,
            khashed=khashed)


class CarteBleuePayment(Payment):
    """Carte Bleue Payment
    Sets the PTYP parameter to "CARTE_BLEUE".
    params: payment_id - Carte Bleue id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(CarteBleuePayment, self).__init__(
            payment_type="CARTE_BLEUE",
            payment_token=payment_id,
            khashed=khashed)


class ELVPayment(Payment):
    """ELV Payment
    Sets the PTYP parameter to "ELV".
    params: payment_id - ELV id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(ELVPayment, self).__init__(
            payment_type="ELV",
            payment_token=payment_id,
            khashed=khashed)


class GiroPayPayment(Payment):
    """GIROPAY Payment
    Sets the PTYP parameter to "GIROPAY".
    params: payment_id - id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(GiroPayPayment, self).__init__(
            payment_type="GIROPAY",
            payment_token=payment_id,
            khashed=khashed)


class InteracPayment(Payment):
    """Interac Payment
    Sets the PTYP parameter to "INTERAC".
    params: payment_id - id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(InteracPayment, self).__init__(
            payment_type="INTERAC",
            payment_token=payment_id,
            khashed=khashed)


class MercadoPagoPayment(Payment):
    """Mercado Pago Payment
    Sets the PTYP parameter to "MERCADE_PAGO".
    params: payment_id - id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(MercadoPagoPayment, self).__init__(
            payment_type="MERCADE_PAGO",
            payment_token=payment_id,
            khashed=khashed)


class NetellerPayment(Payment):
    """Neteller Payment
    Sets the PTYP parameter to "NETELLER".
    params: payment_id - id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(NetellerPayment, self).__init__(
            payment_type="NETELLER",
            payment_token=payment_id,
            khashed=khashed)


class PoliPayment(Payment):
    """POLi Payment
    Sets the PTYP parameter to "POLI".
    params: payment_id - id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(PoliPayment, self).__init__(
            payment_type="POLI",
            payment_token=payment_id,
            khashed=khashed)


class SEPAPayment(Payment):
    """Single Euro Payments Area Payment
    Sets the PTYP parameter to "SEPA".
    params: payment_id - id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(SEPAPayment, self).__init__(
            payment_type="SEPA",
            payment_token=payment_id,
            khashed=khashed)


class SofortPayment(Payment):
    """Sofort Payment
    Sets the PTYP parameter to "SOFORT".
    params: payment_id - id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(SofortPayment, self).__init__(
            payment_type="SOFORT",
            payment_token=payment_id,
            khashed=khashed)


class TokenPayment(Payment):
    """Token Payment
    Sets the PTYP parameter to "TOKEN".
    params: payment_id - id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(TokenPayment, self).__init__(
            payment_type="TOKEN",
            payment_token=payment_id,
            khashed=khashed)


class SkrillPayment(Payment):
    """Skrill/Moneybookers Payment
    Sets the PTYP parameter to "SKRILL".
    params: payment_id - id,
            khashed - boolean
    """
    def __init__(self, payment_id, khashed=True):
        super(SkrillPayment, self).__init__(
            payment_type="SKRILL",
            payment_token=str(payment_id),
            khashed=khashed)


def NewPayment(payment_type, payment_token, khashed=True):
    """User-defined payment type
    Sets the PTYP parameter to desired parameter.
    params: payment_type
            payment_token
            khashed - boolean
    """
    return Payment(payment_type, payment_token, khashed=khashed)
