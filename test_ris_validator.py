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
from json_test import example_data, example_data_products
from ris_validator import RisValidator
from util.validation_error import ValidationError


class TestRisValidator(unittest.TestCase):
    def setUp(self):
       self.validator = RisValidator()

    def test_1examle_data_na(self):
        invalid, missing_in_xml, empty = self.validator.ris_validator(params=example_data_products)
        self.assertEqual(invalid, [])
        missing_in_xml.sort()
        self.assertEqual(missing_in_xml, ['FRMT', 'PTOK'])
        self.assertEqual(empty, ['ANID'])

    def test_2examle_data(self):
        invalid, missing_in_xml, empty = self.validator.ris_validator(params=example_data)
        self.assertEqual(invalid, [])
        missing_in_xml.sort()
        self.assertEqual(missing_in_xml, ['FRMT', 'PTOK'])
        self.assertEqual(empty, ['ANID'])

    def test_3examle_data_invalid(self):
        example_data_products['S2EM'] = 'sdkTestShipTo%40kountsdktestdomain.com'
        with self.assertRaises(ValidationError) as e:
            self.validator.ris_validator(params=example_data_products)
            self.assertIn("EX', 'Field [S2EM] has value ", str(e))


if __name__ == "__main__":
    unittest.main()
