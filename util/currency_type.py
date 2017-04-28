#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

from util.ris_validation_exception import RisException


class CurrencyType(object):
    """Constructor for an Currency type object.
        deprecated Use three-character ISO-4217 currency code.
            @param value - string
            CurrencyType(value)
            "USD". United States Dollars
            "EUR". European currency unit
            "CAD". Canadian Dollar.
            "AUD". Austrailian Dollar
            "JPY". Japanese Yen
            "HKD". Hong Kong Dollar
            "NZD". Hong Kong Dollar
    """
    def __init__(self, value):
        valid_type_list = ["USD", "EUR", "CAD", "AUD", "JPY", "HKD", "NZD"]
        c = RisException("Expected currency type in %s, received [%s]."%(valid_type_list, value))
        try:
            value = value.strip().upper()
        except AttributeError as e:
            raise c
        if value in valid_type_list:
            self.value = value
        else:
            raise c
