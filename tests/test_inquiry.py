#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""Test Cases for Inquiry class"""
from __future__ import absolute_import, unicode_literals, division, print_function
import unittest
import uuid
from kount.request import (ASTAT, BCRSTAT, INQUIRYMODE,
                           CURRENCYTYPE, MERCHANTACKNOWLEDGMENT)
from kount.inquiry import Inquiry
from kount.util.payment import CardPayment, Payment, GiftCardPayment
from kount.util.cartitem import CartItem
from kount.util.address import Address
from kount.settings import SDK_VERSION

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


EMAIL_CLIENT = "sdkTest@kountsdktestdomain.com"
MERCHANT_ID = '999666'
PTOK = "0007380568572514"


BILLING_ADDRESS = Address("1234 North B2A1 Tree Lane South",
                          "", "Albuquerque", "NM", "87101", "US")
SHIPPING_ADDRESS = Address("567 West S2A1 Court North", "",
                           "Gnome", "AK", "99762", "US")

expected = {
    'ANID': '',
    'AUTH': 'A',
    'AVST': 'M',
    'AVSZ': 'M',
    'B2A1': '1234 North B2A1 Tree Lane South',
    'B2A2': '',
    'B2CC': 'US',
    'B2CI': 'Albuquerque',
    'B2PC': '87101',
    'B2PN': '555-867-5309',
    'B2ST': 'NM',
    'BPREMISE': '',
    'BSTREET': '',
    'CASH': '4444',
    'CURR': 'USD',
    'CVVR': 'M',
    'EMAL': EMAIL_CLIENT,
    'FRMT': 'JSON',
    #~ 'IPAD': '131.206.45.21',
    'LAST4': '2514',
    'MACK': 'Y',
    'MERC': '999666',
    'MODE': 'Q',
    'NAME': 'SdkTestFirstName SdkTestLastName',
    'PENC': 'KHASH',
    #~ 'PENC': '',
    'PROD_DESC[0]': '3000 CANDLEPOWER PLASMA FLASHLIGHT',
    'PROD_ITEM[0]': 'SG999999',
    'PROD_PRICE[0]': '68990',
    'PROD_QUANT[0]': '2',
    'PROD_TYPE[0]': 'SPORTING_GOODS',
    #~ 'PTOK': '0007380568572514',
    'PTOK': '000738F16NA2S935A5HY', #for khashed=True in Payment
    'PTYP': 'CARD',
    'S2A1': '567 West S2A1 Court North',
    'S2A2': '',
    'S2CC': 'US',
    'S2CI': 'Gnome',
    'S2EM': 'sdkTestShipToEmail@kountsdktestdomain.com',
    'S2NM': 'SdkShipToFN SdkShipToLN',
    'S2PC': '99762',
    'S2PN': '555-777-1212',
    'S2ST': 'AK',
    'SDK': 'CUST',
    'SDK_VERSION': 'Sdk-Ris-Python-%s' % SDK_VERSION,
    'SITE': 'DEFAULT',
    'SPREMISE': '',
    'SSTREET': '',
    'TOTL': '123456',
    'VERS': SDK_VERSION,
    }

def generate_unique_id():
    "unique session id"
    return str(uuid.uuid4()).replace('-', '').upper()


def default_inquiry(session_id, merchant_id, email_client, ptok, payment, khashed):
    "default_inquiry, PENC is not set"
    result = Inquiry()
    result.request_mode(INQUIRYMODE.DEFAULT)
    result.shipping_address(SHIPPING_ADDRESS)
    result.shipping_name("SdkShipToFN SdkShipToLN") #S2NM
    result.billing_address(BILLING_ADDRESS)
    result.currency_set(CURRENCYTYPE.USD)   #CURR
    result.total_set('123456') #TOTL
    result.billing_phone_number("555-867-5309") #B2PN
    result.shipping_phone_number("555-777-1212") #S2PN
    result.email_client(email_client)
    result.customer_name("SdkTestFirstName SdkTestLastName")
    result.unique_customer_id(session_id[:20]) #UNIQ
    result.website("DEFAULT") #SITE
    result.email_shipping("sdkTestShipToEmail@kountsdktestdomain.com")
    result.ip_address("4.127.51.215") #IPAD
    cart_item = []
    cart_item.append(CartItem("SPORTING_GOODS", "SG999999",
                              "3000 CANDLEPOWER PLASMA FLASHLIGHT",
                              '2', '68990'))
    result.shopping_cart(cart_item)
    result.version()
    result.version_set(SDK_VERSION)  #0695
    result.merchant_set(merchant_id)
    result.payment_set(payment) #PTOK
    result.session_set(session_id) #SESS
    result.order_number(session_id[:10])  #ORDR
    result.authorization_status(ASTAT.Approve) #AUTH
    result.avs_zip_reply(BCRSTAT.MATCH)
    result.avs_address_reply(BCRSTAT.MATCH)
    result.avs_cvv_reply(BCRSTAT.MATCH)
    result.merchant_acknowledgment_set(MERCHANTACKNOWLEDGMENT.TRUE) #"MACK"
    result.cash('4444')
    if khashed:
        result.khash_payment_encoding(enabled=True)
    return result


