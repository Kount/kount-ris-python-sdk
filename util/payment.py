#!/usr/bin/env python
"class Payment - RIS payment type object"
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
    khashed - Indicates whether payment token is khashed.
    True if payment token is khashed.
    """
    def __init__(self, payment_token=None, payment_type=None, khashed=False):
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
            self.khashed = True
        else:
            self.khashed = False


class GiftCardPayment(Payment):
    """A class representing a gift card payment.
    Sets the PTYP parameter to "GIFT".
    Args: gift_card_number - The gift card number
    """
    def __init__(self, gift_card_number):
        super(GiftCardPayment, self).__init__(
            payment_type="GIFT", payment_token=str(gift_card_number))


class GooglePayment(Payment):
    """A class representing a google payment.
        Sets the PTYP parameter to "GIFT".
        Args: google_payment_id - Google payment ID
        """
    def __init__(self, google_payment_id):
        super(GooglePayment, self).__init__(payment_type="GOOG",
                                            payment_token=google_payment_id)


class GreenDotMoneyPakPayment(Payment):
    """Green Dot MoneyPak
    Sets the PTYP parameter to "GDMP".
    param green_dot_mp_payment_id - Green Dot MoneyPak payment ID number
    """
    def __init__(self, green_dot_mp_payment_id):
        super(GreenDotMoneyPakPayment, self).__init__(
            payment_type="GDMP",
            payment_token=str(green_dot_mp_payment_id))


class NoPayment(Payment):
    """No payment type. A class representing no payment.
    Sets the PTYP parameter to "NONE".
    """
    def __init__(self):
        super(NoPayment, self).__init__(payment_type=None, payment_token=None)


class CheckPayment(Payment):
    """Constructor for a check payment
    Sets the PTYP parameter to "CHEK".
    arg: micr - The MICR (Magnetic Ink Character Recognition) line on the check.
    """
    def __init__(self, micr):
        super(CheckPayment, self).__init__(payment_type="CHEK",
                                           payment_token=str(micr))


class PaypalPayment(Payment):
    """Constructor for a paypal payment that accepts the paypal payment ID.
    Sets the PTYP parameter to "PYPL".
    param paypal_payment_id - Paypal payment ID
    """
    def __init__(self, paypal_payment_id):
        super(PaypalPayment, self).__init__(
            payment_type="PYPL", payment_token=paypal_payment_id)


class CardPayment(Payment):
    """Constructor for a credit card payment.
    Sets the PTYP parameter to "CARD".
    param card_number - The card number
    """
    def __init__(self, card_number):
        super(CardPayment, self).__init__(
            payment_type="CARD", payment_token=card_number)


class BillMeLaterPayment(Payment):
    """A class representing a bill me later payment.
    Sets the PTYP parameter to "BLML".
    param payment_id - The payment ID
    """
    def __init__(self, payment_id):
        super(BillMeLaterPayment, self).__init__(
            payment_type="BLML", payment_token=str(payment_id))
