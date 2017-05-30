#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"RisException, RisValidationException RisResponseException"
from settings import error_messages

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


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
        self.exception_code = error_messages[exception_code]
        super(RisResponseException, self).__init__(self.exception_code)
