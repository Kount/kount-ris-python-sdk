#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""TestValidationError"""
import unittest

from kount.util.validation_error import ValidationError
from kount.version import VERSION

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class TestValidationError(unittest.TestCase):
    """TestValidationError"""

    def test_max_length(self):
        """test_max_length"""
        incorrect = "a" * 10
        lengthr = 2
        vale = ValidationError(field=incorrect, length=lengthr)
        with self.assertRaises(ValidationError):
            raise vale
        self.assertEqual('LENGTH', vale.error)
        self.assertEqual("Field [%s] has length [%s] which is longer "
                         "than the maximum of [%s]" %
                         (incorrect, len(incorrect), lengthr), vale.message)

    def test_mode(self):
        """test_mode"""
        incorrect = "a" * 10
        mode = "q"
        vale = ValidationError(field=incorrect, mode=mode)
        with self.assertRaises(ValidationError):
            raise vale
        self.assertIn('REQUIRED', vale.error)
        self.assertIn("Required field [%s] missing for mode [%s]" %
                      (incorrect, mode.upper()), str(vale))

    def test_none_field(self):
        """test_none_field"""
        with self.assertRaises(RuntimeError):
            ValidationError()

    def test_pattern(self):
        """test_pattern"""
        field = 'RFCB'
        value = "42"
        pattern = '^[RC]?$'
        vale = ValidationError(field=field, value=value, pattern=pattern)
        with self.assertRaises(ValidationError):
            raise vale
        self.assertIn('REGEX', vale.error)
        self.assertIn("Field [%s] has value [%s] which does not"
                      " match the pattern [%s]" % (field, value, pattern),
                      str(vale))


if __name__ == "__main__":
    unittest.main()
