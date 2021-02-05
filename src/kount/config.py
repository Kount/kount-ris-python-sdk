#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.

import os

from . import resources
from .version import VERSION
from settings import CONFIGURATION_KEY, SDK_AUTHOR, SDK_MAINTAINER, MAINTAINER_EMAIL, DEFAULT_TIMEOUT

__author__ = SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDK_MAINTAINER
__email__ = MAINTAINER_EMAIL
__status__ = "Development"


class SDKConfig:

    SDK_VERSION = ""
    
    SDK_AUTHOR = __author__

    SDK_MAINTAINER = __maintainer__

    MAINTAINER_EMAIL = __email__

    STATUS = __status__
    # default behaviour for request failures
    _RAISE_ERRORS = True

    # requests timeout
    _DEFAULT_TIMEOUT = DEFAULT_TIMEOUT

    # should be set from the sdk user
    _CONFIGURATION_KEY = CONFIGURATION_KEY

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

        from .util import khash
        k = khash.Khash(config_key)
        k.verify()

