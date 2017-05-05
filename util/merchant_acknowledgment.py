#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


def merchant_acknowledgment(value):
    """Merchant acknowledgment types
        value - "Y". The product expects to ship.
                   "N". The product does not expect to ship.
    """
    ma_dict = {
        "N": "NO",
        "Y": "YES"
        }
    message = "required - Y or N"
    try:
        value = value.upper()
    except AttributeError:
        raise KeyError(message)
    try:
        return ma_dict[value]
    except KeyError as e:
        raise KeyError(message)
