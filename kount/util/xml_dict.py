#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""generated from xmlparser.py, must be updated if
changed xml_filename = 'validate.xml' from settings.py"""
from __future__ import (
    absolute_import, unicode_literals, division, print_function)

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


xml_dict = {
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
    'DOB': {'reg_ex': '^(19|20)\\d\\d-(0[1-9]|1[012])-'\
            '(0[1-9]|[12][0-9]|3[01])$'},
    'EMAL': {'max_length': '64', 'reg_ex': '^.+@.+\\..+$'},
    'EPOC': {'reg_ex': '^\\d{9,10}$'},
    'FRMT': {'max_length': '4', 'reg_ex': '^[JSON]+$'},
    'GENDER': {'reg_ex': '^[MFmf]?$'},
    'IPAD': {'max_length': '16',
             'mode': ['Q', 'P', 'W', 'J'],
             'reg_ex': '^\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]'\
             '[0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b$',
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
    'PTYP': {'mode': ['Q', 'P', 'W', 'J'], 'reg_ex': '^.+$', 'required': True},
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
    'SITE': {'max_length': '8', 'mode': ['Q', 'P', 'W'], 'required': True},
    'SPREMISE': {'max_length': '256'},
    'SSTREET': {'max_length': '256'},
    'TOTL': {'mode': ['Q', 'P', 'W', 'J'],
             'reg_ex': '^\\d{1,15}$',
             'required': True},
    'TRAN': {'max_length': '32', 'mode': ['U', 'X'], 'required': True},
    'UAGT': {'max_length': '1024'},
    'UNIQ': {'max_length': '32'},
    'VERS': {'reg_ex': '^\\d{4}$', 'required': True}
    }
