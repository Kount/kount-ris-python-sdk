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
from util.khash import Khash


class TestKhash(unittest.TestCase):
    def setUp(self):
        self.k = Khash
        self.list_for_hash = ["4111111111111111", '5199185454061655', 4259344583883]
        self.expected = ['WMS5YA6FUZA1KC', '2NOQRXNKTTFL11', 'FEXQI1QS6TH2O5']
        self.merchant_id = '666666'

    def test_token_valid(self): 
        for i, plain_text in enumerate(self.list_for_hash):
            card_solted = self.k.hash_payment_token(token=plain_text)
            e = "%s%s"%(str(self.list_for_hash[i])[:6], self.expected[i])
            self.assertEqual(card_solted, e)
            self.assertTrue(self.k.khashed(card_solted))

    def test_token_invalid(self): 
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_payment_token(token="")
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_payment_token(token=None)
        card_solted = self.k.hash_payment_token(token=10**100000)
        self.assertEqual(card_solted, "100000QKX0L46T00RKBW")
        self.assertTrue(self.k.khashed(card_solted))
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_payment_token(token=-42)
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_payment_token(token=0)
        card_solted = self.k.hash_payment_token(token="Beatles")
        self.assertEqual(card_solted, "Beatle5STRFTYPXBR14E")
        self.assertEqual(self.k.khashed(card_solted), None)
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_payment_token(token="John")
        #self.assertEqual(card_solted, "John2IMOTT3HMQ7T7L")

    def test_hash_gift_card(self):
        for i in range(len(self.list_for_hash)):
            card_solted = self.k.hash_gift_card(self.merchant_id, self.list_for_hash[i])
            e = "%s%s"%(self.merchant_id, self.expected[i])
            self.assertEqual(card_solted, e)
            self.assertTrue(self.k.khashed(card_solted))

    def test_hash_gift_card_int_merchantid(self):
        for i in range(len(self.list_for_hash)):
            card_solted = self.k.hash_gift_card(self.merchant_id, self.list_for_hash[i])
            e = "%s%s"%(self.merchant_id, self.expected[i])
            self.assertEqual(card_solted, e)
            self.assertTrue(self.k.khashed(card_solted))

    def test_list_for_hash_empty(self):
        list_for_hash = ""
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_gift_card(self.merchant_id, list_for_hash)
        #self.assertEqual(card_solted, '666666TBNC2MTR28JOUY')

    def test_list_for_hash_none(self):
        list_for_hash = None
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_gift_card(self.merchant_id, list_for_hash)
        #self.assertEqual(card_solted, '6666663RQF4EOYA9EUUI')

    def test_gift_card_empty_values(self):
        list_for_hash = []
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_gift_card(self.merchant_id, list_for_hash)

    def test_gift_card_no_merchant(self):
        list_for_hash = []
        merchant_id = ""
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_gift_card(merchant_id, list_for_hash)

    def test_gift_card_merchant_empty_str(self):
        merchant_id = ""
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_gift_card(merchant_id, self.list_for_hash)

    def test_list_for_hash_merchant_none(self):
        list_for_hash = []
        merchant_id = None
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_gift_card(merchant_id, list_for_hash)

    def test_list_for_hash_args_missing(self):
        list_for_hash = None
        merchant_id = None
        with self.assertRaises(ValueError):
            card_solted = self.k.hash_gift_card(merchant_id, list_for_hash)


if __name__ == "__main__":
    unittest.main(
        #defaultTest = "TestKhash.test_token_invalid"
        )
