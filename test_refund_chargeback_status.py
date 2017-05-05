#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

import unittest
from util.refund_chargeback_status import refund_chargeback_status


class TestRefundChargebackStatus(unittest.TestCase):
    def test_refund_chargeback_status(self):
        self.assertEqual(refund_chargeback_status("R"), "REFUND")
        self.assertEqual(refund_chargeback_status("r"), "REFUND")
        self.assertEqual(refund_chargeback_status("c"), "CHARGEBACK")
        self.assertRaises(KeyError, refund_chargeback_status, "yo" )
        self.assertRaises(KeyError, refund_chargeback_status, None )
        self.assertRaises(KeyError, refund_chargeback_status, "" )
        self.assertRaises(KeyError, refund_chargeback_status, 5)
        self.assertRaises(KeyError, refund_chargeback_status, {})


if __name__ == "__main__":
    unittest.main()