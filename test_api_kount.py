#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import unittest
from pretty_print import pretty_print_POST
from json_test import example_data
from json_test import example_data_na
from local_settings import kountAPIkey
from local_settings import url_test
from local_settings import url_api
from pprint import pprint 


def dict_compare(d1, d2):
    #compare 2 dictionaries
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same


class TestAPIRIS(unittest.TestCase):
    #implemented curl from https://kopana.atlassian.net/wiki/display/KS/Testing
    def setUp(self):
        self.kountAPIkey = kountAPIkey
        self.url = url_test
        self.headers_api = {'X-Kount-Api-Key': self.kountAPIkey}
        self.url_API = url_api

    def test_api_kount(self):
        #~ expected modified 'TRAN'
        self.data = example_data
        self.expected = {"VERS":"0695","MODE":"Q","TRAN":"PHJJ03Z1TT95","MERC":"999666","SESS":"088E9F4961354D4F90041988B8D5C66B","ORDR":"088E9F496135","AUTO":"R","SCOR":"34","GEOX":"US","BRND":None,"REGN":None,"NETW":"N","KAPT":"N","CARDS":"1","DEVICES":"1","EMAILS":"1","VELO":"0","VMAX":"0","SITE":"DEFAULT","DEVICE_LAYERS":"....","FINGERPRINT":None,"TIMEZONE":None,"LOCALTIME":" ","REGION":None,"COUNTRY":None,"PROXY":None,"JAVASCRIPT":None,"FLASH":None,"COOKIES":None,"HTTP_COUNTRY":None,"LANGUAGE":None,"MOBILE_DEVICE":None,"MOBILE_TYPE":None,"MOBILE_FORWARDER":None,"VOICE_DEVICE":None,"PC_REMOTE":None,"RULES_TRIGGERED":1,"RULE_ID_0":"1024842","RULE_DESCRIPTION_0":"Review if order total > $1000 USD","COUNTERS_TRIGGERED":0,"REASON_CODE":None,"DDFS":None,"DSR":None,"UAS":None,"BROWSER":None,"OS":None,"PIP_IPAD":None,"PIP_LAT":None,"PIP_LON":None,"PIP_COUNTRY":None,"PIP_REGION":None,"PIP_CITY":None,"PIP_ORG":None,"IP_IPAD":None,"IP_LAT":None,"IP_LON":None,"IP_COUNTRY":None,"IP_REGION":None,"IP_CITY":None,"IP_ORG":None,"WARNING_COUNT":0}
        self.request_and_response()

    def test_api_kount_2_items(self):
        #~ expected modified 'TRAN'
        self.data = example_data_na
        self.expected = {'BROWSER': None, 'IP_LON': None, 'DEVICES': '1', 'SITE': 'DEFAULT', 'VERS': '0695', 'SESS': 'F8E874A38B7B4B6DBB71492A584A969D', 'VMAX': '0', 'JAVASCRIPT': None, 'LOCALTIME': ' ', 'REGN': 'CA_NS', 'DDFS': None, 'FLASH': None, 'FINGERPRINT': None, 'MERC': '999666', 'REGION': None, 'BRND': None, 'TIMEZONE': None, 'PIP_COUNTRY': None, 'MOBILE_DEVICE': None, 'PIP_LAT': None, 'EMAILS': '1', 'TRAN': 'PHH30BXK2GTG', 'IP_LAT': None, 'IP_CITY': None, 'ORDR': 'F8E874A38B7B', 'COOKIES': None, 'AUTO': 'R', 'MOBILE_TYPE': None, 'IP_REGION': None, 'COUNTERS_TRIGGERED': 0, 'PIP_REGION': None, 'PROXY': None, 'IP_ORG': None, 'WARNING_COUNT': 0, 'NETW': 'N', 'RULE_ID_0': '1024842', 'PIP_ORG': None, 'PC_REMOTE': None, 'REASON_CODE': None, 'PIP_CITY': None, 'VOICE_DEVICE': None, 'UAS': None, 'KAPT': 'N', 'MODE': 'Q', 'MOBILE_FORWARDER': None, 'DSR': None, 'HTTP_COUNTRY': None, 'IP_COUNTRY': None, 'SCOR': '34', 'LANGUAGE': None, 'PIP_LON': None, 'COUNTRY': None, 'GEOX': 'CA', 'RULES_TRIGGERED': 1, 'OS': None, 'CARDS': '1', 'DEVICE_LAYERS': '....', 'VELO': '0', 'IP_IPAD': None, 'RULE_DESCRIPTION_0': 'Review if order total > $1000 USD', 'PIP_IPAD': None}
        self.request_and_response()

    def test_api_kount_last_2_items_bad_email(self):
        example_data_na["EMAL"] = 'curly.riscaller12%40kountqa.com'
        self.data = example_data_na
        self.expected = {'ERROR_0': '321 BAD_EMAL Cause: [[curly.riscaller12%40kountqa.com is an invalid email address], Field: [EMAL], Value: [curly.riscaller12%40kountqa.com]', 'ERRO': 321, 'ERROR_COUNT': 1, 'WARNING_COUNT': 0, 'MODE': 'E'}
        self.request_and_response()

    def test_api_kount_2_items_bad_s2em(self):
        #~ S2EM': 'sdkTestShipTo%40kountsdktestdomain.com
        example_data_na["S2EM"] = 'sdkTestShipTo%40kountsdktestdomain.com'
        self.data = example_data_na
        self.expected = {'AUTO': 'R',
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
             'RULE_ID_0': '1024842',
             'SCOR': '34',
             'SESS': 'F8E874A38B7B4B6DBB71492A584A969D',
             'SITE': 'DEFAULT',
             'TIMEZONE': None,
             'TRAN': 'PH0N0TH8VQ81',
             'UAS': None,
             'VELO': '0',
             'VERS': '0695',
             'VMAX': '0',
             'VOICE_DEVICE': None,
             'WARNING_COUNT': 0}
        self.request_and_response()

    def test_api_kount_2_items_missing_email(self):
        example_data_na["EMAL"] = None
        self.data = example_data_na
        self.expected = {'WARNING_COUNT': 0, 'ERROR_COUNT': 1, 'MODE': 'E', 'ERROR_0': '401 EXTRA_DATA', 'ERRO': 401}
        self.request_and_response()

    def test_api_kount_empty_data(self):
        self.data = {}
        self.expected = {'WARNING_COUNT': 0, 'ERROR_COUNT': 1, 'MODE': 'E', 'ERROR_0': '401 EXTRA_DATA', 'ERRO': 401}
        self.request_and_response()

    def request_and_response(self):
        self.r = requests.Request('POST', 
                            self.url,
                            headers=self.headers_api, 
                            data=self.data,
                            )
        prepared = self.r.prepare()
        #~ pretty_print_POST(prepared)
        s = requests.Session()
        self.current = s.send(prepared)
        s.close()
        self.assertEqual(200, self.current.status_code)
        if self.data == {}:
            self.assertEqual(self.current.text, "MODE=E\nERRO=201")
            return
        self.assertEqual(200, self.current.status_code)
        self.assertNotIn('Error', self.current.json())
        self.assertEqual(200, self.current.status_code)
        added, removed, modified, same = dict_compare(self.current.json(), self.expected)
        added, removed, modified, same = dict_compare(self.current.json(), self.expected)
        if self.data["EMAL"]: 
            self.assertEqual(added, set())
            self.assertEqual(removed, set())
            self.assertEqual(sorted(list(same)), sorted([x for x in self.expected if not x.startswith('TRAN')]))
        return


if __name__ == "__main__":
    unittest.main(
        #~ warnings='ignore'
        #~ defaultTest="TestAPIRIS.test_api_kount_2_items_bad_s2em"
    )
