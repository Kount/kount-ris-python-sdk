#!/usr/bin/env python
"Test Ris Validator"
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.

import unittest
from json_test import example_data, example_data_products
from ris_validator import RisValidator
#~ from util.validation_error import ValidationError
from util.ris_validation_exception import RisValidationException


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


class TestRisValidator(unittest.TestCase):
    "Test Ris Validator"
    def setUp(self):
        self.validator = RisValidator(raise_errors=True)

    def test_examle_data_array(self):
        "test_examle_data_array - PROD_TYPE[0]"
        invalid, missing_in_xml, empty = self.validator.ris_validator(
            params=example_data_products,
            xml_to_dict1=self.validator.xml_to_dict1)
        self.assertEqual(invalid, [])
        missing_in_xml.sort()
        self.assertIn('PTOK', missing_in_xml)
        self.assertEqual(empty, ['ANID'])

    def test_examle_data(self):
        "example data PROD_TYPE[]"
        invalid, missing_in_xml, empty = self.validator.ris_validator(
            params=example_data,
            xml_to_dict1=self.validator.xml_to_dict1)
        self.assertEqual(invalid, [])
        missing_in_xml.sort()
        self.assertEqual(missing_in_xml, ['PTOK'])
        self.assertEqual(empty, ['ANID'])

    def test_examle_data_invalid(self):
        "invalid email"
        example = example_data_products.copy()
        bad = example['S2EM'].replace('@', '%40')
        example['S2EM'] = bad
        with self.assertRaises(RisValidationException):
            self.validator.ris_validator(
                params=example,
                xml_to_dict1=self.validator.xml_to_dict1,
                )
        try:
            self.validator.ris_validator(
                params=example,
                xml_to_dict1=self.validator.xml_to_dict1)
        except RisValidationException as vale:
            self.assertIn("Regex", str(vale))


if __name__ == "__main__":
    unittest.main()
