# -*- coding: utf-8 -*-
import requests
import json
import unittest
from random import randint
import time
from pretty_print import pretty_print_POST
from json_test import example_data
from local_settings import kountAPIkey

#~ requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#~ from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
        self.headers = {}
        self.url = "https://risk.test.kount.net"
        self.headers_api = {'X-Kount-Api-Key': self.kountAPIkey}
        self.url_API = "https://api.test.kount.net/rpc/v1/orders/detail.json"
        self.r = requests.Request('POST', 
                                                self.url,
                                                headers=self.headers_api, 
                                                data=example_data,
                                                #~ verify=False,
                                                    )
        prepared = self.r.prepare()
        pretty_print_POST(prepared)
        s = requests.Session()
        self.currentR = s.send(prepared)

    def test_api_Kount(self):
        #~ expected modified 'TRAN'
        currentR = self.currentR.json()
        expected = {"VERS":"0695","MODE":"Q","TRAN":"PHJJ03Z1TT95","MERC":"999666","SESS":"088E9F4961354D4F90041988B8D5C66B","ORDR":"088E9F496135","AUTO":"R","SCOR":"34","GEOX":"US","BRND":None,"REGN":None,"NETW":"N","KAPT":"N","CARDS":"1","DEVICES":"1","EMAILS":"1","VELO":"0","VMAX":"0","SITE":"DEFAULT","DEVICE_LAYERS":"....","FINGERPRINT":None,"TIMEZONE":None,"LOCALTIME":" ","REGION":None,"COUNTRY":None,"PROXY":None,"JAVASCRIPT":None,"FLASH":None,"COOKIES":None,"HTTP_COUNTRY":None,"LANGUAGE":None,"MOBILE_DEVICE":None,"MOBILE_TYPE":None,"MOBILE_FORWARDER":None,"VOICE_DEVICE":None,"PC_REMOTE":None,"RULES_TRIGGERED":1,"RULE_ID_0":"1024842","RULE_DESCRIPTION_0":"Review if order total > $1000 USD","COUNTERS_TRIGGERED":0,"REASON_CODE":None,"DDFS":None,"DSR":None,"UAS":None,"BROWSER":None,"OS":None,"PIP_IPAD":None,"PIP_LAT":None,"PIP_LON":None,"PIP_COUNTRY":None,"PIP_REGION":None,"PIP_CITY":None,"PIP_ORG":None,"IP_IPAD":None,"IP_LAT":None,"IP_LON":None,"IP_COUNTRY":None,"IP_REGION":None,"IP_CITY":None,"IP_ORG":None,"WARNING_COUNT":0}
        self.assertEqual(currentR.keys(), expected.keys())
        added, removed, modified, same = dict_compare(currentR, expected)
        self.assertEqual(added, set())
        self.assertEqual(removed, set())
        a = list(same)
        a.sort()
        b = [x for x in list(expected.keys()) if not x.startswith('TRAN')]
        b.sort()
        self.assertEqual(a, b)

    def tearDown(self):
        self.assertNotIn('Error', self.currentR.json())
        self.assertEqual(200, self.currentR.status_code)


if __name__ == "__main__":
    unittest.main()
