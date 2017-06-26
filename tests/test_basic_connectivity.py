#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""Test Cases from sdk documentation
generate_unique_id
default_inquiry
Test Basic Connectivity
"""
from __future__ import absolute_import, unicode_literals, division, print_function
import unittest
from kount.response import Response
from kount.ris_validator import RisValidationException
from kount.client import Client
from kount.settings import RAISE_ERRORS
from kount.util.payment import Payment, CardPayment
import inittest
from test_inquiry import generate_unique_id, default_inquiry

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


URL_API = "https://risk.beta.kount.net"
URL_API_BETA = URL_API
MERCHANT_ID6 = '999666'
MERCHANT_ID7 = '999667'
PTOK = "0007380568572514"
EMAIL = 'predictive@kount.com'
KOUNT_API_KEY6 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5OTk2NjYiLCJhdWQiOiJLb3VudC4xIiwiaWF0IjoxNDk0NTM0Nzk5LCJzY3AiOnsia2EiOm51bGwsImtjIjpudWxsLCJhcGkiOmZhbHNlLCJyaXMiOnRydWV9fQ.eMmumYFpIF-d1up_mfxA5_VXBI41NSrNVe9CyhBUGck"
KOUNT_API_KEY7 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5OTk2NjciLCJhdWQiOiJLb3VudC4xIiwiaWF0IjoxNDk0NTM1OTE2LCJzY3AiOnsia2EiOm51bGwsImtjIjpudWxsLCJhcGkiOmZhbHNlLCJyaXMiOnRydWV9fQ.KK3zG4dMIhTIaE5SeCbej1OAFhZifyBswMPyYFAVRrM"


class TestBasicConnectivity(unittest.TestCase):
    "Test Basic Connectivity"
    maxDiff = None

    def setUp(self):
        self.session_id = generate_unique_id()[:32]
        self.email_client = EMAIL
        payment = CardPayment(PTOK, khashed=False)
        #~ payment = Payment(payment_type="CARD", payment_token=PTOK,
                          #~ khashed=False)
        self.inq = default_inquiry(
            self.session_id, MERCHANT_ID7, self.email_client,
            ptok=PTOK, payment=payment, khashed=False)

    def test_12_expected_score(self):
        "test_12_expected_score"
        self.inq.params["UDF[~K!_SCOR]"] = '42'
        res = Client(URL_API_BETA, KOUNT_API_KEY7,
                     raise_errors=RAISE_ERRORS).process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual("42", rr.params['SCOR'])

    def test_13_expected_decision(self):
        "test_13_expected_decision"
        self.inq.params["UDF[~K!_AUTO]"] = 'R'
        res = Client(URL_API, KOUNT_API_KEY7, raise_errors=RAISE_ERRORS).process(
            params=self.inq.params)
        self.assertIsNotNone(res)
        self.assertEqual("R", res["AUTO"])

    def test_16_expected_geox(self):
        "test_16_expected_geox"
        self.inq.params["UDF[~K!_SCOR]"] = '42'
        self.inq.params["UDF[~K!_AUTO]"] = 'D'
        self.inq.params["UDF[~K!_GEOX]"] = 'NG'
        res = Client(URL_API, KOUNT_API_KEY7,
                     raise_errors=RAISE_ERRORS).process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual("D", res["AUTO"])
        self.assertEqual("NG", res["GEOX"])
        self.assertEqual("42", rr.params['SCOR'])

    def test_cyrillic(self):
        "test_cyrillic"
        bad = u'Сирма :ы№'
        self.inq.params["S2NM"] = bad
        self.inq.params["EMAL"] = bad
        self.assertRaises(
            RisValidationException,
            Client(URL_API, KOUNT_API_KEY7,
                   raise_errors=True).process, self.inq.params)
        res = Client(URL_API, KOUNT_API_KEY7,
                     raise_errors=False).process(params=self.inq.params)
        self.assertIsNotNone(res)
        actual = u"321 BAD_EMAL Cause: [[%s is an invalid email address]"\
                 ", Field: [EMAL], Value: [%s]" % (bad, bad)
        self.assertEqual({
            u'ERRO': 321,
            u'ERROR_0': actual,
            u'ERROR_COUNT': 1, u'MODE': u'E', u'WARNING_COUNT': 0}, res)

    def test_long(self):
        "test_long request"
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
        inq = self.inq
        for bad in bad_list:
            inq.params["S2NM"] = bad * 999
            self.assertRaises(
                RisValidationException,
                Client(URL_API,
                       KOUNT_API_KEY6,
                       raise_errors=True).process, inq.params)
            try:
                Client(
                    URL_API, KOUNT_API_KEY6,
                    raise_errors=False).process(params=inq.params)
            except ValueError as vale:
                self.assertEqual(expected, str(vale))

class TestBasicConnectivityKhashed(TestBasicConnectivity):
    "Test Basic Connectivity Khashed"
    maxDiff = None

    def setUp(self):
        self.session_id = generate_unique_id()[:32]
        self.email_client = EMAIL
        payment = CardPayment(PTOK, khashed=True)
        self.inq = default_inquiry(
            self.session_id, MERCHANT_ID7, self.email_client,
            ptok=PTOK, payment=payment, khashed=True)


if __name__ == "__main__":
    unittest.main(
        #~ defaultTest="TestBasicConnectivity.test_16_expected_geox"
                  )
