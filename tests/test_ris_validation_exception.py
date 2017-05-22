#!/usr/bin/env python
"Test Ris Response Exception"
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


import unittest
from sdkpython.util.ris_validation_exception import RisResponseException
from sdkpython.settings import error_messages

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


class TestRisResponseException(unittest.TestCase):
    "test Ris response exception"
    def test_code_301(self):
        'code 301'
        exc = RisResponseException(301)
        self.assertEqual(str(exc), 'Bad version')
        self.assertEqual(str(exc), error_messages[301])
        with self.assertRaises(RisResponseException):
            raise exc


if __name__ == "__main__":
    unittest.main()
