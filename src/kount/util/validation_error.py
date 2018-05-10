#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"VALIDATIONERROR, ValidationError"

from __future__ import absolute_import, unicode_literals, division, \
    print_function

from kount.version import VERSION

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class ValidationError(Exception):
    _REGEX_ERR = 'REGEX'
    _LENGTH_ERR = 'LENGTH'
    _REQUIRED_ERR = 'REQUIRED'
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
        self.error = None
        self.message = None
        if 0 < length < len(field):
            self.message = "Field [%s] has length [%s] which is longer than "\
                           "the maximum of [%s]" % (field, len(field), length)
            self.error = self._LENGTH_ERR
        elif pattern:
            self.message = "Field [%s] has value [%s] which does not "\
                           "match the pattern [%s]" % (field, value, pattern)
            self.error = self._REGEX_ERR
        elif mode:
            self.message = "Required field [%s] missing for mode [%s]" % (
                field, mode.upper())
            self.error = self._REQUIRED_ERR
        if not self.error or not self.message:
            raise RuntimeError("ValidationError not set")
        super(ValidationError, self).__init__(self.message)
