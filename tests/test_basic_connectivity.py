#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/
# Copyright (C) 2025 Kount an Equifax Company All Rights Reserved.
"""Test Cases from sdk documentation
generate_unique_id
default_inquiry
Test Basic Connectivity
"""
import unittest
import pytest

from kount.client import Client
from kount.util.payment import CardPayment
from kount.version import VERSION

from .test_inquiry import generate_unique_id, default_inquiry

from kount.config import SDKConfig

__author__ = SDKConfig.SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDKConfig.SDK_MAINTAINER
__email__ = SDKConfig.MAINTAINER_EMAIL
__status__ = SDKConfig.STATUS


PTOK = "0007380568572514"
EMAIL = 'predictive@kount.com'


@pytest.mark.usefixtures("api_url", "api_key", "merchant_id")
class TestBasicConnectivity(unittest.TestCase):
    """Test Basic Connectivity"""
    maxDiff = None

    def _client(self, **kwargs):
        kwargs['api_url'] = self.api_url
        kwargs['api_key'] = self.api_key
        return Client(**kwargs)

    def _process(self, request, **client_kwargs):
        return self._client(**client_kwargs).process(request)

    def setUp(self):
        self.session_id = generate_unique_id()[:32]
        self.email_client = EMAIL
        payment = CardPayment(PTOK, khashed=False)
        self.inq = default_inquiry(self.merchant_id,
                                   self.session_id,
                                   self.email_client,
                                   payment=payment)

    def test_12_expected_score(self):
        "test_12_expected_score"
        self.inq.params["UDF[~K!_SCOR]"] = '42'
        res = self._process(self.inq)
        self.assertIsNotNone(res)
        self.assertEqual('42', res.get_score())

    def request_with_Lbin(self):
        "test_Lbin_set_in_requst"
        self.inq.params["LBIN"] = '1234567'
        self.assertEqual('1234567', self.inq.params.get("LBIN"))
        res = self._process(self.inq)
        self.assertEqual(0, len(res.get_errors))

    def request_without_Lbin(self):
        "test_Lbin_not_set_in_requst"
        res = self._process(self.inq)
        self.assertEqual(0, len(res.get_errors))

    def test_13_expected_decision(self):
        """test_13_expected_decision"""
        self.inq.params["UDF[~K!_AUTO]"] = 'R'
        res = self._process(self.inq)
        self.assertIsNotNone(res)
        self.assertEqual("R", res.get_auto())

    def test_16_expected_geox(self):
        """test_16_expected_geox"""
        self.inq.params["UDF[~K!_SCOR]"] = '42'
        self.inq.params["UDF[~K!_AUTO]"] = 'D'
        self.inq.params["UDF[~K!_GEOX]"] = 'NG'
        res = self._process(self.inq)
        self.assertIsNotNone(res)
        self.assertEqual("D", res.get_auto())
        self.assertEqual("NG", res.get_geox())
        self.assertEqual("42", res.get_score())

    def test_cyrillic(self):
        """test_cyrillic"""
        bad = u'Сирма :ы№'
        self.inq.params["S2NM"] = bad
        self.inq.params["EMAL"] = bad
        res = self._process(self.inq, raise_errors=False)
        self.assertIsNotNone(res)
        self.assertEqual({
            u'ERRO': 321,
            u'ERROR_0': u"321 BAD_EMAL Cause: [Invalid email address]"\
                 ", Field: [EMAL], Value: [%s]" % (bad),
            u'ERROR_COUNT': 1, u'MODE': u'E', u'WARNING_COUNT': 0},
            {u'ERRO':res.get_error_code(),
            u'ERROR_0': res.get_errors()[0],
            u'ERROR_COUNT': len(res.get_errors()),
            u'MODE': res.get_mode(),
            u'WARNING_COUNT': len(res.get_warnings())})

    def test_long(self):
        """test_long request"""
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
            inq.params["S2NM"] = bad
            try:
                self._process(inq, raise_errors=False)
            except ValueError as vale:
                self.assertEqual(expected, str(vale))


class TestBasicConnectivityKhashed(TestBasicConnectivity):
    """Test Basic Connectivity Khashed"""
    maxDiff = None

    def setUp(self):
        self.session_id = generate_unique_id()[:32]
        self.email_client = EMAIL
        payment = CardPayment(PTOK)
        self.inq = default_inquiry(
            self.merchant_id, self.session_id,
            self.email_client, payment=payment)


if __name__ == "__main__":
    unittest.main(
        # defaultTest="TestBasicConnectivity.test_16_expected_geox"
    )
