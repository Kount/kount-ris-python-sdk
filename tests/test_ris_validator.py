#!/usr/bin/env python
"Test Ris Validator"
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
import unittest
from kount import config
from kount.ris_validator import RisValidator
from kount.ris_validator import RisValidationException
from kount.version import VERSION

from .json_test import example_data, example_data_products

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class TestRisValidator(unittest.TestCase):
    """Test Ris Validator"""

    def setUp(self):
        conf = config.SDKConfig
        self.validator = RisValidator(
            conf.get_rules_xml_file(),
            raise_errors=conf.get_should_raise_validation_errors())

    def test_example_data_array(self):
        """test_examle_data_array - PROD_TYPE[0]"""
        invalid, missing_in_xml, empty = self.validator.ris_validator(
            params=example_data_products)
        self.assertEqual(invalid, [])
        missing_in_xml.sort()
        self.assertIn('PTOK', missing_in_xml)
        self.assertEqual(empty, ['ANID'])

    def test_example_data(self):
        """example data PROD_TYPE[]"""
        invalid, missing_in_xml, empty = self.validator.ris_validator(
            params=example_data)
        self.assertEqual(invalid, [])
        missing_in_xml.sort()
        self.assertEqual(missing_in_xml, ['PTOK'])
        self.assertEqual(empty, ['ANID'])

    def test_example_data_invalid(self):
        """invalid email"""
        example = example_data_products.copy()
        bad = example['S2EM'].replace('@', '%40')
        example['S2EM'] = bad
        with self.assertRaises(RisValidationException):
            self.validator.ris_validator(params=example)
        try:
            self.validator.ris_validator(params=example)
        except RisValidationException as vale:
            self.assertIn("Regex", str(vale))


if __name__ == "__main__":
    unittest.main()
