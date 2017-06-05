#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"class Client"

from __future__ import (
    absolute_import, unicode_literals, division, print_function)
import logging
import os
import requests
from .settings import RESOURCE_FOLDER, XML_FILENAME
from .ris_validator import RisValidator
from .util.xmlparser import xml_to_dict


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


XML_FILE = os.path.join(os.path.dirname(__file__), '..',
                        RESOURCE_FOLDER, XML_FILENAME)

logger = logging.getLogger('kount.client')


class Client:
    """Transport class
    raise_errors - False - log them only
                   True - raise them before request.post
    """
    def __init__(self, url, key, timeout=5, raise_errors=False):
        self.url = url
        self.timeout = timeout
        self.kount_api_key = key
        self.headers_api = {'X-Kount-Api-Key': self.kount_api_key}
        self.xml_2_dict, self.required, self.notrequired = xml_to_dict(
            XML_FILE)
        self.raise_errors = raise_errors
        self.validator = RisValidator(raise_errors=self.raise_errors)
        logger.debug("url - %s, len_key - %s", url, len(key))

    def process(self, params):
        """validate data and request post
        https://pypi.python.org/pypi/requests - 0.13.3
        Use simplejson if available."""
        try:
            assert params['FRMT'] == 'JSON'
        except KeyError:
            params['FRMT'] = 'JSON'
        invalid, missing_in_xml, empty = self.validator.ris_validator(
            params=params,
            xml_2_dict=self.validator.xml_2_dict,
            )
        logger.debug("validation errors= %s, missing_in_xml = %s, "
                     "empty = %s", invalid, missing_in_xml, empty)
        request = requests.post(self.url,
                                headers=self.headers_api,
                                data=params,
                                timeout=self.timeout)
        logger.debug("url %s, headers %s, params %s", self.url,
                     self.headers_api, params)
        try:
            req_json = request.json()
            logger.debug("process json: %s", req_json)
            return req_json
        except ValueError as jde:
            logger.debug("ValueError - %s", jde)
            try:
                text_to_json = {
                    c.split('=')[0]:
                    c.split('=')[1] for c in request.text.split('\n')}
                logger.debug("process text: %s", text_to_json)
                return text_to_json
            except IndexError:
                error = "Neither JSON nor String %s" % request.text
                logger.debug(error)
                raise ValueError(error)
