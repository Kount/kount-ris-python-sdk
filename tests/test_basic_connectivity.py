#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""Test Cases from sdk documentation
generate_unique_id
default_inquiry
Test Basic Connectivity
"""
from __future__ import (
    absolute_import, unicode_literals, division, print_function)
import unittest
import uuid
from kount.response import Response
from kount.settings import RAISE_ERRORS
from kount.request import (ASTAT, BCRSTAT, INQUIRYMODE,
                           CURRENCYTYPE, MERCHANTACKNOWLEDGMENT)
from kount.inquiry import Inquiry
from kount.util.payment import CardPayment
from kount.util.cartitem import CartItem
from kount.util.address import Address
from kount.util.ris_validation_exception import RisValidationException
from kount.client import Client
from kount.util.xml_dict import XML_DICT, REQUIRED, NOTREQUIRED
from kount.settings import SDK_VERSION

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


BILLING_ADDRESS = Address("1234 North B2A1 Tree Lane South",
                          "", "Albuquerque", "NM", "87101", "US")
SHIPPING_ADDRESS = Address("567 West S2A1 Court North", "",
                           "Gnome", "AK", "99762", "US")
URL_API = "https://risk.beta.kount.net"
URL_API_BETA = URL_API
MERCHANT_ID = '999666'
MERCHANT_ID_999667 = '999667'
PTOK = "0007380568572514"
KOUNT_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5OTk2NjYiLCJhdWQiOiJLb3VudC4xIiwiaWF0IjoxNDk0NTM0Nzk5LCJzY3AiOnsia2EiOm51bGwsImtjIjpudWxsLCJhcGkiOmZhbHNlLCJyaXMiOnRydWV9fQ.eMmumYFpIF-d1up_mfxA5_VXBI41NSrNVe9CyhBUGck"
KOUNT_API_KEY999667 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5OTk2NjciLCJhdWQiOiJLb3VudC4xIiwiaWF0IjoxNDk0NTM1OTE2LCJzY3AiOnsia2EiOm51bGwsImtjIjpudWxsLCJhcGkiOmZhbHNlLCJyaXMiOnRydWV9fQ.KK3zG4dMIhTIaE5SeCbej1OAFhZifyBswMPyYFAVRrM"


def generate_unique_id():
    "unique session id"
    return str(uuid.uuid4()).replace('-', '').upper()


def default_inquiry(session_id, merchant_id, email_client, ptok):
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
    result.merchant_set(merchant_id) # 999666
    payment = CardPayment(ptok)
    result.payment_set(payment) #PTOK
    result.session_set(session_id) #SESS
    result.order_number(session_id[:10])  #ORDR
    result.authorization_status(ASTAT.Approve) #AUTH
    result.avs_zip_reply(BCRSTAT.MATCH)
    result.avs_address_reply(BCRSTAT.MATCH)
    result.avs_cvv_reply(BCRSTAT.MATCH)
    result.merchant_acknowledgment_set(MERCHANTACKNOWLEDGMENT.TRUE) #"MACK"
    result.cash('4444')
    #~ result.params["PENC"] = "KHASH"
    return result


class TestBasicConnectivity(unittest.TestCase):
    "Test Basic Connectivity"
    def setUp(self):
        self.maxDiff = None
        self.session_id = generate_unique_id()[:32]
        email_client = 'predictive@kount.com'
        self.inq = default_inquiry(self.session_id,
                                   MERCHANT_ID_999667,
                                   email_client, ptok=PTOK)
        self.client = Client(URL_API_BETA, KOUNT_API_KEY999667)
        self.xml_2_dict = XML_DICT
        self.required = REQUIRED
        self.notrequired = NOTREQUIRED

    def test_12_expected_score(self):
        "test_12_expected_score"
        self.inq.params["UDF[~K!_SCOR]"] = '42'
        if RAISE_ERRORS:
            self.assertRaises(
                RisValidationException,
                Client(url=URL_API, key=KOUNT_API_KEY).process, self.inq.params)
        else:
            res = self.client.process(params=self.inq.params)
            self.assertIsNotNone(res)
            rr = Response(res)
            self.assertEqual("42", rr.params['SCOR'])

    def test_13_expected_decision(self):
        "test_13_expected_decision"
        self.inq.params["UDF[~K!_AUTO]"] = 'R'
        if RAISE_ERRORS:
            self.assertRaises(
                RisValidationException,
                Client(url=URL_API, key=KOUNT_API_KEY).process, self.inq.params)
        else:
            res = self.client.process(params=self.inq.params)
            self.assertIsNotNone(res)
            self.assertEqual("R", res["AUTO"])

    def test_16_expected_geox(self):
        "test_16_expected_geox"
        self.inq.params["UDF[~K!_SCOR]"] = '42'
        self.inq.params["UDF[~K!_AUTO]"] = 'D'
        self.inq.params["UDF[~K!_GEOX]"] = 'NG'
        if RAISE_ERRORS:
            self.assertRaises(
                RisValidationException,
                Client(url=URL_API, key=KOUNT_API_KEY).process, self.inq.params)
        else:
            res = self.client.process(params=self.inq.params)
            self.assertIsNotNone(res)
            rr = Response(res)
            self.assertEqual("D", res["AUTO"])
            self.assertEqual("NG", res["GEOX"])
            self.assertEqual("42", rr.params['SCOR'])

    def test_cyrillic(self):
        "test_cyrillic"
        self.maxDiff = None
        bad = u'Сирма :ы№'
        self.inq.params["S2NM"] = bad
        self.inq.params["EMAL"] = bad
        if RAISE_ERRORS:
            self.assertRaises(
                RisValidationException,
                Client(url=URL_API, key=KOUNT_API_KEY).process, self.inq.params)
        else:
            self.assertFalse(RAISE_ERRORS)
            res = self.client.process(params=self.inq.params)
            self.assertIsNotNone(res)
            actual = u"321 BAD_EMAL Cause: [[%s is an invalid email address]"\
                     ", Field: [EMAL], Value: [%s]" % (bad, bad)
            self.assertEqual({
                u'ERRO': 321,
                u'ERROR_0': actual,
                u'ERROR_COUNT': 1, u'MODE': u'E', u'WARNING_COUNT': 0}, res)

    def test_long(self):
        "test_long request"
        self.maxDiff = None
        bad_list = [
            'Сирма :ы№',
            'abcqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq 12345']
        expected = """Neither JSON nor String """\
            """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n"""\
            "<html><head>\n"\
            "<title>413 Request Entity Too Large</title>\n"\
            "</head><body>\n"\
            "<h1>Request Entity Too Large</h1>\n"\
            "The requested resource<br />/<br />\n"\
            "does not allow request data with POST requests, or the"\
            " amount of data provided in\n"\
            "the request exceeds the capacity limit.\n"\
            "</body></html>\n"\
            "MODE=E\n"\
            "ERRO=201"
        if RAISE_ERRORS:
            self.assertRaises(
                RisValidationException,
                Client(url=URL_API, key=KOUNT_API_KEY).process, self.inq.params)
        else:
            self.assertFalse(RAISE_ERRORS)
            for bad in bad_list:
                self.inq.params["S2NM"] = bad * 999
                try:
                    self.assertRaises(ValueError, self.client.process, self.inq.params)
                    self.client.process(params=self.inq.params)
                except ValueError as vale:
                    self.assertEqual(expected, vale.__str__())


if __name__ == "__main__":
    unittest.main(
        #~ defaultTest="TestBasicConnectivity.test_long"
        )
