﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2025 Kount an Equifax Company All Rights Reserved.
"Address class - representing a street address"

from kount.version import VERSION
from kount.config import SDKConfig

__author__ = SDKConfig.SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDKConfig.SDK_MAINTAINER
__email__ = SDKConfig.MAINTAINER_EMAIL
__status__ = SDKConfig.STATUS


class Address(object):
    """A class representing a street address.
       Keyword arguments:
            address1 - Address 1 (default empty string)
            address2 - Address 2 (default empty string)
            city - City (default empty string)
            state - State (default empty string)
            postal_code - Postal code (default empty string)
            country - Country (default empty string)
            premise - Premise (default empty string)
            street - Street (default empty string)
    """

    def __init__(self, address1="", address2="", city="", state="",
                 postal_code="", country="", premise="", street=""):
        """Address constructor."""
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.premise = premise
        self.street = street
