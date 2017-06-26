#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"example data from https://kopana.atlassian.net/wiki/display/KS/Testing"
from __future__ import absolute_import, unicode_literals, division, print_function
__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


example_data = {
    'ANID': '',
    'AUTH': 'A',
    'AVST': 'M',
    'AVSZ': 'M',
    'B2A1': '1234+North+B2A1+Tree+Lane+South',
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
    'NAME': 'Goofy+Grumpus',
    'ORDR': '088E9F496135',
    'PROD_DESC[]': '3000+CANDLEPOWER+PLASMA+FLASHLIGHT',
    'PROD_ITEM[]': 'SG999999',
    'PROD_PRICE[]': '68990',
    'PROD_QUANT[]': '2',
    'PROD_TYPE[]': 'SPORTING%5FGOODS',
    'PTOK': '0007380568572514',
    'PTYP': 'CARD',
    'S2A1': '567+West+S2A1+Court+North',
    'S2CC': 'US',
    'S2CI': 'Gnome',
    'S2EM': 'sdkTestShipTo@kountsdktestdomain.com',
    'S2NM': 'SdkTestShipToFirst+SdkShipToLast',
    'S2PC': '99762',
    'S2PN': '208+777-1212',
    'S2ST': 'AK',
    'SESS': '088E9F4961354D4F90041988B8D5C66B',
    'SITE': 'DEFAULT',
    'TOTL': '123456',
    'UAGT': 'Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10%5F9%5F5%29+'\
            'AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+'\
            'Chrome%2F37.0.2062.124+Safari%2F537.36',
    'UNIQ': '088E9F4961354D4F9004',
    'VERS': '0695'
}

example_data_products = {
    'ANID': '',
    'AUTH': 'A',
    'AVST': 'M',
    'AVSZ': 'M',
    'B2A1': '1234+North+B2A1+Tree+Lane+South',
    'B2CC': 'US',
    'B2CI': 'Albuquerque',
    'B2PC': '87101',
    'B2PN': '555+867-5309',
    'B2ST': 'NM',
    'CASH': '4444',
    'CURR': 'USD',
    'CVVR': 'M',
    'EMAL': 'curly.riscaller15@kountqa.com',
    'FRMT': 'JSON', # set if not via sdk
    'IPAD': '129.173.116.98',
    'MACK': 'Y',
    'MERC': '999666',
    'MODE': 'Q',
    'NAME': 'Goofy+Grumpus',
    'ORDR': 'F8E874A38B7B',
    'PROD_DESC[0]': '3000+CANDLEPOWER+PLASMA+FLASHLIGHT',
    'PROD_DESC[1]': '3000+HP+NUCLEAR+TOILET',
    'PROD_ITEM[0]': 'SG999999',
    'PROD_ITEM[1]': 'TP999999',
    'PROD_PRICE[0]': '68990',
    'PROD_PRICE[1]': '1000990',
    'PROD_QUANT[0]': '2',
    'PROD_QUANT[1]': '44',
    'PROD_TYPE[0]': 'SPORTING%5FGOODS',
    'PROD_TYPE[1]': 'SPORTING%5FGOODS2',
    'PTOK': '0055071350519059',
    'PTYP': 'CARD',
    'S2A1': '567+West+S2A1+Court+North',
    'S2CC': 'US',
    'S2CI': 'Gnome',
    'S2EM': 'sdkTestShipTo@kountsdktestdomain.com',
    'S2NM': 'SdkTestShipToFirst+SdkShipToLast',
    'S2PC': '99762',
    'S2PN': '208+777-1212',
    'S2ST': 'AK',
    'SESS': 'F8E874A38B7B4B6DBB71492A584A969D',
    'SITE': 'DEFAULT',
    'TOTL': '107783',
    'UAGT': 'Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10%5F9%5F5%29+'\
            'AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+'\
            'Chrome%2F37.0.2062.124+Safari%2F537.36',
    'UNIQ': 'F8E874A38B7B4B6DBB71',
    'SDK': 'CUST',
    'VERS': '0695'
    }
