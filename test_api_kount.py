#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

import requests
import unittest
import os
import json
from pretty_print import pretty_print_POST
from json_test import example_data, example_data_products
from local_settings import kountAPIkey, url_api
from settings import resource_folder, xml_filename
from ris_validator import RisValidator
from util.xmlparser import xml_to_dict
from response import Response

#~ from pprint import pprint
#~ from local_settings import url_api
xml_filename_path = os.path.join(os.path.dirname(__file__),
                            resource_folder, xml_filename)


class Client:
    def __init__(self, url, key):
        self.url = url_api
        self.kountAPIkey = key
        self.headers_api = {'X-Kount-Api-Key': self.kountAPIkey
                            #~ , 'Accept': 'application/json'
                            }
        self.xml_to_dict1, self.required_field_names, self.notrequired_field_names = xml_to_dict(xml_filename_path)
        
    def process(self, params):
        assert params['FRMT'] == 'JSON'

        self.validator = RisValidator.ris_validator(self, params, self.xml_to_dict1)
        self.r = requests.post(self.url,
                            headers=self.headers_api, 
                            data=params,
                            )
        """prepared = self.r.prepare()
        pretty_print_POST(prepared)
        s = requests.Session()
        self.current = s.send(prepared)
        s.close()"""
        #~ print ("/////////////", self.r.status_code)
        #~ print ("//////////text", self.r.text, "7"*10)
        #~ print ("json//", self.r.json())

        if self.r.json == {}:
            self.assertEqual(self.r.text, "MODE=E\nERRO=201")
            return
        assert 200 == self.r.status_code
        #~ print('***********', self.current.json())
        assert 'Error' not in self.r.text
        rs = Response(self.r)
        #~ print("Response(self.current----------", rs.get_kc_warnings(), rs.get_warnings())
        return self.r

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
        self.url = url_api
        self.headers_api = {'X-Kount-Api-Key': self.kountAPIkey}

    def test_api_kount(self):
        #~ expected modified 'TRAN'
        #~ self.data = example_data
        self.data = example_data_products.copy()
        self.data['IPAD'] = "131.206.45.21"

        #~ del(self.data['B2A2'])
        l500 = []
        lmiss = []
        self.expected = example_data
        #~ self.data = {'AUTH': 'A', 'AVST': 'M', 'EMAL': 'sdkTest@kountsdktestdomain.com', 'S2CC': 'US', 'CVVR': 'M', 'B2CI': 'Albuquerque', 'PTYP': 'CARD', 'BPREMISE': '', 'S2PN': '555-777-1212', 'AVSZ': 'M', 'IPAD': '131.206.45.21', 'PROD_ITEM[0]': 'SG999999', 'B2ST': 'NM', 'B2A1': '1234 North B2A1 Tree Lane South', 'S2PC': '99762', 'SITE': 'DEFAULT', 'S2A1': '567 West S2A1 Court North', 'VERS': '0695', 'MACK': 'Y', 'SPREMISE': '', 'NAME': 'SdkTestFirstName SdkTestLastName', 'PROD_TYPE[0]': 'SPORTING_GOODS', 'S2A2': None, 'PROD_QUANT[0]': 2, 'ORDR': '655e7318-35', 'SSTREET': '', 'S2ST': 'AK', 'S2CI': 'Gnome', 'S2EM': 'sdkTestShipToEmail@kountsdktestdomain.com', 'PROD_DESC[0]': '3000 CANDLEPOWER PLASMA FLASHLIGHT', 'B2CC': 'US', 'BSTREET': '', 'CURR': 'USD', 'SDK_VERSION': 'Sdk-Ris-Python-0695-201705111526', 'SESS': '655e7318-35eb-461a-8859-d44202bc', 'TOTL': 123456, 'B2PC': '87101', 'MERC': 999666, 'UNIQ': '655e7318-35eb-461a-88', 'PROD_PRICE[0]': 68990, 'B2A2': None, 'MODE': 'Q', 'PTOK': '0007380568572514', 'S2NM': 'SdkShipToFN SdkShipToLN', 'B2PN': '555-867-5309', 'LAST4': '2514', 'SDK': 'PYTH'}
        self.data = {'B2ST': 'NM', 'S2A1': '567+West+S2A1+Court+North', 'EMAL': 'sdkTest@kountsdktestdomain.com',
                      'B2CC': 'US', 'LAST4': '2514', 'S2ST': 'AK', 'PROD_QUANT[0]': '2', 'CURR': 'USD',
                      #~ 'S2A2': None,
                      'B2A1': '1234+North+B2A1+Tree+Lane+South', 'IPAD': '131.206.45.21', 'SESS': '6ba5d072-6c88-4dfa-bcea-a3714b06',
                      #~ 'B2A2': None,
                      'S2EM': 'sdkTestShipToEmail@kountsdktestdomain.com', 'BPREMISE': '', 'S2PN': '555-777-1212',
                      'ORDR': '6ba5d072-6c', 'B2PN': '555-867-5309', 'S2CI': 'Gnome', 'B2CI': 'Albuquerque',
                      'SITE': 'DEFAULT', 'MERC': '999666', 'VERS': '0695',
                      'SDK': 'JAVA',
                      'PROD_DESC[0]': '3000+CANDLEPOWER+PLASMA+FLASHLIGHT', 'S2PC': '99762', 'CVVR': 'M', 'PTOK': '0007380568572514',
                      'TOTL': '123456', 'S2CC': 'US', 'MODE': 'Q', 'B2PC': '87101', 'NAME': 'SdkTestFirstName+SdkTestLastName',
                      'SSTREET': '', 'AUTH': 'A', 'AVSZ': 'M', 'BSTREET': '', 'PROD_TYPE[0]': 'SPORTING_GOODS', 'MACK': 'Y',
                      'PROD_PRICE[0]': '68990',     'UAGT': 'Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10%5F9%5F5%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F37.0.2062.124+Safari%2F537.36',
                      'UNIQ': 'F8E874A38B7B4B6DBB71', 'PTYP': 'CARD',
                      'SDK_VERSION': 'Sdk-Ris-Python-0695-201705111625', 'PROD_ITEM[0]': 'SG999999',
                      'S2NM': 'SdkShipToFN+SdkShipToLN', 'SPREMISE': '', 'AVST': 'M',
                      'FRMT':'JSON', 'CASH': '4444', 'ANID':''}
        """for k in self.data:
            if k not in self.data1:
                lmiss.append((k, self.data[k]))
            self.data = example_data_products.copy()
            self.data[k] = self.data1.get(k,'someDefault')
            if self.data[k] == "FRMT":
                self.data1.get(k, 'JSON')
            else:
                self.data[k] = self.data1.get(k,'someDefault')
            try:
                self.request_and_response()
            except AssertionError:
                print('/'*20, k)
                l500.append((k, self.data[k], self.data1.get(k,'someDefault')))
        print('l500', l500)
        print('lmiss', lmiss)"""
        self.request_and_response()

    def test_api_kount_2_items(self):
        #~ expected modified 'TRAN'
        self.data = example_data_products
        self.expected = {'BROWSER': None, 'IP_LON': None, 'DEVICES': '1', 'SITE': 'DEFAULT', 'VERS': '0695', 'SESS': 'F8E874A38B7B4B6DBB71492A584A969D', 'VMAX': '0', 'JAVASCRIPT': None, 'LOCALTIME': ' ', 'REGN': 'CA_NS', 'DDFS': None, 'FLASH': None, 'FINGERPRINT': None, 'MERC': '999666', 'REGION': None, 'BRND': None, 'TIMEZONE': None, 'PIP_COUNTRY': None, 'MOBILE_DEVICE': None, 'PIP_LAT': None, 'EMAILS': '1', 'TRAN': 'PHH30BXK2GTG', 'IP_LAT': None, 'IP_CITY': None, 'ORDR': 'F8E874A38B7B', 'COOKIES': None, 'AUTO': 'R', 'MOBILE_TYPE': None, 'IP_REGION': None, 'COUNTERS_TRIGGERED': 0, 'PIP_REGION': None, 'PROXY': None, 'IP_ORG': None, 'WARNING_COUNT': 0, 'NETW': 'N', 'RULE_ID_0': '1024842', 'PIP_ORG': None, 'PC_REMOTE': None, 'REASON_CODE': None, 'PIP_CITY': None, 'VOICE_DEVICE': None, 'UAS': None, 'KAPT': 'N', 'MODE': 'Q', 'MOBILE_FORWARDER': None, 'DSR': None, 'HTTP_COUNTRY': None, 'IP_COUNTRY': None, 'SCOR': '34', 'LANGUAGE': None, 'PIP_LON': None, 'COUNTRY': None, 'GEOX': 'CA', 'RULES_TRIGGERED': 1, 'OS': None, 'CARDS': '1', 'DEVICE_LAYERS': '....', 'VELO': '0', 'IP_IPAD': None, 'RULE_DESCRIPTION_0': 'Review if order total > $1000 USD', 'PIP_IPAD': None}
        self.request_and_response()

    def test_api_kount_last_2_items_bad_email(self):
        self.data = example_data_products.copy()
        self.data["EMAL"] = 'curly.riscaller12%40kountqa.com'
        self.expected = {'ERROR_0': '321 BAD_EMAL Cause: [[curly.riscaller12%40kountqa.com is an invalid email address], Field: [EMAL], Value: [curly.riscaller12%40kountqa.com]', 'ERRO': 321, 'ERROR_COUNT': 1, 'WARNING_COUNT': 0, 'MODE': 'E'}
        self.request_and_response()

    def test_api_kount_2_items_bad_s2em(self):
        #~ S2EM': 'sdkTestShipTo%40kountsdktestdomain.com
        example_data_products["S2EM"] = 'sdkTestShipTo%40kountsdktestdomain.com'
        self.data = example_data_products
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
        example_data_products["EMAL"] = None
        self.data = example_data_products
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
        
        try:
            self.assertEqual(200, self.current.status_code)
        except AssertionError as e:
            print(500, e)
            pretty_print_POST(prepared)
            s.close()
            raise e
        s.close()
        print('j'*10, self.current.json())

        if self.data == {}:
            self.assertEqual(self.current.text, "MODE=E\nERRO=201")
            return
        self.assertEqual(200, self.current.status_code)
        self.assertNotIn('Error', self.current.json())
        added, removed, modified, same = dict_compare(self.current.json(), self.expected)
        if self.data["EMAL"]:
            print(added)
            print(removed)
            #~ self.assertEqual(added, set())
            #~ self.assertEqual(removed, set())
            #~ self.assertEqual(sorted(list(same)), sorted([x for x in self.expected if not x.startswith('TRAN')]))
        return


if __name__ == "__main__":
    unittest.main(
        #~ warnings='ignore'
        defaultTest="TestAPIRIS.test_api_kount"
        #~ defaultTest="TestAPIRIS.test_api_kount_2_items"
    )
