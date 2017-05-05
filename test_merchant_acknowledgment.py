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
from util.merchant_acknowledgment import merchant_acknowledgment


class TestMerchantAcknowledgmentType(unittest.TestCase):
    def test_ma(self):
        self.assertEqual(merchant_acknowledgment("Y"), "YES")
        self.assertEqual(merchant_acknowledgment("y"), "YES")
        self.assertRaises(KeyError, merchant_acknowledgment, "yo" )
        self.assertRaises(KeyError, merchant_acknowledgment, None )
        self.assertRaises(KeyError, merchant_acknowledgment, "" )
        self.assertRaises(KeyError, merchant_acknowledgment, 5)
        self.assertRaises(KeyError, merchant_acknowledgment, {})


if __name__ == "__main__":
    unittest.main()