#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""RisException
example ussage:
    exc = RisException("REQUIRED", "jjjsssssssj")
    raise exc
    raise RisException(message="REQUIRED", cause="jjjj", kwargs={})
"""

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


class RisException(Exception):
    """RIS exeption class:
            message - exception message
            cause - exception cause"""
