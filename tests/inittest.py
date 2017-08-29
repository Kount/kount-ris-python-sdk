#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"TestKhash"
from __future__ import absolute_import, unicode_literals, division, print_function
from kount.util.khash import Khash
from kount.settings import configurationKey as iv
from kount.version import VERSION

#~ import logging
#~ logging.basicConfig()

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"
try:
    from base64 import a85decode #python3.x.y
except ImportError:
    from mom.codec.base85 import b85decode as a85decode #python2.7.13

Khash.set_iv(a85decode(iv))
