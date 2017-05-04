#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

from util.ris_validation_exception import RisException


class ShippingType(object):
    """Constructor for an Shipping type object.
            Args: value, string
            ShippingType(value)
            "SD". Same day shipping type.
            "ND". Next day shipping type.
            "2D". Second day shipping type.
            "ST". Standard shipping type.
    """
    def __init__(self, value=""):
        valid_type_list = ["SD", "ND", "2D", "ST"]
        c = RisException("Expected shipping type in %s, received [%s]."%(valid_type_list, value))
        try:
            value = value.strip().upper()
        except AttributeError as e:
            raise c
        if value in valid_type_list:
            self.value = value
        else:
            raise c
