#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"settings"
from __future__ import absolute_import, unicode_literals, division, print_function


__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"

PYTHON_VERSION = "3.6.1"
RESOURCE_FOLDER = "resources"
XML_FILENAME = 'validate.xml'
XML_DICT = 'xml_rules.py'
SDK_VERSION = "0695"

#~ raise errors or log them, excl. "ValueError: Configured SALT phrase is incorrect."
#~ RAISE_ERRORS = False
RAISE_ERRORS = True


# request's timeout
TIMEOUT = 5

SALT = "fake salt"

#~ uncomment this if you'd like to get the SALT from the environment
#~ import os
#~ try:
    #~ SALT = os.environ['K_SALT']
#~ except KeyError:
    #~ print("The default fake salt set. Required actual one from Kount")

#~ put SALT in the local_settings.py and don't commit it
#~ comment this code if the SALT is an environment variable
try:
    from .local_settings import *
except ImportError as ie:
    print("The default fake salt set. Required actual one from Kount. ", ie)
