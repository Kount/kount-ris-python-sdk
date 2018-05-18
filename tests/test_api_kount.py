#!/usr/bin/env python
"""Test class TestAPIRIS"""
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
import logging
import unittest

import pytest

from kount.client import Client
from kount.ris_validator import RisValidationException
from kount.version import VERSION

from .json_test import example_data_products

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"

LOGGER = logging.getLogger('kount')

expected1 = {
    'AUTO': 'R',
    'BRND': None,
    'BROWSER': None,
    'CARDS': '5',
    'COOKIES': None,
    'COUNTERS_TRIGGERED': 0,
    'COUNTRY': None,
    'DDFS': None,
    'DEVICES': '1',
    'DEVICE_LAYERS': '....',
    'DSR': None,
    'EMAILS': '21',
    'FINGERPRINT': None,
    'FLASH': None,
    'GEOX': 'US',
    'HTTP_COUNTRY': None,
    'IP_CITY': None,
    'IP_COUNTRY': None,
    'IP_IPAD': None,
    'IP_LAT': None,
    'IP_LON': None,
    'IP_ORG': None,
    'IP_REGION': None,
    'JAVASCRIPT': None,
    'KAPT': 'N',
    'LANGUAGE': None,
    'LOCALTIME': ' ',
    'MERC': '',  # will be replaced
    'MOBILE_DEVICE': None,
    'MOBILE_FORWARDER': None,
    'MOBILE_TYPE': None,
    'MODE': 'Q',
    'NETW': 'N',
    'ORDR': 'F8E874A38B7B',
    'OS': None,
    'PC_REMOTE': None,
    'PIP_CITY': None,
    'PIP_COUNTRY': None,
    'PIP_IPAD': None,
    'PIP_LAT': None,
    'PIP_LON': None,
    'PIP_ORG': None,
    'PIP_REGION': None,
    'PROXY': None,
    'REASON_CODE': None,
    'REGION': None,
    'REGN': None,
    'RULES_TRIGGERED': 1,
    'RULE_DESCRIPTION_0': 'Review if order total > $1000 USD',
    'SCOR': '99',
    'SESS': 'F8E874A38B7B4B6DBB71492A584A969D',
    'SITE': 'DEFAULT',
    'TIMEZONE': None,
    'UAS': None,
    'VERS': '0695',
    'VOICE_DEVICE': None,
    'WARNING_COUNT': 0}


def dict_compare(dict1, dict2):
    """compare 2 dictionaries"""
    dict1_keys = set(dict1.keys())
    dict2_keys = set(dict2.keys())
    intersect_keys = dict1_keys.intersection(dict2_keys)
    added = dict1_keys - dict2_keys
    removed = dict2_keys - dict1_keys
    modified = {o: (dict1[o],
                    dict2[o]) for o in intersect_keys if dict1[o] != dict2[o]}
    same = set(o for o in intersect_keys if dict1[o] == dict2[o])
    return added, removed, modified, same


CURLED = {
    'ANID': '',
    'AUTH': 'A',
    'AVST': 'M',
    'AVSZ': 'M',
    'B2A1': '1234 North B2A1 Tree Lane South',
    'B2CC': 'US',
    'B2CI': 'Albuquerque',
    'B2PC': '87101',
    'B2PN': '555+867-5309',
    'B2ST': 'NM',
    'CASH': '4444',
    'CURR': 'USD',
    'CVVR': 'M',
    'EMAL': 'curly.riscaller15@kountqa.com',
    'FRMT': 'JSON',
    'IPAD': '4.127.51.215',
    'LAST4': '2514',
    'MACK': 'Y',
    'MERC': '999666',
    'MODE': 'Q',
    'NAME': 'Goofy Grumpus',
    'ORDR': '088E9F496135',
    'PROD_DESC[]': '3000 CANDLEPOWER PLASMA FLASHLIGHT',
    'PROD_ITEM[]': 'SG999999',
    'PROD_PRICE[]': '68990',
    'PROD_QUANT[]': '2',
    'PROD_TYPE[]': 'SPORTING_GOODS',
    'PTOK': '0007380568572514',
    'PTYP': 'CARD',
    'S2A1': '567 West S2A1 Court North',
    'S2CC': 'US',
    'S2CI': 'Gnome',
    'S2EM': 'sdkTestShipTo@kountsdktestdomain.com',
    'S2NM': 'SdkTestShipToFirst SdkShipToLast',
    'S2PC': '99762',
    'S2PN': '208 777-1212',
    'S2ST': 'AK',
    'SESS': '088E9F4961354D4F90041988B8D5C66B',
    'SITE': 'DEFAULT',
    'TOTL': '123456',
    'UNIQ': '088E9F4961354D4F9004',
    'VERS': '0695'}


