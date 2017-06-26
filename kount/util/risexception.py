#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""RisException
example ussage:
    exc = RisException("REQUIRED", "jjjsssssssj")
    raise exc
    raise RisException(message="REQUIRED", cause="jjjj", kwargs={})
"""
from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class RisException(Exception):
    """RIS exeption class:
            message - exception message
            cause - exception cause"""
