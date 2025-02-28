#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2025 Kount an Equifax Company All Rights Reserved.
import unittest
import pytest

from kount.version import VERSION
from kount.util.khash import Khash
from kount.config import SDKConfig

__author__ = SDKConfig.SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDKConfig.SDK_MAINTAINER
__email__ = SDKConfig.MAINTAINER_EMAIL
__status__ = SDKConfig.STATUS


@pytest.mark.usefixtures("conf_key")
class TestKhash(unittest.TestCase):
    """Khash class test cases"""

    def setUp(self):
        self.list_for_hash = ["4111111111111111",
                              '5199185454061655',
                              4259344583883]
        self.expected = ['WMS5YA6FUZA1KC', '2NOQRXNKTTFL11', 'FEXQI1QS6TH2O5']
        self.merchant_id = '666666'
        self.khash = Khash.get()

    def test_token_valid(self):
        """valid token"""
        self.assertEqual(
            "BADTOKGM3BD98ZY871QB",
            self.khash.hash_payment_token(token="BADTOKEN"))

        self.assertEqual(
            "000738F16NA2S935A5HY",
            self.khash.hash_payment_token(token="0007380568572514"))

        for i, plain_text in enumerate(self.list_for_hash):
            card_hashed = self.khash.hash_payment_token(token=plain_text)
            expected = "%s%s" % (str(self.list_for_hash[i])[:6],
                                 self.expected[i])
            self.assertEqual(card_hashed, expected)
            self.assertTrue(self.khash.khashed(card_hashed))

    def test_token_invalid(self):
        """invalid token"""
        with self.assertRaises(ValueError):
            self.khash.hash_payment_token(token="")
        with self.assertRaises(ValueError):
            self.khash.hash_payment_token(token=None)
        card_hashed = self.khash.hash_payment_token(token="10**200")
        self.assertEqual(card_hashed, "10**20GA6AXR02LVUE5X")
        with self.assertRaises(ValueError):
            self.khash.hash_payment_token(token=-42)
        with self.assertRaises(ValueError):
            self.khash.hash_payment_token(token=10**200)
        with self.assertRaises(ValueError):
            self.khash.hash_payment_token(token=0)
        card_hashed = self.khash.hash_payment_token(token="Beatles")
        self.assertEqual(card_hashed, "Beatle5STRFTYPXBR14E")
        self.assertTrue(self.khash.khashed(card_hashed))
        bad = "John"
        try:
            self.khash.hash_payment_token(token=bad)
        except ValueError as vale:
            self.assertEqual("incorrect arg: [%s]" % bad, str(vale))
        with self.assertRaises(ValueError):
            self.assertTrue(self.khash.hash_payment_token(token=bad))

    def test_hash_gift_card(self):
        """gift card"""
        for i in range(len(self.list_for_hash)):
            card_hashed = self.khash.hash_gift_card(
                self.merchant_id, self.list_for_hash[i])
            expected = "%s%s" % (self.merchant_id, self.expected[i])
            self.assertEqual(card_hashed, expected)
            self.assertTrue(self.khash.khashed(card_hashed))

    def test_hash_gift_card_int_merchantid(self):
        """test_hash_gift_card_int_merchantid"""
        for i in range(len(self.list_for_hash)):
            card_hashed = self.khash.hash_gift_card(
                self.merchant_id, self.list_for_hash[i])
            expected = "%s%s" % (self.merchant_id, self.expected[i])
            self.assertEqual(card_hashed, expected)
            self.assertTrue(self.khash.khashed(card_hashed))

    def test_list_for_hash_empty(self):
        """list_for_hash_empty"""
        list_for_hash = ""
        with self.assertRaises(ValueError):
            self.khash.hash_gift_card(self.merchant_id, list_for_hash)

    def test_list_for_hash_none(self):
        """hash_none"""
        list_for_hash = None
        with self.assertRaises(ValueError):
            self.khash.hash_gift_card(self.merchant_id, list_for_hash)

    def test_gift_card_empty_values(self):
        """gift_card_empty_values"""
        list_for_hash = []
        with self.assertRaises(ValueError):
            self.khash.hash_gift_card(self.merchant_id, list_for_hash)

    def test_gift_card_no_merchant(self):
        """gift card without merchant"""
        list_for_hash = []
        merchant_id = ""
        with self.assertRaises(ValueError):
            self.khash.hash_gift_card(merchant_id, list_for_hash)

    def test_gift_card_merchant_empty_str(self):
        """gift_card_merchant_empty_str"""
        merchant_id = ""
        with self.assertRaises(ValueError):
            self.khash.hash_gift_card(merchant_id, self.list_for_hash)

    def test_list_for_hash_merchant_none(self):
        """list_for_hash_merchant_none"""
        list_for_hash = []
        merchant_id = None
        with self.assertRaises(ValueError):
            self.khash.hash_gift_card(merchant_id, list_for_hash)

    def test_list_for_hash_args_missing(self):
        """list_for_hash_args_missing"""
        list_for_hash = None
        merchant_id = None
        with self.assertRaises(ValueError):
            self.khash.hash_gift_card(merchant_id, list_for_hash)


if __name__ == "__main__":
    unittest.main(verbosity=2)
