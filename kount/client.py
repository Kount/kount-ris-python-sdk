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
from .settings import TIMEOUT, SDK_VERSION, RAISE_ERRORS


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
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
        card_solted = Khash.hash_payment_token(token="666666669")
        if card_solted != "6666662I8EDD7LNC77GP" and raise_errors:
            mesg = "Configured SALT phrase is incorrect"
            logger.error(mesg)
            raise ValueError(mesg)
        self.timeout = timeout

        self.validator = RisValidator(raise_errors=raise_errors)
        logger.debug("url - %s, len_key - %s", url, len(key))

    def process(self, params):
        """validate data and request post
        https://pypi.python.org/pypi/requests - 0.13.3
        Use simplejson if available."""
        invalid, missing_in_xml, empty = self.validator.ris_validator(params=params)
        if invalid:
            message = "validation errors = %s, missing_in_xml = %s, empty = %s" % (
                invalid, missing_in_xml, empty)
            logger.error(message)
            if self.raise_errors:
                raise RisValidationException(
                    message, errors=invalid, cause="empty = %s" % empty)
        headers_api = {'X-Kount-Api-Key': self._kount_api_key}
        try:
            headers_api["X-Kount-Merc-Id"] = params['MERC']
        except KeyError:
            message = "Required field 'MERC' is missing. \
                       Header's param 'X-Kount-Merc-Id' is not set."
            logger.debug(message)
            if self.raise_errors:
                raise RisValidationException(
                    message, errors=['MERC'], cause="MERC is missing")
        params['FRMT'] = 'JSON'
        logger.debug("url %s, headers %s, params %s", self.url,
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
            logger.debug("process json: %s", req_json)
            return req_json            

def parse_k_v(text):
    return dict(c.split('=', 1) for c in text.split('\n'))
