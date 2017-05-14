#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"
python_version = "3.6"
resource_folder = "resources"
xml_filename = 'validate.xml'
xml_dict = 'xml_dict.py'
sdk_version = "0695"
#https://support.kount.com/Developer_Resources/Getting_Started/Technical_Specification_Guide_r._January_2016_-_v_6.4.5
error_messages = {
    201: 'Missing version',
    202: 'Missing mode',
    203: 'Missing merchant ID',
    204: 'Missing session ID',
    205: 'Missing transaction ID',
    211: 'Missing currency type',
    212: 'Missing total',
    221: 'Missing email',
    222: 'Missing anid',
    231: 'Missing payment type',
    232: 'Missing card number',
    233: 'Missing check micro',
    234: 'Missing PayPal ID',
    235: 'Missing Payment Token',
    241: 'Missing IP address',
    251: 'Missing merchant acknowledgement',
    261: 'Missing post body',
    301: 'Bad version',
    302: 'Bad mode',
    303: 'Bad merchant ID',
    304: 'Bad session ID',
    305: 'Bad trasaction ID',
    311: 'Bad currency type',
    312: 'Bad total',
    321: 'Bad anid',
    331: 'Bad payment type',
    332: 'Bad card number',
    333: 'Bad check micro',
    334: 'Bad PayPal ID',
    335: 'Bad Google ID',
    336: 'Bad Bill Me Later ID',
    341: 'Bad IP address',
    351: 'Bad merchant acknowledgement',
    399: 'Bad option',
    401: 'Extra data',
    402: 'Mismatched payment - type: you provided payment information in a field that did not match the payment type',
    403: 'Unnecessary anid',
    404: 'Unnecessary payment token',
    501: 'Unauthorized request',
    502: 'Unauthorized merchant',
    503: 'Unauthorized IP address',
    504: 'Unauthorized passphrase',
    601: 'System error',
    701: 'The transaction ID specified in the update was not found.'
    }
