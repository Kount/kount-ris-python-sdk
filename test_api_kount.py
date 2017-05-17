#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://bitbucket.org/panatonkount/sdkpython
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
import logging
import unittest
import os
import requests

from json_test import example_data_products
from local_settings import kount_api_key, url_api, timeout
from settings import resource_folder, xml_filename
from ris_validator import RisValidator
from client import Client
from util.xmlparser import xml_to_dict
from simplejson.scanner import JSONDecodeError


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


XML_FILE = os.path.join(os.path.dirname(__file__),
                        resource_folder, xml_filename)

LOGGER = logging.getLogger('kount')

def dict_compare(dict1, dict2):
    "compare 2 dictionaries"
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


class TestAPIRIS(unittest.TestCase):
    "implemented curl from https://kopana.atlassian.net/wiki/display/KS/Testing"
    def setUp(self):
        "for testing - self.maxDiff = None"
        self.maxDiff = None
        self.kount_api_key = kount_api_key
        self.url = url_api
        self.data = None
        self.headers_api = {'X-Kount-Api-Key': self.kount_api_key}

    def test_api_kount(self):
        "expected modified 'TRAN'"
        self.data = CURLED
        actual = Client(url=url_api, key=kount_api_key).process(
            params=self.data)
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
            "COOKIES": None, "HTTP_COUNTRY": None, "LANGUAGE":  None,
            "MOBILE_DEVICE": None, "MOBILE_TYPE": None,
            "MOBILE_FORWARDER": None,
            "VOICE_DEVICE": None, "PC_REMOTE": None, "RULES_TRIGGERED":1,
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
        added, removed, modified, _ = dict_compare(actual, expected)
        self.assertEqual(added, set())
        self.assertEqual(removed, set())
        self.assertEqual(modified.keys(),
                         {'CARDS': ('196', '1'),
                          'GEOX': ('CN', 'US'),
                          'RULE_ID_0': ('6822', '1024842'),
                          'REGN': ('CN_02', None),
                          'TRAN': ('P04S03M57HSP', 'PTPN0Z04P8Y6'),
                          'SCOR': ('99', '29'), 'NETW': ('A', 'N'),
                          'EMAILS': ('20', '1')}.keys())
        #~ self.assertEqual(Client.process(), expected)

    def test_api_kount_2_items(self):
        "expected modified 'TRAN'"
        self.data = example_data_products
        expected = {
            'BROWSER': None, 'IP_LON': None, 'DEVICES': '1', 'SITE': 'DEFAULT',
            'VERS': '0695', 'SESS': 'F8E874A38B7B4B6DBB71492A584A969D',
            'JAVASCRIPT': None, 'LOCALTIME': ' ', 'REGN': 'CA_NS',
            'DDFS': None, 'FLASH': None, 'FINGERPRINT': None, 'MERC': '999666',
            'REGION': None, 'BRND': None, 'TIMEZONE': None, 'PIP_COUNTRY': None,
            'MOBILE_DEVICE': None, 'PIP_LAT': None, 'EMAILS': '1',
            'IP_LAT': None, 'IP_CITY': None, 'ORDR': 'F8E874A38B7B',
            'COOKIES': None, 'AUTO': 'R', 'MOBILE_TYPE': None,
            'IP_REGION': None,
            'COUNTERS_TRIGGERED': 0, 'PIP_REGION': None, 'PROXY': None,
            'IP_ORG': None, 'WARNING_COUNT': 0, 'NETW': 'N',
            'PIP_ORG': None,
            'PC_REMOTE': None, 'REASON_CODE': None, 'PIP_CITY': None,
            'VOICE_DEVICE': None, 'UAS': None, 'KAPT': 'N', 'MODE': 'Q',
            'MOBILE_FORWARDER': None, 'DSR': None, 'HTTP_COUNTRY': None,
            'IP_COUNTRY': None, 'SCOR': '34', 'LANGUAGE': None, 'PIP_LON': None,
            'COUNTRY': None, 'GEOX': 'CA', 'RULES_TRIGGERED': 1, 'OS': None,
            'CARDS': '1', 'DEVICE_LAYERS': '....',
            'IP_IPAD': None,
            'RULE_DESCRIPTION_0': 'Review if order total > $1000 USD',
            'PIP_IPAD': None}
        actual = Client(url=url_api, key=kount_api_key).process(
            params=self.data)
        del actual['TRAN']
        del actual['RULE_ID_0']
        del actual['VELO']
        del actual['VMAX']
        self.assertEqual(actual, expected)

    def test_last_2_items_bad_email(self):
        "last_2_items_bad_email"
        self.data = example_data_products.copy()
        bad = CURLED['EMAL'].replace('@', "%40")
        self.data["EMAL"] = bad
        expected = {
            'ERROR_0':
            "321 BAD_EMAL Cause: [[%s is an invalid email address],"
            " Field: [EMAL], Value: [%s]" % (bad, bad),
            'ERRO': 321, 'ERROR_COUNT': 1,
            'WARNING_COUNT': 0, 'MODE': 'E'}
        actual = Client(url=url_api, key=kount_api_key).process(
            params=self.data)
        self.assertEqual(actual, expected)

    def test_2_items_bad_s2em(self):
        "bad S2EM"
        bad = example_data_products["S2EM"].replace('@', "%40")
        example_data_products["S2EM"] = bad
        self.data = example_data_products
        expected = {
            'AUTO': 'R',
            'BRND': None,
            'BROWSER': None,
            'CARDS': '1',
            'COOKIES': None,
            'COUNTERS_TRIGGERED': 0,
            'COUNTRY': None,
            'DDFS': None,
            'DEVICES': '1',
            'DEVICE_LAYERS': '....',
            'DSR': None,
            'EMAILS': '1',
            'FINGERPRINT': None,
            'FLASH': None,
            'GEOX': 'CA',
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
            'MERC': '999666',
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
            'REGN': 'CA_NS',
            'RULES_TRIGGERED': 1,
            'RULE_DESCRIPTION_0': 'Review if order total > $1000 USD',
            'SCOR': '34',
            'SESS': 'F8E874A38B7B4B6DBB71492A584A969D',
            'SITE': 'DEFAULT',
            'TIMEZONE': None,
            'UAS': None,
            'VERS': '0695',
            'VOICE_DEVICE': None,
            'WARNING_COUNT': 0}
        actual = Client(url=url_api, key=kount_api_key).process(
            params=self.data)
        del actual['TRAN']
        del actual['RULE_ID_0']
        del actual['VELO']
        del actual['VMAX']
        self.assertEqual(actual, expected)

    def test_two_items_none_email(self):
        "email = None"
        example_data_products["EMAL"] = None
        self.data = example_data_products
        expected = {
            'ERRO': 221, 'ERROR_COUNT': 1,
            'MODE': 'E', 'WARNING_COUNT': 0,
            'ERROR_0': "221 MISSING_EMAL Cause: "
                       "[Non-empty value was required in this case], "
                       "Field: [EMAL], Value: []",}
        actual = Client(url=url_api, key=kount_api_key).process(
            params=self.data)
        self.assertEqual(actual, expected)

    def test_two_items_missing_email(self):
        "missing email"
        del example_data_products["EMAL"]
        self.data = example_data_products
        expected = {
            'ERRO': 221, 'ERROR_COUNT': 1,
            'MODE': 'E', 'WARNING_COUNT': 0,
            'ERROR_0': "221 MISSING_EMAL Cause: "
                       "[Non-empty value was required in this case], "
                       "Field: [EMAL], Value: []",}
        actual = Client(url=url_api, key=kount_api_key).process(
            params=self.data)
        self.assertEqual(actual, expected)

    def test_api_kount_empty_data(self):
        "empty data"
        self.data = {}
        self.data = {'FRMT': 'JSON'}
        expected = {"MODE": "E", "ERRO": "201"}
        actual = Client(url=url_api, key=kount_api_key).process(
            params=self.data)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(
        #~ defaultTest = "TestAPIRIS.test_api_kount_empty_data"
        #~ defaultTest = "TestAPIRIS.test_two_items_missing_email"
        )
