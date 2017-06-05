#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk
# Copyright (C) 2017 Kount Inc. All Rights Reserved.

"Test Payment Type"
import unittest

from kount.util.payment import (BillMeLaterPayment, CardPayment, CheckPayment,
                                GiftCardPayment, GooglePayment,
                                GreenDotMoneyPakPayment, NoPayment,
                                Payment, PaypalPayment)


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


class TestPaymentType(unittest.TestCase):
    "Test Payment Type"
    def setUp(self):
        self.test = 1234567890*1000000000

    def test_giftcardpayment(self):
        "giftcard payment"
        ptype = GiftCardPayment(gift_card_number=self.test)
        self.assertTrue(isinstance(ptype, GiftCardPayment))
        self.assertEqual(ptype.last4, str(self.test)[-4:])
        self.assertFalse(ptype.khashed)
        self.assertEqual(ptype.payment_type, "GIFT")
        self.assertEqual(ptype.payment_token, str(self.test))

    def test_payments(self):
        "all payments"
        plist = (Payment, BillMeLaterPayment, CardPayment,
                 CheckPayment, GiftCardPayment, GooglePayment,
                 GreenDotMoneyPakPayment, NoPayment, Payment, PaypalPayment)
        payment_dict = {
            "BLML": BillMeLaterPayment(self.test),
            "CARD": CardPayment(self.test),
            "CHEK": CheckPayment(self.test),
            "GIFT": GiftCardPayment(self.test),
            "GOOG": GooglePayment(self.test),
            "GDMP": GreenDotMoneyPakPayment(self.test),
            "NONE": NoPayment(),
            "PYPL": PaypalPayment(self.test),
            }
        ptypes = []
        for current in payment_dict:
            curp = payment_dict[current]
            if isinstance(curp, NoPayment):
                self.assertEqual(curp.last4, "NONE")
                self.assertIsNone(curp.payment_token)
            else:
                self.assertEqual(curp.last4, str(self.test)[-4:])
                self.assertEqual(curp.payment_token, str(self.test))
            self.assertFalse(curp.khashed)
            self.assertEqual(curp.payment_type, current)
            ptypes.append(payment_dict[current])
            self.assertIsInstance(payment_dict[current], plist)


if __name__ == "__main__":
    unittest.main()