@pytest.mark.usefixtures("api_url", "api_key", "merchant_id")
class TestAPIRIS(unittest.TestCase):
    """
    implemented curl from https://kopana.atlassian.net/wiki/display/KS/Testing
    """
    maxDiff = None

    api_url = None
    api_key = None
    merchant_id = None
    timeout = 5

    def _expected_response(self):
        r = dict(expected1)
        r['MERC'] = self.merchant_id
        return r

    def test_api_kount(self):
        """expected modified 'TRAN'"""
        data = CURLED
        self.assertIn('MODE', CURLED)
        expected = {
            "VERS": "0695", "MODE": "Q", "TRAN": "PTPN0Z04P8Y6",
            "MERC": "999666", "SESS": "088E9F4961354D4F90041988B8D5C66B",
            "ORDR": "088E9F496135", "AUTO": "R", "SCOR": "29", "GEOX": "US",
            "BRND": None, "REGN": None, "NETW": "N", "KAPT": "N", "CARDS": "1",
            "DEVICES": "1", "EMAILS": "1", "VELO": "0",
            "VMAX": "0", "SITE": "DEFAULT", "DEVICE_LAYERS": "....",
            "FINGERPRINT": None, "TIMEZONE": None, "LOCALTIME": " ",
            "REGION": None,
            "COUNTRY": None, "PROXY": None, "JAVASCRIPT": None, "FLASH": None,
            "COOKIES": None, "HTTP_COUNTRY": None, "LANGUAGE": None,
            "MOBILE_DEVICE": None, "MOBILE_TYPE": None,
            "MOBILE_FORWARDER": None,
            "VOICE_DEVICE": None, "PC_REMOTE": None, "RULES_TRIGGERED": 1,
            "RULE_ID_0": "1024842",
            "RULE_DESCRIPTION_0": "Review if order total > $1000 USD",
            "COUNTERS_TRIGGERED": 0,
            "REASON_CODE": None, "DDFS": None, "DSR": None,
            "UAS": None, "BROWSER": None,
            "OS": None, "PIP_IPAD": None, "PIP_LAT": None, "PIP_LON": None,
            "PIP_COUNTRY": None,
            "PIP_REGION": None, "PIP_CITY": None, "PIP_ORG": None,
            "IP_IPAD": None,
            "IP_LAT": None, "IP_LON": None, "IP_COUNTRY": None,
            "IP_REGION": None,
            "IP_CITY": None, "IP_ORG": None, "WARNING_COUNT": 0}
        for raise_errors in [True, False]:
            actual = self._client(raise_errors=raise_errors)._execute(data)
            added, removed, modified, _ = dict_compare(actual, expected)
            self.assertEqual(added, set())
            self.assertEqual(removed, set())
            modified_exp = {'CARDS': ('196', '1'),
                            'RULE_ID_0': ('6822', '1024842'),
                            'TRAN': ('P04S03M57HSP', 'PTPN0Z04P8Y6'),
                            'SCOR': ('99', '29'),
                            'EMAILS': ('20', '1')}
            self.assertEqual(sorted(modified), sorted(modified_exp))

    def test_api_kount_2_items(self):
        "expected modified 'TRAN'"
        data = example_data_products.copy()
        self.assertIn('MODE', data)
        for raise_errors in [True, False]:
            actual = self._client(raise_errors=raise_errors)._execute(data)
            del (actual['TRAN'], actual['RULE_ID_0'],
                 actual['VELO'], actual['VMAX'])
            self.assertEqual(actual, self._expected_response())

    def test_last_2_items_bad_email(self):
        "last_2_items_bad_email"
        data = example_data_products.copy()
        self.assertIn('MODE', CURLED)
        bad = CURLED['EMAL'].replace('@', "%40")
        data["EMAL"] = bad
        self.assertRaises(
            RisValidationException,
            lambda: self._client(raise_errors=True)._execute(data)
        )
        expected = {
            'ERROR_0':
                "321 BAD_EMAL Cause: [[%s is an invalid email address],"
                " Field: [EMAL], Value: [%s]" % (bad, bad),
            'ERRO': 321,
            'ERROR_COUNT': 1,
            'WARNING_COUNT': 0,
            'MODE': 'E'}
        actual = self._client(raise_errors=False)._execute(data)
        self.assertEqual(actual, expected)

    def test_2_items_bad_s2em(self):
        """bad S2EM"""
        bad = example_data_products["S2EM"].replace('@', "%40")
        data = example_data_products.copy()
        data["S2EM"] = bad
        self.assertRaises(
            RisValidationException,
            lambda: self._client(raise_errors=True)._execute(data)
        )
        actual = self._client(raise_errors=False)._execute(params=data)
        del (actual['TRAN'], actual['RULE_ID_0'],
             actual['VELO'], actual['VMAX'])
        self.assertEqual(actual, self._expected_response())

    def test_two_items_none_email(self):
        "email = None"
        data = example_data_products.copy()
        data["EMAL"] = None
        self.assertIn('MODE', data)
        expected = {
            'ERRO': 221, 'ERROR_COUNT': 1,
            'MODE': 'E', 'WARNING_COUNT': 0,
            'ERROR_0': "221 MISSING_EMAL Cause: "
                       "[Non-empty value was required in this case], "
                       "Field: [EMAL], Value: []"}
        for raise_errors in [True, False]:
            actual = self._client(raise_errors=raise_errors)._execute(data)
            self.assertEqual(actual, expected)

    def test_two_items_missing_or_long_email(self):
        "missing or long incorrect email"
        data = example_data_products.copy()
        del data["EMAL"]
        self.assertIn('MODE', data)
        expected = {
            'ERRO': 221, 'ERROR_COUNT': 1,
            'MODE': 'E', 'WARNING_COUNT': 0,
            'ERROR_0': "221 MISSING_EMAL Cause: "
                       "[Non-empty value was required in this case], "
                       "Field: [EMAL], Value: []"}
        for raise_errors in [True, False]:
            actual = self._client(raise_errors=raise_errors)._execute(data)
            self.assertEqual(actual, expected)
        data["EMAL"] = "a" * 57 + "@aaa.com"
        with self.assertRaises(RisValidationException):
            self._client(raise_errors=True)._execute(data)
        response = self._client(raise_errors=False)._execute(data)
        self.assertEqual(321, response['ERRO'])

    def test_api_kount_empty_data(self):
        "empty data"
        data = {'FRMT': 'JSON'}
        expected = {"MODE": "E", "ERRO": "201"}
        with self.assertRaises(RisValidationException):
            self.assertTrue(self._client(raise_errors=True)._execute(data))
        actual = self._client(raise_errors=False)._execute(data)
        self.assertEqual(actual, expected)

    def _client(self, **kwargs):
        kwargs['api_url'] = self.api_url
        kwargs['api_key'] = self.api_key
        kwargs['timeout'] = self.timeout
        return Client(**kwargs)

