#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

import unittest
from util.ris_validation_exception import RisException
from util.shipping_type import ShippingType


class TestShippingType(unittest.TestCase):
    def test_shipping_type_valid(self ):
        for type in ["SD", "ND", "2D", "ST", "sD", " ND", " 2D ", "st"]:
            st = ShippingType(type)
            self.assertTrue(isinstance(st, ShippingType))

    def test_shipping_type_incorrect_string(self):
        for bad_type in ["42", "<script>alert(42)</script>", None, "", 42]:
            expected = "Expected shipping type in "
            with self.assertRaisesRegex(RisException, expected) as ct:
                st = ShippingType(bad_type)


if __name__ == "__main__":
    unittest.main()
