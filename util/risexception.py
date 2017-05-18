#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


class RisException(Exception):
    """RIS exeption class:
            message - exception message
            cause - exception cause"""


if __name__ == "__main__":
    exc = RisException("REQUIRED", "jjjsssssssj")
    raise exc
    raise RisException(message="REQUIRED", cause="jjjj", kwargs={})
