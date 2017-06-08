#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"settings"
from __future__ import (
    absolute_import, unicode_literals, division, print_function)
import os

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

PYTHON_VERSION = "3.6.1"
RESOURCE_FOLDER = "resources"
XML_FILENAME = 'validate.xml'
XML_DICT = 'xml_dict.py'
SDK_VERSION = "0695"

#~ raise errors or log them
RAISE_ERRORS = False
#~ RAISE_ERRORS = True

 #~ uncomment this if you'd like to get the SALT from the environment
#~ try:
    #~ SALT = os.environ['K_SALT']
#~ except KeyError:
    #~ SALT = "fake salt"

#~ put SALT in the local_settings.py and don't commit it
#~ comment this code if the SALT is an environment variable
try:
    from .local_settings import *
except ImportError:
    SALT = "fake salt"

# request's timeout
TIMEOUT = 5
