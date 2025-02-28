#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2025 Kount an Equifax Company All Rights Reserved.
import unittest
from kount.util.address import Address
from kount.version import VERSION
from kount.config import SDKConfig

__author__ = SDKConfig.SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDKConfig.SDK_MAINTAINER
__email__ = SDKConfig.MAINTAINER_EMAIL
__status__ = SDKConfig.STATUS


class TestAddress(unittest.TestCase):
    """Address class test cases"""

    def test_address_valid(self):
        """valid address"""
        adr = Address(address1="567 West S2A1 Court North",
                      address2=None, state="Gnome", postal_code="AK",
                      premise="99762", country="US")
        self.assertTrue(isinstance(adr, Address))
        adr = Address("1234 North B2A1 Tree Lane South", None,
                      "Albuquerque", "NM", "87101", "US")
        self.assertTrue(isinstance(adr, Address))
        adr = Address("567 West S2A1 Court North", None,
                      "Gnome", "AK", "99762", "US")
        self.assertEqual("567 West S2A1 Court North", str(adr.address1))

    def test_address_incorrect_string(self):
        """incorrect address"""
        for bad_type in [42**42, "<script>alert(42)</script>", None, "", 42]:
            adr = Address(bad_type)
            self.assertEqual("", str(adr.country))

    def test_address_cyrillic(self):
        """incorrect address - cyrillic"""
        for bad_type in ["Сирма", "'%=:*-+<", "ъ"]:
            adr = Address(bad_type)
            self.assertEqual("", str(adr.country))
            self.assertEqual(bad_type, adr.address1)


if __name__ == "__main__":
    unittest.main()
