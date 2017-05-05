#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


def bankcard_reply(value):
    """bank card reply
        value - "M". There was a match.
            "N". There was not a match.
            "X". No information was available.
    """
    bankcard_dict = {
        "M": "MATCH",
        "N": "NO_MATCH",
        "X":  "UNAVAILABLE"
        }
    return bankcard_dict[value]


if __name__ == "__main__":
    assert bankcard_reply("M") == "MATCH"