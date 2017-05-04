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
from util.ris_validation_exception import RisException
from util.currency_type import CurrencyType


class TestCurrencyType(unittest.TestCase):
    def test_currency_type_valid(self ):
        for type in ["USD", "EUR", "CAD", "AUD", "JPY", "HKD", "NZD", " HKD", " NZD ", " nzD "]:
            ct = CurrencyType(type)
            self.assertTrue(isinstance(ct, CurrencyType))

    def test_currency_type_incorrect_string(self):
        for bad_type in ["42", "<script>alert(42)</script>", None, "", 42]:
            expected = "Expected currency type in "
            with self.assertRaisesRegex(RisException, expected) as ct:
                CurrencyType(bad_type)


if __name__ == "__main__":
     unittest.main()
