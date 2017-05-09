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
from request import ASTAT, BCRSTAT, CURRENCYTYPE #, MERCHANTACKNOWLEDGMENT, REFUNDCBSTAT, SHIPPINGTYPESTAT, INQUIRYMODE
from inquiry import Inquiry
from pprint import pprint
import uuid
from util.payment import CardPayment
from util.cartitem import CartItem
from util.address import Address


class Utilities(unittest.TestCase):
    RIS_ENDPOINT = "https://risk.test.kount.net"
    MERCHANT_ID = 999666
    BILLING_ADDRESS = Address("1234 North B2A1 Tree Lane South", None, "Albuquerque", "NM", "87101", "US")
    SHIPPING_ADDRESS = Address("567 West S2A1 Court North", None, "Gnome", "AK", "99762", "US")

    @staticmethod
    def default_inquiry(session_id):
        result = Inquiry()
        #~ inquiry_mode = INQUIRYMODE.DEFAULT
        result.shipping_address(Utilities.SHIPPING_ADDRESS)
        result.shipping_name("SdkShipToFN SdkShipToLN")
        result.billing_address(Utilities.BILLING_ADDRESS)
        unique_id = session_id[:21]  
        result.currency_set(CURRENCYTYPE.USD)
        result.total_set(123456)
        result.cash(4444)
        result.billing_phone_number("555-867-5309")
        result.shipping_phone_number("555-777-1212")
        result.email_client("sdkTest@kountsdktestdomain.com")
        result.customer_name("SdkTestFirstName SdkTestLastName")
        result.unique_customer_id(unique_id)
        result.website("DEFAULT")
        result.email_shipping("sdkTestShipToEmail@kountsdktestdomain.com")
        result.ip_address("131.206.45.21")
        cart_item = []
        cart_item.append(CartItem("SPORTING_GOODS", "SG999999", "3000 CANDLEPOWER PLASMA FLASHLIGHT", 2, 68990))
        result.shopping_cart(cart_item)
        result.version("1.0.0")
        result.merchant_set(Utilities.MERCHANT_ID)
        payment = CardPayment("0007380568572514")
        result.payment_set(payment)
        result.session_set(session_id)
        order_id = session_id[:11]
        result.order_number(order_id)
        result.merchant_acknowledgment_set("YES")
        result.authorization_status(ASTAT.Approve)
        result.avs_zip_reply(BCRSTAT.MATCH)
        result.avs_address_reply(BCRSTAT.MATCH)
        result.avs_cvv_reply(BCRSTAT.MATCH)
        return result


class TestInquiry(unittest.TestCase):
    def setUp(self):
        self.params = {}
        self.result = Utilities.default_inquiry(session_id = str(uuid.uuid4()))

    def test_utilities(self):
        #~ session_id = str(uuid.uuid4())
        result = self.result
        #~ print(112221, result.params)
        #~ self.maxDiff = None
        expected = {'AUTH': 'A',
            'AVST': 'M',
            'AVSZ': 'M',
            'B2A1': '1234 North B2A1 Tree Lane South',
            'B2A2': None,
            'B2CC': 'US',
            'B2CI': 'Albuquerque',
            'B2PC': '87101',
            'B2PN': '555-867-5309',
            'B2ST': 'NM',
            'BPREMISE': '',
            'BSTREET': '',
            'CURR': 'USD',
            'CVVR': 'M',
            'EMAL': 'sdkTest@kountsdktestdomain.com',
            'IPAD': '131.206.45.21',
            'LAST4': '2514',
            'MACK': 'Y',
            'MERC': 999666,
            'NAME': 'SdkTestFirstName SdkTestLastName',
            'PENC': '',
            'PROD_DESC[0]': '3000 CANDLEPOWER PLASMA FLASHLIGHT',
            'PROD_ITEM[0]': 'SG999999',
            'PROD_PRICE[0]': 68990,
            'PROD_QUANT[0]': 2,
            'PROD_TYPE[0]': 'SPORTING_GOODS',
            'PTOK': '0007380568572514',
            'PTYP': 'CARD',
            'S2A1': '567 West S2A1 Court North',
            'S2A2': None,
            'S2CC': 'US',
            'S2CI': 'Gnome',
            'S2EM': 'sdkTestShipToEmail@kountsdktestdomain.com',
            'S2NM': 'SdkShipToFN SdkShipToLN',
            'S2PC': '99762',
            'S2PN': '555-777-1212',
            'S2ST': 'AK',
            'SDK': 'Python 3.6',
            'SDK_VERSION': 'Sdk-Ris-Python-1.0.0',
            'SITE': 'DEFAULT',
            'SPREMISE': '',
            'SSTREET': '',
            'TOTL': 123456,
            'VERS': '1.0.0'}
        actual = result.params
        del(actual['UNIQ'])
        del(actual['SESS'])
        del(actual['ORDR'])
        self.assertEqual(result.params, expected)


if __name__ == "__main__":
    unittest.main()
