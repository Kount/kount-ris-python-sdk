#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""class Client"""

from __future__ import (absolute_import, unicode_literals,
                        division, print_function)

import logging
import requests

from . import config
from . import request
from . import response
from .ris_validator import RisValidator, RisValidationException
from .version import VERSION

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


LOG = logging.getLogger('kount.client')


class Client:

    def __init__(self, api_url, api_key,
                 timeout=None,
                 raise_errors=None):
        """
        Client class used to execute Kount request
        :param api_url: endpoint to which the request should be sent
        :param api_key: merchant api key, provided by Kount
        :param timeout: request timeout, if not set the default value
         from SDKConfig will be used
        :param raise_errors: indicates if request validation error should
         be thrown, if not set the default value from SDKConfig will be used
        """
        self.api_url = api_url
        self.api_key = api_key
        conf = config.SDKConfig
        self.timeout = timeout or conf.get_default_timeout()
        if raise_errors is None:
            raise_errors = conf.get_should_raise_validation_errors()
        self.raise_errors = raise_errors
        self.validator = RisValidator(conf.get_rules_xml_file(),
                                      raise_errors)
        LOG.debug("url - %s, len_key - %s", self.api_url, len(self.api_key))

    def process(self, req):
        if not isinstance(req, request.Request):
            raise ValueError("invalid request %s" % type(request))
        res = self._execute(req.params)
        if res:
            return response.Response(res)
        return None

    def _execute(self, params):
        """validate data and request post
        https://pypi.python.org/pypi/requests
        Use simplejson if available.
        if raise_errors==False, the validation errors will not be raised,
        only logged; by default raise_errors=True"""
        if LOG.isEnabledFor(logging.DEBUG):
            for key, param in params.items():
                LOG.debug('%s=%s', key, param)
        invalid, missing_in_xml, empty = self.validator.ris_validator(
            params=params)
        if invalid:
            message = "validation errors = %s, missing_in_xml = %s,"\
                      "empty = %s" % (invalid, missing_in_xml, empty)
            LOG.error(message)
            if self.raise_errors:
                raise RisValidationException(
                    message, errors=invalid, cause="empty = %s" % empty)
        headers_api = {'X-Kount-Api-Key': self.api_key}
        params['FRMT'] = 'JSON'
        LOG.debug("url=%s, headers=%s, params=%s", self.api_url,
                  headers_api, params)

        req = requests.post(self.api_url,
                            headers=headers_api,
                            data=params,
                            timeout=self.timeout)
        try:
            resp = req.json()
        except ValueError as jde:
            LOG.error("ValueError - %s", jde)
            try:
                text_to_json = parse_k_v(req.text)
                LOG.debug("process text: %s", text_to_json)
                return text_to_json
            except ValueError:
                error = "Neither JSON nor String %s" % req.text
                LOG.debug(error)
                raise ValueError(error)
        else:
            LOG.debug("MERC = %s, SESS = %s, SDK ELAPSED = %s ms.",
                      params.get('MERC', None),
                      params.get("SESS", None),
                      req.elapsed.total_seconds())
            return resp


def parse_k_v(text):
    """parse text to dict"""
    return dict(c.split('=', 1) for c in text.split('\n'))
