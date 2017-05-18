#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://bitbucket.org/panatonkount/sdkpython
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
import logging
import unittest
import os
import requests

from local_settings import timeout, raise_errors
from settings import resource_folder, xml_filename
from ris_validator import RisValidator
from util.xmlparser import xml_to_dict
from simplejson.scanner import JSONDecodeError


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


XML_FILE = os.path.join(os.path.dirname(__file__),
                        resource_folder, xml_filename)

LOGGER = logging.getLogger('kount')


class Client:
    """Transport class
    raise_errors - False - log them only
                   True - raise them before request.post
    """
    def __init__(self, url, key):
        self.url = url
        self.kount_api_key = key
        self.headers_api = {'X-Kount-Api-Key': self.kount_api_key}
        self.xml_to_dict1, self.required, self.notrequired = xml_to_dict(
            XML_FILE)
        self.validator = RisValidator(raise_errors=raise_errors)
        self.raise_errors = raise_errors
        prepared = "url - %s, len_key - %s" % (url, len(key))
        LOGGER.debug(prepared)

    def process(self, params):
        "validate data and request post"
        try:
            assert params['FRMT'] == 'JSON'
        except KeyError:
            params['FRMT'] = 'JSON'
        invalid, missing_in_xml, empty = self.validator.ris_validator(
            params=params,
            xml_to_dict1=self.validator.xml_to_dict1,
            )
        LOGGER.debug("validation errors= %s" % invalid)
        LOGGER.debug("validation missing_in_xml = %s, empty= %s" % (
            missing_in_xml, empty))
        request = requests.post(self.url,
                                headers=self.headers_api,
                                data=params,
                                timeout=timeout)
        prepared = "%s, %s, %s" % (
            self.url, self.headers_api, params.items)
        LOGGER.debug(prepared)
        try:
            LOGGER.debug(request.json())
            return request.json()
        except JSONDecodeError as jde:
            LOGGER.debug(jde)
            try:
                text_to_json = {
                    c.split('=')[0]:
                    c.split('=')[1] for c in request.text.split('\n')}
                LOGGER.debug(text_to_json)
                return text_to_json
            except IndexError:
                error = "Neither JSON nor String %s" % request.text
                LOGGER.debug(error)
                raise ValueError(error)


if __name__ == "__main__":
    unittest.main()
