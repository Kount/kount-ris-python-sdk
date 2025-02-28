#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk
# Copyright (C) 2025 Kount an Equifax Company All Rights Reserved.
"""class Client"""

import logging
import requests

from tests.conftest import api_url
from . import config
from . import request
from . import response
from datetime import datetime, timedelta
from .version import VERSION
from .config import SDKConfig

__author__ = SDKConfig.SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDKConfig.SDK_MAINTAINER
__email__ = SDKConfig.MAINTAINER_EMAIL
__status__ = SDKConfig.STATUS


LOG = logging.getLogger('kount.client')


class Client:

    def __init__(self, api_url, api_key,
                 timeout=None,
                 raise_errors=None,
                 migration_mode_enabled=False,
                 pf_client_id=None,  # Payments Fraud by Kount 360 Client ID goes here
                 pf_auth_endpoint='https://login.kount.com/oauth2/aus12zvb2vueTvA7F0h8/v1/token',
                 pf_api_endpoint='https://api.kount.com/commerce/ris',
                 pf_api_key='API_KEY_GOES_HERE'
                 ):
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
        LOG.debug("url - %s, len_key - %s", self.api_url, len(self.api_key))
        self.migration_mode_enabled = migration_mode_enabled
        self.pf_client_id = pf_client_id
        self.pf_auth_endpoint = pf_auth_endpoint
        self.pf_api_endpoint = pf_api_endpoint
        self.pf_api_key = pf_api_key
        self.auth_token = AuthorizationToken(None, None, None, None)

    def process(self, req):

        if not isinstance(req, request.Request):
            raise ValueError("invalid request, %s" % type(request))
        
        res = self._execute(req.params)
        if res:
            return response.Response(res)
        return None

    def _refresh_auth_token(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': 'Basic ' + self.pf_api_key
        }

        data = {
            'scope': 'k1_integration_api',
            'grant_type': 'client_credentials'
        }

        req = requests.post(self.pf_auth_endpoint, headers=headers, data=data)

        if req.status_code < 400:
            self.auth_token = AuthorizationToken(**req.json())
        else:
            raise Exception('Error refreshing refreshing token: %s' % req.text)

    def _execute(self, params):
        """validate data and request post
        https://pypi.python.org/pypi/requests
        Use simplejson if available.
        if raise_errors==False, the validation errors will not be raised,
        only logged; by default raise_errors=True"""
        api_url = self.api_url

        if LOG.isEnabledFor(logging.DEBUG):
            for key, param in params.items():
                LOG.debug('%s=%s', key, param)

        if self.migration_mode_enabled:
            if self.auth_token.expires_at < datetime.now():
                self._refresh_auth_token()
            headers_api = {'Authorization': f"{self.auth_token.token_type} {self.auth_token.access_token}"}
            params['MERC'] = self.pf_client_id
            api_url = self.pf_api_endpoint
        else:
            headers_api = {'X-Kount-Api-Key': self.api_key}

            if self.api_key == "API_KEY":
                raise Exception('Please configure the API Key in settings.py file')

        params['FRMT'] = 'JSON'
        LOG.debug("url=%s, headers=%s, params=%s", api_url,
                  headers_api, params)

        req = requests.post(api_url,
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


class AuthorizationToken:
    """AuthorizationToken class used to execute Kount request"""
    def __init__(self, access_token, token_type, expires_in, scope):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope
        if expires_in:
            self.expires_at = datetime.now() + timedelta(seconds=expires_in - 60) # allow for latency
        else:
            self.expires_at = datetime.now() - timedelta(seconds=10)

