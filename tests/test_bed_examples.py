#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""Test Cases for an example implementation
generate_unique_id
put test data in user_inquiry
"""
from __future__ import absolute_import, unicode_literals, division, print_function
import unittest
import inittest
from test_inquiry import generate_unique_id
from kount.response import Response
from kount.client import Client
from kount.settings import RAISE_ERRORS
from kount.util.payment import CardPayment
from kount.inquiry import Inquiry
from kount.request import (ASTAT, BCRSTAT, INQUIRYMODE,
                           CURRENCYTYPE, MERCHANTACKNOWLEDGMENT)
from kount.util.cartitem import CartItem
from kount.util.address import Address
from kount.settings import (SDK_VERSION, SDK)
from kount.version import VERSION
from .settings import (INTEGRATION_TEST_URL, TEST_MERCHANT_ID, TEST_MERCHANT_API_KEY)

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


URL_API = INTEGRATION_TEST_URL 
URL_API_BETA = URL_API
MERCHANT_ID6 = TEST_MERCHANT_ID 
PTOK = "4111111111111111"
EMAIL = 'john@test.com'
KOUNT_API_KEY6 = TEST_MERCHANT_API_KEY

BILLING_ADDRESS = Address("", "", "Manchester", "NH", "03109", "US")
BILLING_PHONE = "555-888-5678"

def user_inquiry(session_id, merchant_id, email_client, payment):
    "user_inquiry, PENC is not set"
    result = Inquiry()
    result.request_mode(INQUIRYMODE.DEFAULT)
    result.billing_address(BILLING_ADDRESS)
    result.currency_set(CURRENCYTYPE.USD)   #CURR
    result.total_set(3500) #TOTL
    result.billing_phone_number(BILLING_PHONE) #B2PN
    result.email_client(email_client)
    result.customer_name("J Test")
    result.unique_customer_id(session_id[:20]) #UNIQ
    result.website("DEFAULT") #SITE
    result.ip_address("4.127.51.215") #IPAD
    cart_item = []
    cart_item.append(CartItem("1", "8482",
                              "Standard Monthly Plan",
                              1, '3500'))
    result.shopping_cart(cart_item)
    result.version()
    result.version_set(SDK_VERSION)  #0695
    result.merchant_set(merchant_id)
    result.payment_set(payment) #PTOK
    result.session_set(session_id) #SESS
    result.order_number(session_id[:10])  #ORDR
    result.authorization_status(ASTAT.Approve) #AUTH
    result.avs_zip_reply(BCRSTAT.MATCH)
    result.params_set("SDK",SDK)
    result.avs_address_reply(BCRSTAT.MATCH)
    result.avs_cvv_reply(BCRSTAT.MATCH)
    result.merchant_acknowledgment_set(MERCHANTACKNOWLEDGMENT.TRUE) #"MACK"
    return result

expected = {
    'ANID': '',
    'AUTH': 'A',
    'AVST': 'M',
    'AVSZ': 'M',
    'B2A1': '',
    'B2A2': '',
    'B2CC': 'US',
    'B2CI': 'Manchester',
    'B2PC': '03109',
    'B2PN': BILLING_PHONE,
    'B2ST': 'NH',
    'BPREMISE': '',
    'BSTREET': '',
    'CURR': 'USD',
    'CVVR': 'M',
    'EMAL': EMAIL,
    'FRMT': 'JSON',
    'IPAD': '4.127.51.215',
    'LAST4': '1111',
    'MACK': 'Y',
    'MERC': '999666',
    'MODE': 'Q',
    'NAME': 'J Test',
    #~ 'ORDR': '4F7132C2FE',
    #~ 'PENC': 'KHASH',
    'PROD_DESC[0]': 'Standard Monthly Plan',
    'PROD_ITEM[0]': '8482',
    'PROD_PRICE[0]': '3500',
    'PROD_QUANT[0]': 1,
    'PROD_TYPE[0]': '1',
    'PTOK': PTOK,
    'PTYP': 'CARD',
    'SDK': SDK,
    #~ 'SDK_VERSION': 'Sdk-Ris-Python-0695-201708301601',
    #~ 'SESS': '4F7132C2FE8547928CD9329B78AA0A59',
    'SITE': 'DEFAULT',
    'TOTL': 3500,
    #~ 'UNIQ': '4F7132C2FE8547928CD9',
    'VERS': '0695'}


class TestBed(unittest.TestCase):
    "Test Bed for use-cases, with & without Khash"
    maxDiff = None

    def setUp(self):
        self.session_id = generate_unique_id()[:32]
        self.email_client = EMAIL

    def test_not_khashed(self):
        "test without khashed card"
        #~ required khashed=False
        payment = CardPayment(PTOK, False)
        self.inq = user_inquiry(
            self.session_id, MERCHANT_ID6, self.email_client,
            payment=payment)
        self.assertNotIn('PENC', self.inq.params)
        self.compare(expected)

    def test_khashed(self):
        "test with khashed card"
        #~ not required default khashed=True
        payment = CardPayment(PTOK)
        self.inq = user_inquiry(
            self.session_id, MERCHANT_ID6, self.email_client,
            payment=payment)
        self.assertIn('PENC', self.inq.params)
        self.assertEqual('KHASH', self.inq.params['PENC'])
        expected_khashed = expected.copy()
        expected_khashed['PENC'] = 'KHASH'
        expected_khashed['PTOK'] = '411111WMS5YA6FUZA1KC'
        self.compare(expected_khashed)

    def compare(self, expected_dict):
        "common method for both tests"
        res = Client(URL_API_BETA, KOUNT_API_KEY6,
                     raise_errors=RAISE_ERRORS).process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertNotIn('ERRO', rr.params)
        actual = self.inq.params.copy()
        remove = ['SDK_VERSION', 'SESS', 'UNIQ', 'ORDR']
        for k in remove:
            if k in actual:
                del actual[k]
        self.assertEqual(expected_dict, actual)


if __name__ == "__main__":
    unittest.main(verbosity=2)
