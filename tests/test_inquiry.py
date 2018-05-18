#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""Test Cases for Inquiry class"""
import pytest
import unittest
import uuid

from kount.client import Client
from kount.request import (AuthStatus, BankcardReply, InquiryMode,
                           CurrencyType, MerchantAcknowledgment)
from kount.inquiry import Inquiry
from kount.util.payment import CardPayment, Payment, GiftCardPayment
from kount.util.cartitem import CartItem
from kount.util.address import Address
from kount.config import SDKConfig
from kount.version import VERSION

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"

EMAIL_CLIENT = "sdkTest@kountsdktestdomain.com"
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
    # 'IPAD': '131.206.45.21',
    'LAST4': '2514',
    'MACK': 'Y',
    'MERC': '999666',
    'MODE': 'Q',
    'NAME': 'SdkTestFirstName SdkTestLastName',
    'PENC': 'KHASH',
    # 'PENC': '',
    'PROD_DESC[0]': '3000 CANDLEPOWER PLASMA FLASHLIGHT',
    'PROD_ITEM[0]': 'SG999999',
    'PROD_PRICE[0]': '68990',
    'PROD_QUANT[0]': '2',
    'PROD_TYPE[0]': 'SPORTING_GOODS',
    # 'PTOK': '0007380568572514',
    'PTOK': '000738F16NA2S935A5HY',  # for khashed=True in Payment
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
    'SDK_VERSION': 'Sdk-Ris-Python-%s' % SDKConfig.SDK_VERSION,
    'SITE': 'DEFAULT',
    'SPREMISE': '',
    'SSTREET': '',
    'TOTL': '123456',
    'VERS': SDKConfig.SDK_VERSION,
}


def generate_unique_id():
    """unique session id"""
    return str(uuid.uuid4()).replace('-', '').upper()


def default_inquiry(merchant_id, session_id, email_client, payment):
    """default_inquiry, PENC is not set"""
    inq = Inquiry()
    inq.set_request_mode(InquiryMode.DEFAULT)
    inq.set_shipping_address(SHIPPING_ADDRESS)
    inq.set_shipping_name("SdkShipToFN SdkShipToLN")  # S2NM
    inq.set_billing_address(BILLING_ADDRESS)
    inq.set_currency(CurrencyType.USD)  # CURR
    inq.set_total('123456')  # TOTL
    inq.set_billing_phone_number("555-867-5309")  # B2PN
    inq.set_shipping_phone_number("555-777-1212")  # S2PN
    inq.set_email_client(email_client)
    inq.set_customer_name("SdkTestFirstName SdkTestLastName")
    inq.set_unique_customer_id(session_id[:20])  # UNIQ
    inq.set_website("DEFAULT")  # SITE
    inq.set_email_shipping("sdkTestShipToEmail@kountsdktestdomain.com")
    inq.set_ip_address("4.127.51.215")  # IPAD
    cart_items = list()
    cart_items.append(CartItem("SPORTING_GOODS", "SG999999",
                               "3000 CANDLEPOWER PLASMA FLASHLIGHT",
                               '2', '68990'))
    inq.set_shopping_cart(cart_items)
    inq.version()
    inq.set_version(SDKConfig.SDK_VERSION)  # 0695
    inq.set_merchant(merchant_id)
    inq.set_payment(payment)  # PTOK
    inq.set_session_id(session_id)  # SESS
    inq.set_order_number(session_id[:10])  # ORDR
    inq.set_authorization_status(AuthStatus.APPROVE)  # AUTH
    inq.set_avs_zip_reply(BankcardReply.MATCH)
    inq.set_avs_address_reply(BankcardReply.MATCH)
    inq.set_avs_cvv_reply(BankcardReply.MATCH)
    inq.set_merchant_acknowledgment(MerchantAcknowledgment.TRUE)  # "MACK"
    inq.set_cash('4444')
    return inq


@pytest.mark.usefixtures("api_url", "api_key", "merchant_id")
class TestInquiry(unittest.TestCase):
    """Inquiry class tests"""
    maxDiff = None

    merchant_id = None
    api_key = None
    api_url = None

    def setUp(self):
        self.session_id = str(generate_unique_id())
        self.client = Client(self.api_url, self.api_key)

    def test_utilities(self):
        """test_utilities"""
        payment = Payment(
            payment_type="CARD",
            payment_token=PTOK,
            khashed=False)
        self.assertEqual(payment._payment_type, 'CARD')
        self.assertEqual(payment.last4, '2514')
        self.assertEqual(payment.payment_token, '0007380568572514')
        self.assertFalse(payment.khashed)
        inq = default_inquiry(
            merchant_id=self.merchant_id,
            session_id=self.session_id,
            email_client=EMAIL_CLIENT,
            payment=payment)

        expected_not_khashed = expected.copy()
        expected_not_khashed["PTOK"] = '0007380568572514'
        actual = inq.params
        self.assertEqual(actual['PTYP'], 'CARD')
        self.assertIn(expected_not_khashed['SDK_VERSION'],
                      actual['SDK_VERSION'])

        del (actual['UNIQ'],
             actual['IPAD'],
             actual['SDK_VERSION'],
             actual['SESS'],
             actual['ORDR'],
             expected_not_khashed['SDK_VERSION'],
             expected_not_khashed['PENC'])

        self.assertEqual(actual, expected_not_khashed)

    def test_utilities_khashed(self):
        """test_utilities khashed"""
        _expected = expected.copy()
        payment = CardPayment(PTOK)
        self.assertEqual(payment._payment_type, 'CARD')
        self.assertEqual(payment.last4, '2514')
        self.assertEqual(payment.payment_token, '000738F16NA2S935A5HY')
        self.assertTrue(payment.khashed)
        result = default_inquiry(
            session_id=self.session_id,
            merchant_id=self.merchant_id,
            email_client=EMAIL_CLIENT,
            payment=payment)
        actual = result.params
        self.assertEqual(actual['PTYP'], 'CARD')
        self.assertIn(_expected['SDK_VERSION'], actual['SDK_VERSION'])
        del (actual['UNIQ'],
             actual['IPAD'],
             actual['SDK_VERSION'],
             actual['SESS'],
             actual['ORDR'],
             _expected['SDK_VERSION'])
        self.assertEqual(actual, _expected)

    def test_utilities_gift_khashed(self):
        """test_utilities GIFT khashed"""
        _expected = expected.copy()
        payment = GiftCardPayment(PTOK)
        self.assertEqual(payment._payment_type, 'GIFT')
        self.assertEqual(payment.last4, '2514')
        self.assertEqual(payment.payment_token, '000738F16NA2S935A5HY')
        self.assertTrue(payment.khashed)
        result = default_inquiry(
            session_id=self.session_id,
            merchant_id=self.merchant_id,
            email_client=EMAIL_CLIENT,
            payment=payment)
        actual = result.params
        self.assertEqual(actual['PTYP'], 'GIFT')
        self.assertIn(_expected['SDK_VERSION'], actual['SDK_VERSION'])
        del (_expected['SDK_VERSION'],
             _expected['PTYP'],
             actual['PTYP'],
             actual['UNIQ'],
             actual['IPAD'],
             actual['SDK_VERSION'],
             actual['SESS'],
             actual['ORDR'])
        self.assertEqual(actual, _expected)


if __name__ == "__main__":
    unittest.main()