class TestInquiry(unittest.TestCase):
    "Inquiry class tests"
    maxDiff = None

    def setUp(self):
        self.session_id = str(generate_unique_id())

    def test_utilities(self):
        "test_utilities"
        payment = Payment(payment_type="CARD", payment_token=PTOK,
                          khashed=False)
        self.assertEqual(payment.payment_type, 'CARD')
        self.assertEqual(payment.last4, '2514')
        self.assertEqual(payment.payment_token, '0007380568572514')
        self.assertFalse(payment.khashed)
        result = default_inquiry(
            session_id=self.session_id,
            merchant_id=MERCHANT_ID,
            email_client=EMAIL_CLIENT, ptok=PTOK,
            payment=payment, khashed=False)
        expected_not_khashed = expected.copy()
        expected_not_khashed["PTOK"] = '0007380568572514'
        actual = result.params
        self.assertEqual(actual['PTYP'], 'CARD')
        self.assertIn(expected_not_khashed['SDK_VERSION'],
                      actual['SDK_VERSION'])
        del (actual['UNIQ'], actual['IPAD'], actual['SDK_VERSION'],
             expected_not_khashed['SDK_VERSION'], expected_not_khashed['PENC'],
             actual['SESS'], actual['ORDR'])
        self.assertEqual(actual, expected_not_khashed)

    def test_utilities_khashed(self):
        "test_utilities khashed"
        _expected = expected.copy()
        payment = CardPayment(PTOK, khashed=True)
        self.assertEqual(payment.payment_type, 'CARD')
        self.assertEqual(payment.last4, '2514')
        self.assertEqual(payment.payment_token, '000738F16NA2S935A5HY')
        self.assertTrue(payment.khashed)
        result = default_inquiry(
            session_id=self.session_id,
            merchant_id=MERCHANT_ID,
            email_client=EMAIL_CLIENT, ptok=PTOK, payment=payment, khashed=True)
        actual = result.params
        self.assertEqual(actual['PTYP'], 'CARD')
        self.assertIn(_expected['SDK_VERSION'], actual['SDK_VERSION'])
        del (actual['UNIQ'], actual['IPAD'], actual['SDK_VERSION'],
             actual['SESS'], actual['ORDR'], _expected['SDK_VERSION'])
        self.assertEqual(actual, _expected)

    def test_utilities_gift_khashed(self):
        "test_utilities GIFT khashed"
        #~ payment = CardPayment(PTOK, khashed=True)
        _expected = expected.copy()
        payment = GiftCardPayment(PTOK, khashed=True)
        self.assertEqual(payment.payment_type, 'GIFT')
        self.assertEqual(payment.last4, '2514')
        self.assertEqual(payment.payment_token, '000738F16NA2S935A5HY')
        self.assertTrue(payment.khashed)
        result = default_inquiry(
            session_id=self.session_id,
            merchant_id=MERCHANT_ID,
            email_client=EMAIL_CLIENT, ptok=PTOK, payment=payment, khashed=True)
        actual = result.params
        self.assertEqual(actual['PTYP'], 'GIFT')
        self.assertIn(_expected['SDK_VERSION'], actual['SDK_VERSION'])
        del (actual['PTYP'], _expected['PTYP'], actual['UNIQ'], actual['IPAD'],
             actual['SDK_VERSION'], actual['SESS'],
             actual['ORDR'], _expected['SDK_VERSION'])
        self.assertEqual(actual, _expected)


if __name__ == "__main__":
    unittest.main()
