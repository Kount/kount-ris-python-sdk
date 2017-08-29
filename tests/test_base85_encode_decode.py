#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"Base85 Encode Decode Test"
from __future__ import absolute_import, unicode_literals, division, print_function
import unittest
import sys

if sys.version_info[0] > 2:
    from base64 import a85encode, a85decode
    py27 = False
else:
    from mom.codec.base85 import b85encode as a85encode, b85decode as a85decode
    py27 = True
from kount.version import VERSION

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class Base85EncodeDecodeTest(unittest.TestCase):
    "Base85EncodeDecodeTest"
    def setUp(self):
        self.plain_text = "This is sample text for testing purposes."
        self.encoded_text = b"<+oue+DGm>F(&p)Ch4`2AU&;>AoD]4FCfN8Bl7Q+E-62?Df]K2/c"

    def test_encode(self):
        "test valid encode"
        encoded = a85encode(self.plain_text.encode('utf-8'))
        decoded = a85decode(encoded)
        self.assertEqual(encoded, self.encoded_text)
        self.assertEqual(decoded, self.plain_text.encode('utf-8'))

    def test_decode(self):
        "test valid decode"
        decoded = a85decode(self.encoded_text)
        self.assertEqual(decoded, self.plain_text.encode('utf-8'))

    def test_decode_invalid(self):
        "test invalid decode"
        self.assertEqual(a85decode(b''), b'')
        if not py27:
            self.assertRaises(ValueError, a85decode, self.plain_text)
        else:
            self.assertRaises(TypeError, a85decode, self.plain_text)

    def test_encode_invalid(self):
        "test invalid encode"
        self.assertEqual(a85encode(b''), b'')
        self.assertRaises(TypeError, a85encode, '')
        self.assertRaises(TypeError, a85encode, self.plain_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
