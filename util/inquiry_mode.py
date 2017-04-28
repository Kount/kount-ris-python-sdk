#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

from util.ris_validation_exception import RisException


class InquiryMode(object):
    """Constructor for an inquiry mode object.
            @param value - string
            InquiryMode(value)
            "Q". Default inquiry mode, internet order type.
            "P". Phone order type.
            "W". Kount Central Mode W - Full Inquiry [W]ith thresholds.
            "J". Kount Central Mode J - Fast Inquiry [J]ust thresholds.
    """
    def __init__(self, value="Q"):
        value = value or "Q"
        valid_mode_list = ["Q", "P", "W", "J"]
        try:
            value = value.strip().capitalize()
        except AttributeError as e:
            value = "Q"
        if value in valid_mode_list:
            self.value = value
        else:
            raise RisException("Expected mode in %s, received [%s]."%(valid_mode_list, value))
