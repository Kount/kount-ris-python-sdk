#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""Test Cases for an example implementation
generate_unique_id
put test data in user_inquiry
"""
import unittest
import pytest

from kount.client import Client
from kount.config import SDKConfig
from kount.util.payment import CardPayment
from kount.inquiry import Inquiry
from kount.request import (AuthStatus, BankcardReply, InquiryMode,
                           CurrencyType, MerchantAcknowledgment)
from kount.util.cartitem import CartItem
from kount.util.address import Address
from kount.version import VERSION

from .test_inquiry import generate_unique_id

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


PTOK = "4111111111111111"
EMAIL = 'john@test.com'
BILLING_ADDRESS = Address("", "", "Manchester", "NH", "03109", "US")
BILLING_PHONE = "555-888-5678"


def user_inquiry(session_id, merchant_id, email_client, payment):
    """user_inquiry, PENC is not set"""
    result = Inquiry()
    result.set_request_mode(InquiryMode.DEFAULT)
    result.set_billing_address(BILLING_ADDRESS)
    result.set_currency(CurrencyType.USD)  # CURR
    result.set_total(3500)  # TOTL
    result.set_billing_phone_number(BILLING_PHONE)  # B2PN
    result.set_email_client(email_client)
    result.set_customer_name("J Test")
    result.set_unique_customer_id(session_id[:20])  # UNIQ
    result.set_website("DEFAULT")  # SITE
    result.set_ip_address("4.127.51.215")  # IPAD
    cart_items = [CartItem("1", "8482", "Standard Monthly Plan", 1, '3500')]
    result.set_shopping_cart(cart_items)
    result.version()
    result.set_version(SDKConfig.SDK_VERSION)  # 0695
    result.set_merchant(merchant_id)
    result.set_payment(payment)  # PTOK
    result.set_session_id(session_id)  # SESS
    result.set_order_number(session_id[:10])  # ORDR
    result.set_authorization_status(AuthStatus.APPROVE)  # AUTH
    result.set_avs_zip_reply(BankcardReply.MATCH)
    result.set_avs_address_reply(BankcardReply.MATCH)
    result.set_avs_cvv_reply(BankcardReply.MATCH)
    result.set_merchant_acknowledgment(MerchantAcknowledgment.TRUE)  # "MACK"
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
    # 'ORDR': '4F7132C2FE',
    # 'PENC': 'KHASH',
    'PROD_DESC[0]': 'Standard Monthly Plan',
    'PROD_ITEM[0]': '8482',
    'PROD_PRICE[0]': '3500',
    'PROD_QUANT[0]': 1,
    'PROD_TYPE[0]': '1',
    'PTOK': PTOK,
    'PTYP': 'CARD',
    'SDK': 'CUST',
    # 'SDK_VERSION': 'Sdk-Ris-Python-0695-201708301601',
    # 'SESS': '4F7132C2FE8547928CD9329B78AA0A59',
    'SITE': 'DEFAULT',
    'TOTL': 3500,
    # 'UNIQ': '4F7132C2FE8547928CD9',
    'VERS': '0695'}


@pytest.mark.usefixtures("api_url", "api_key", "merchant_id")
class TestBed(unittest.TestCase):
    """Test Bed for use-cases, with & without Khash"""
    maxDiff = None

    merchant_id = None
    api_key = None
    api_url = None

    def setUp(self):
        self.session_id = generate_unique_id()[:32]
        self.email_client = EMAIL

    def test_not_khashed(self):
        """test without khashed card"""
        # required khashed=False
        payment = CardPayment(PTOK, False)
        self.inq = user_inquiry(
            self.session_id, self.merchant_id, self.email_client,
            payment=payment)
        self.assertNotIn('PENC', self.inq.params)
        self.compare(expected)

    def test_khashed(self):
        """test with khashed card"""
        # not required default khashed=True
        payment = CardPayment(PTOK)
        self.inq = user_inquiry(
            self.session_id, self.merchant_id, self.email_client,
            payment=payment)
        self.assertIn('PENC', self.inq.params)
        self.assertEqual('KHASH', self.inq.params['PENC'])
        expected_khashed = expected.copy()
        expected_khashed['PENC'] = 'KHASH'
        expected_khashed['PTOK'] = '411111WMS5YA6FUZA1KC'
        self.compare(expected_khashed)

    def compare(self, expected_dict):
        """common method for both tests"""
        res = Client(self.api_url, self.api_key).process(self.inq)
        self.assertIsNotNone(res)
        self.assertNotIn('ERRO', res.params)
        actual = self.inq.params.copy()
        remove = ['SDK_VERSION', 'SESS', 'UNIQ', 'ORDR']
        for k in remove:
            if k in actual:
                del actual[k]
        self.assertEqual(expected_dict, actual)


if __name__ == "__main__":
    unittest.main(verbosity=2)
