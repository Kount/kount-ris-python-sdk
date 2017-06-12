#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"Test XML to python dict"
from __future__ import absolute_import, unicode_literals, division, print_function
import unittest
import os
from kount.util.xmlparser import xml_to_dict
from kount.settings import RESOURCE_FOLDER, XML_FILENAME

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


XML_FILENAME_PATH = os.path.join(os.path.dirname(__file__), '..',
                                 RESOURCE_FOLDER, XML_FILENAME)

def dict_contains_subset(A, B):
    """extract Dict A From B
    DeprecationWarning: assertDictContainsSubset is deprecated for python 3.5
    self.assertDictContainsSubset(expected, actual[0])"""
    return dict([(k, B[k]) for k in A.keys() if k in B.keys()])


class TestXMLtoDict(unittest.TestCase):
    "parse xml from sdk to python dict"
    maxDiff = None

    def test_xml_to_dict(self):
        """ assert the new rules are added in XML_FILENAME,
        skip this test if the existed rules are changed"""
        actual = xml_to_dict(XML_FILENAME_PATH)
        expected = {
            'ANID': {'max_length': '64', 'mode': ['P'], 'required': True},
            'AUTH': {'reg_ex': '^[AD]$'},
            'AVST': {'reg_ex': '^[MNX]?$'},
            'AVSZ': {'reg_ex': '^[MNX]?$'},
            'B2A1': {'max_length': '256'},
            'B2A2': {'max_length': '256'},
            'B2CC': {'max_length': '2'},
            'B2CI': {'max_length': '256'},
            'B2PC': {'max_length': '16'},
            'B2PN': {'max_length': '32'},
            'B2ST': {'max_length': '256'},
            'BPREMISE': {'max_length': '256'},
            'BSTREET': {'max_length': '256'},
            'CASH': {'reg_ex': '^\\d{1,15}$'},
            'CAT1': {'max_length': '16'},
            'CAT2': {'max_length': '16'},
            'CURR': {'mode': ['Q', 'P', 'W', 'J'],
                     'reg_ex': '^[A-Z]{3}$',
                     'required': True},
            'CUSTOMER_ID': {'mode': ['W', 'J'], 'required': True},
            'CVVR': {'reg_ex': '^[MNX]?$'},
            'DOB': {'reg_ex': "^(19|20)\\d\\d-(0[1-9]|1[012])-"
                              "(0[1-9]|[12][0-9]|3[01])$"},
            'EMAL': {'max_length': '64', 'reg_ex': '^.+@.+\\..+$'},
            'EPOC': {'reg_ex': '^\\d{9,10}$'},
            'FRMT': {'max_length': '4', 'reg_ex': '^[JSON]+$'},
            'GENDER': {'reg_ex': '^[MFmf]?$'},
            'IPAD': {'max_length': '16',
                     'mode': ['Q', 'P', 'W', 'J'],
                     'reg_ex': "^\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?"
                               "[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4]"
                               "[0-9]|[01]?[0-9][0-9]?)\\b$",
                     'required': True},
            'LAST4': {'reg_ex': '^([a-zA-Z0-9]{4})?$'},
            'MACK': {'mode': ['Q', 'P', 'X', 'U', 'W'],
                     'reg_ex': '^[YN]$',
                     'required': True},
            'MERC': {'reg_ex': '^\\d{6}$', 'required': True},
            'MODE': {'reg_ex': '^Q|P|U|X|W|J$', 'required': True},
            'NAME': {'max_length': '64'},
            'ORDR': {'max_length': '32'},
            'PROD_DESC': {'max_length': '255'},
            'PROD_ITEM': {'max_length': '255', 'mode': ['Q', 'P', 'W'],
                          'required': True},
            'PROD_PRICE': {'mode': ['Q', 'P', 'W'],
                           'reg_ex': '^[0-9]+$',
                           'required': True},
            'PROD_QUANT': {'mode': ['Q', 'P', 'W'],
                           'reg_ex': '^[0-9]+$',
                           'required': True},
            'PROD_TYPE': {'max_length': '255', 'mode': ['Q', 'P', 'W'],
                          'required': True},
            'PTYP': {'mode': ['Q', 'P', 'W', 'J'], 'reg_ex': '^.+$',
                     'required': True},
            'RFCB': {'reg_ex': '^[RC]?$'},
            'S2A1': {'max_length': '256'},
            'S2A2': {'max_length': '256'},
            'S2CC': {'max_length': '2'},
            'S2CI': {'max_length': '256'},
            'S2EM': {'max_length': '64', 'reg_ex': '^.+@.+\\..+$'},
            'S2NM': {'max_length': '64'},
            'S2PC': {'max_length': '16'},
            'S2PN': {'max_length': '32'},
            'S2ST': {'max_length': '256'},
            'SESS': {'max_length': '32',
                     'mode': ['Q', 'P', 'X', 'U', 'W'],
                     'required': True},
            'SHTP': {'reg_ex': '^(SD|ND|2D|ST)?$'},
            'SITE': {'max_length': '8', 'mode': ['Q', 'P', 'W'],
                     'required': True},
            'SPREMISE': {'max_length': '256'},
            'SSTREET': {'max_length': '256'},
            'TOTL': {'mode': ['Q', 'P', 'W', 'J'],
                     'reg_ex': '^\\d{1,15}$',
                     'required': True},
            'TRAN': {'max_length': '32', 'mode': ['U', 'X'],
                     'required': True},
            'UAGT': {'max_length': '1024'},
            'UNIQ': {'max_length': '32'},
            'VERS': {'reg_ex': '^\\d{4}$', 'required': True}}
        self.assertLessEqual(len(expected), len(actual[0]))
        self.assertEqual(expected, dict_contains_subset(expected, actual[0]))


if __name__ == "__main__":
    unittest.main()
