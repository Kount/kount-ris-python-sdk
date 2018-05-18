#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"Test Payment Type"
import unittest
import pytest

from kount.util.khash import Khash
from kount.util.payment import (
    BillMeLaterPayment, CardPayment, CheckPayment,
    GiftCardPayment, GooglePayment,
    GreenDotMoneyPakPayment, NoPayment,
    Payment, PaypalPayment)

from kount.version import VERSION

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


@pytest.mark.usefixtures("conf_key")
class TestPaymentType(unittest.TestCase):
    """Test Payment Type"""
    def setUp(self):
        self.test = 1234567890*1000000000

    def test_giftcardpayment(self):
        """giftcard payment"""
        ptype = GiftCardPayment(gift_card_number=self.test, khashed=False)
        self.assertTrue(isinstance(ptype, Payment))
        self.assertEqual(ptype.last4, str(self.test)[-4:])
        self.assertFalse(ptype.khashed)
        self.assertEqual(ptype.payment_type, "GIFT")
        self.assertEqual(ptype.payment_token, str(self.test))

    def test_payments(self):
        "all predefined payments"
        plist = (Payment, BillMeLaterPayment, CardPayment,
                 CheckPayment, GiftCardPayment, GooglePayment,
                 GreenDotMoneyPakPayment, NoPayment, Payment, PaypalPayment)
        payment_dict = {
            "BLML": BillMeLaterPayment(self.test, khashed=False),
            "CARD": CardPayment(self.test, khashed=False),
            "CHEK": CheckPayment(self.test, khashed=False),
            "GIFT": GiftCardPayment(self.test, khashed=False),
            "GOOG": GooglePayment(self.test, khashed=False),
            "GDMP": GreenDotMoneyPakPayment(self.test, khashed=False),
            "NONE": NoPayment(),
            "PYPL": PaypalPayment(self.test, khashed=False),
            }
        ptypes = []
        for current in payment_dict:
            curp = payment_dict[current]
            if current == "NONE":
                self.assertEqual(curp.last4, "NONE")
                self.assertIsNone(curp.payment_token)
            else:
                self.assertEqual(curp.last4, str(self.test)[-4:])
                self.assertEqual(curp.payment_token, str(self.test))
            self.assertEqual(curp._payment_type, current)
            ptypes.append(payment_dict[current])
            self.assertIsInstance(payment_dict[current], plist)
            if curp.payment_token is not None:
                self.assertEqual(curp.payment_token, str(self.test))

    def test_user_defined_payment(self):
        "user defined payments"""
        curp = Payment("PM42", self.test, False)
        self.assertEqual(curp.last4, str(self.test)[-4:])
        self.assertEqual(curp.payment_token, str(self.test))
        self.assertFalse(curp.khashed)
        self.assertEqual(curp._payment_type, "PM42")
        self.assertEqual(curp.payment_token, str(self.test))
        self.assertIsInstance(curp, Payment)

    def test_user_defined_payment_khashed(self):
        "user defined payments with Payment - khashed token"
        curp = Payment("PM42", self.test, True)
        self.assertEqual(curp.last4, str(self.test)[-4:])
        self.assertEqual(curp.payment_token,
                         Khash.get().hash_payment_token(self.test))
        self.assertTrue(curp.khashed)
        self.assertEqual(curp._payment_type, "PM42")
        self.assertIsInstance(curp, Payment)

    def test_user_defined_newpayment(self):
        "user defined payments - token khashed and notkhashed "
        curp = Payment("PM42", self.test, khashed=False)
        self.assertEqual(curp.last4, str(self.test)[-4:])
        self.assertEqual(curp.payment_token, str((self.test)))
        self.assertFalse(curp.khashed)
        self.assertEqual(curp.payment_type, "PM42")
        self.assertIsInstance(curp, Payment)
        curp = Payment("PM42", self.test, True)
        self.assertEqual(curp.last4, str(self.test)[-4:])
        self.assertEqual(curp.payment_token,
                         Khash.get().hash_payment_token(self.test))
        self.assertTrue(curp.khashed)


if __name__ == "__main__":
    unittest.main(
        #~ defaultTest="TestPaymentType.test_payments"
        )
