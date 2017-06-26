#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"class Client"

from __future__ import absolute_import, unicode_literals, division, print_function
import logging
import requests
from .ris_validator import RisValidator, RisValidationException
from .util.khash import Khash
from .settings import TIMEOUT, RAISE_ERRORS


__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


logger = logging.getLogger('kount.client')


class Client:
    """Transport class
    raise_errors - False - log them only
                   True - raise them before request.post
    """
    def __init__(self, url, key, timeout=TIMEOUT, raise_errors=RAISE_ERRORS):
        self.url = url
        self._kount_api_key = key
        self.raise_errors = raise_errors
        Khash.verify()
        self.timeout = timeout
        self.validator = RisValidator(raise_errors=raise_errors)
        logger.debug("url - %s, len_key - %s", url, len(key))

    def process(self, params):
        """validate data and request post
        https://pypi.python.org/pypi/requests - 0.13.3
        Use simplejson if available.
        if raise_errors==False, the validation errors will not be raised,
        only logged; by default raise_errors=True"""
        invalid, missing_in_xml, empty = self.validator.ris_validator(params=params)
        if invalid:
            message = "validation errors = %s, missing_in_xml = %s,"\
                      "empty = %s" % (invalid, missing_in_xml, empty)
            logger.error(message)
            if self.raise_errors:
                raise RisValidationException(
                    message, errors=invalid, cause="empty = %s" % empty)
        headers_api = {'X-Kount-Api-Key': self._kount_api_key}
        merc = params.get('MERC', None)
        params['FRMT'] = 'JSON'
        logger.debug("url=%s, headers=%s, params=%s", self.url,
                     headers_api, params)
        request = requests.post(self.url,
                                headers=headers_api,
                                data=params,
                                timeout=self.timeout)
        try:
            req_json = request.json()
        except ValueError as jde:
            logger.error("ValueError - %s", jde)
            try:
                text_to_json = parse_k_v(request.text)
                logger.debug("process text: %s", text_to_json)
                return text_to_json
            except ValueError:
                error = "Neither JSON nor String %s" % request.text
                logger.debug(error)
                raise ValueError(error)
        else:
            roundtrip = request.elapsed.total_seconds()
            sess = params.get("SESS", None)
            logger.debug("MERC = %s, SESS = %s, SDK ELAPSED = %s ms.",
                         merc, sess, roundtrip)
            return req_json


def parse_k_v(text):
    "parse text to dict"
    return dict(c.split('=', 1) for c in text.split('\n'))
