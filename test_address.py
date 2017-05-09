#!/usr/bin/env python
# -*- coding: utf-8 -*-
#~ This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

import unittest
from util.address import  Address


class TestAddress(unittest.TestCase):
    def test_address_valid(self):
        st = Address(address1="567 West S2A1 Court North", address2=None, state="Gnome", postal_code="AK", premise="99762", country="US")
        self.assertTrue(isinstance(st, Address))
        st = Address("1234 North B2A1 Tree Lane South", None, "Albuquerque", "NM", "87101", "US")
        self.assertTrue(isinstance(st, Address))
        st = Address("567 West S2A1 Court North", None, "Gnome", "AK", "99762", "US")
        self.assertEqual("567 West S2A1 Court North", str(st.address1))

    def test_address_incorrect_string(self):
        for bad_type in [42**42, "<script>alert(42)</script>", None, "", 42]:
            st = Address(bad_type)
            self.assertEqual("", str(st.country))


if __name__ == "__main__":
    unittest.main()
