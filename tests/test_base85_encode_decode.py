#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"Base85 Encode Decode Test"
from __future__ import absolute_import, unicode_literals, division, print_function
import unittest
try:
    from base64 import a85encode, a85decode
    py27 = False
except ImportError:
    from mom.codec.base85 import b85encode as a85encode, b85decode as a85decode
    py27 = True

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class Base85EncodeDecodeTest(unittest.TestCase):
    "Base85EncodeDecodeTest"
    def setUp(self):
        self.plain_text = b"This is sample text for testing purposes."
        self.encoded_text = b"<+oue+DGm>F(&p)Ch4`2AU&;>AoD]4FCfN8Bl7Q+E-62?Df]K2/c"

    def test_encode(self):
        "test valid encode"
        encoded = a85encode(self.plain_text)
        decoded = a85decode(encoded)
        self.assertEqual(encoded, self.encoded_text)
        self.assertEqual(decoded, self.plain_text)

    def test_decode(self):
        "test valid decode"
        decoded = a85decode(self.encoded_text)
        self.assertEqual(decoded, self.plain_text)

    def test_decode_invalid(self):
        "test invalid decode"
        decoded = a85decode(self.encoded_text[:5])
        self.assertEqual(decoded, self.plain_text[:5].strip())
        self.assertEqual(decoded, self.plain_text[:4])
        decoded = a85decode(b'')
        self.assertEqual(decoded, b'')

    def test_encode_invalid(self):
        "test invalid encode"
        encoded = a85encode(b'')
        self.assertEqual(encoded, b'')
        encoded = a85encode(self.plain_text[:5])
        self.assertEqual(encoded, b'<+oue+9')
        test_str = 'ABC'
        self.assertRaises(TypeError, a85encode, '')
        self.assertRaises(TypeError, a85encode, test_str)
        if not py27:
            self.assertRaises(TypeError, a85encode, str(self.plain_text))
        b = bytearray(test_str, 'utf-8')
        expected = b'5sdp'
        if py27:
            self.assertEqual(expected, a85encode(str(b)))
            b = bytes(test_str)
            self.assertEqual(expected, a85encode(str(b)))
            self.assertEqual(expected, a85encode(b'ABC'))
            self.assertEqual(expected, a85encode(b))
        else:
            self.assertEqual(expected, a85encode(b))
            b = bytes(test_str, 'utf-8')
            self.assertEqual(expected, a85encode(b))


if __name__ == "__main__":
    unittest.main(verbosity=2)
