#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"RisException, RisValidationException RisResponseException"

from __future__ import (
    absolute_import, unicode_literals, division, print_function)


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

ERROR_MESSAGES = {
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
    402: "Mismatched payment - type: you provided payment "
         "information in a field that did not match the payment type",
    403: 'Unnecessary anid',
    404: 'Unnecessary payment token',
    501: 'Unauthorized request',
    502: 'Unauthorized merchant',
    503: 'Unauthorized IP address',
    504: 'Unauthorized passphrase',
    601: 'System error',
    701: 'The transaction ID specified in the update was not found.'
    }


class RisException(Exception):
    """RIS exeption class:
        message - exception message
        cause - exception cause"""


class RisValidationException(RisException):
    """Ris validation exception class.
        kwargs -
            message - exception message
            cause - cause
            errors - list of errors encountered.
            """
    def __init__(self, message="", errors=[], cause=""):
        # Call the base class constructor with the parameters it needs
        self.message = message
        self.errors = errors
        self.cause = cause
        super(RisValidationException, self).__init__(
            self.message, self.cause, self.errors)


class RisResponseException(RisException):
    """Response exception
        kwargs -
            exception_code - Ris exception code
    """
    def __init__(self, exception_code):
        self.exception_code = ERROR_MESSAGES[exception_code]
        super(RisResponseException, self).__init__(self.exception_code)
