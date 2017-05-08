#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

import unittest
import os
from settings import resource_folder, xml_filename
xml_filename_path = os.path.join(os.path.dirname(__file__),
                            resource_folder, xml_filename)
from util.xmlparser import xml_to_dict
#from pprint import pprint


class TestPaymentType(unittest.TestCase):
    def test_xml_to_dict(self):
        a = xml_to_dict(xml_filename_path)
        #pprint(a)
        self.assertTrue(a)

if __name__ == "__main__":
    unittest.main()
