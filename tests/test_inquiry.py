#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""Test Cases for Inquiry class"""

import unittest
from local_settings import (merchant_id as MERCHANT_ID,
                            ptok as PTOK)
from settings import sdk_version
from test_basic_connectivity import generate_unique_id, default_inquiry

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


EMAIL_CLIENT = "sdkTest@kountsdktestdomain.com"


class TestInquiry(unittest.TestCase):
    "Inquiry class tests"
    def setUp(self):
        session_id = generate_unique_id()
        self.result = default_inquiry(
            session_id=str(session_id),
            merchant_id=MERCHANT_ID,
            email_client=EMAIL_CLIENT, ptok=PTOK)
        self.maxDiff = None

    def test_utilities(self):
        "test_utilities"
        result = self.result
        expected = {
            'ANID': '',
            'AUTH': 'A',
            'AVST': 'M',
            'AVSZ': 'M',
            'B2A1': '1234 North B2A1 Tree Lane South',
            'B2A2': '',
            'B2CC': 'US',
            'B2CI': 'Albuquerque',
            'B2PC': '87101',
            'B2PN': '555-867-5309',
            'B2ST': 'NM',
            'BPREMISE': '',
            'BSTREET': '',
            'CASH': '4444',
            'CURR': 'USD',
            'CVVR': 'M',
            'EMAL': EMAIL_CLIENT,
            'FRMT': 'JSON',
            #~ 'IPAD': '131.206.45.21',
            'LAST4': '2514',
            'MACK': 'Y',
            'MERC': '999666',
            'MODE': 'Q',
            'NAME': 'SdkTestFirstName SdkTestLastName',
            #~ 'PENC': '',
            'PROD_DESC[0]': '3000 CANDLEPOWER PLASMA FLASHLIGHT',
            'PROD_ITEM[0]': 'SG999999',
            'PROD_PRICE[0]': '68990',
            'PROD_QUANT[0]': '2',
            'PROD_TYPE[0]': 'SPORTING_GOODS',
            'PTOK': '0007380568572514',
            'PTYP': 'CARD',
            'S2A1': '567 West S2A1 Court North',
            'S2A2': '',
            'S2CC': 'US',
            'S2CI': 'Gnome',
            'S2EM': 'sdkTestShipToEmail@kountsdktestdomain.com',
            'S2NM': 'SdkShipToFN SdkShipToLN',
            'S2PC': '99762',
            'S2PN': '555-777-1212',
            'S2ST': 'AK',
            'SDK': 'CUST',
            'SDK_VERSION': 'Sdk-Ris-Python-%s' % sdk_version,
            'SITE': 'DEFAULT',
            'SPREMISE': '',
            'SSTREET': '',
            'TOTL': '123456',
            'VERS': sdk_version,
            }
        actual = result.params
        self.assertIn(expected['SDK_VERSION'], actual['SDK_VERSION'])
        del (actual['UNIQ'], actual['IPAD'], actual['SDK_VERSION'],
             expected['SDK_VERSION'], actual['SESS'], actual['ORDR'])
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
