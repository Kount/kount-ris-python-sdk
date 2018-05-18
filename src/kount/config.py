#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.

import os

from . import resources
from .version import VERSION

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class SDKConfig:
    # field validation rules
    _XML_FILENAME = os.path.join(resources.__path__[0], 'validate.xml')

    SDK_VERSION = "0695"

    # default behaviour for request failures
    _RAISE_ERRORS = True

    # requests timeout
    _DEFAULT_TIMEOUT = None

    # should be set from the sdk user
    _CONFIGURATION_KEY = None

    @classmethod
    def get_rules_xml_file(cls):
        return cls._XML_FILENAME

    @classmethod
    def get_default_timeout(cls):
        return cls._DEFAULT_TIMEOUT

    @classmethod
    def get_configuration_key(cls):
        return cls._CONFIGURATION_KEY

    @classmethod
    def get_should_raise_validation_errors(cls):
        return cls._RAISE_ERRORS

    @classmethod
    def setup(cls,
              config_key,
              default_timeout=5,
              raise_errors=True,
              xml_rules_file_name=None):
        """
        Call this method before start using the SDK
        :param config_key: mandatory parameter, configuration key provided
         by Kount
        :param default_timeout: request timeout, default value is 5 seconds
        :param raise_errors: indicate if the request should throw an exception
         in case of error, default value is True
        :param xml_rules_file_name: xml rules for validation of the request,
         should not be overwritten, unless you know what you are doing
        """

        cls._CONFIGURATION_KEY = config_key
        cls._DEFAULT_TIMEOUT = default_timeout
        cls._RAISE_ERRORS = raise_errors
        if xml_rules_file_name:
            cls._XML_FILENAME = xml_rules_file_name

        from .util import khash
        k = khash.Khash(config_key)
        k.verify()

