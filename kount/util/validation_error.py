#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"ValidationErrorType, VALIDATIONERROR, ValidationError"

from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class VALIDATIONERROR(object):
    """VALIDATIONERROR"""
    REGEX_ERR = 'REGEX'
    LENGTH_ERR = 'LENGTH'
    REQUIRED_ERR = 'REQUIRED'


class ValidationErrorType(Exception):
    """ValidationErrorType exception
        Args: value - Value of the error type - REGEX, LENGTH, REQUIRED.
    """
    def __init__(self, message=""):
        unicode_str = str(message)
        if isinstance(message, str) or unicode_str or not message:
            if message not in [
                    VALIDATIONERROR.LENGTH_ERR,
                    VALIDATIONERROR.REGEX_ERR, VALIDATIONERROR.REQUIRED_ERR]:
                message = "Expected value of the error type %s, %s, %s, "\
                        "found [%s]" % (VALIDATIONERROR.LENGTH_ERR,
                                        VALIDATIONERROR.REGEX_ERR,
                                        VALIDATIONERROR.REQUIRED_ERR,
                                        message)
        super(ValidationErrorType, self).__init__(message)


class ValidationError(ValidationErrorType):
    """Get the string representation of the error.
        Keyword arguments:
            field - the name of the bad field
            mode - the RIS mode the field is associated with
            value - field value
            pattern - the regular expression violated
            length - the maximum allowable length
        raise  ValidationError
    """
    def __init__(self, field="", mode="", value="", pattern="", length=0):
        validation_error = False
        if int(length) < len(field):
            self.message = "Field [%s] has length [%s] which is longer than "\
                           "the maximum of [%s]" % (field, len(field), length)
            self.error = VALIDATIONERROR.LENGTH_ERR
            validation_error = True
        if pattern:
            self.message = "Field [%s] has value [%s] which does not "\
                           "match the pattern [%s]" % (field, value, pattern)
            self.error = VALIDATIONERROR.REGEX_ERR
            validation_error = True
        if mode != "" and mode is not None:
            self.message = "Required field [%s] missing for mode [%s]" % (
                field, mode.upper())
            self.error = VALIDATIONERROR.REQUIRED_ERR
            validation_error = True
        if validation_error:
            super(ValidationError, self).__init__((self.error, self.message))
