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
from util.ris_validation_exception import RisResponseException
from settings import error_messages


class TestRisResponseException(unittest.TestCase):
    def setUp(self):
       pass

    def test_code_301(self):
        c = RisResponseException(301)
        #~ self.assertEqual(str(c), 'Bad version')
        self.assertEqual(str(c), error_messages[301])
        with self.assertRaises(RisResponseException):
            raise c


if __name__ == "__main__":
    unittest.main()
