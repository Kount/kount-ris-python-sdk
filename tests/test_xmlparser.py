#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"Test Xml Parser"
from __future__ import absolute_import, unicode_literals, division, print_function
import unittest
import os
from kount.settings import RESOURCE_FOLDER, XML_FILENAME
from kount.util.xmlparser import xml_to_dict

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"

XML_FILENAME_PATH = os.path.join(os.path.dirname(__file__), '..',
                                 RESOURCE_FOLDER, XML_FILENAME)


class TestXmlParser(unittest.TestCase):
    "Test Xml Parser"
    maxDiff = None

    def test_xml_to_dict(self):
        "assert the new rools are parsed properly to python dict"
        test_xml = XML_FILENAME_PATH.replace(".xml", "_test.xml")
        new_rules = """<param name="RE42">
                        <required>
                          <mode>Q</mode>
                          <mode>P</mode>
                          <mode>W</mode>
                          <mode>J</mode>
                        </required>
                        <reg_ex>^.+$</reg_ex>
                       </param>
                       <param name="NR42">
                        <max_length>42</max_length>
                       </param>
                       </ris_validation>"""
        with open(XML_FILENAME_PATH, 'r') as source:
            with open(test_xml, 'w') as fp:
                new = source.read().replace('</ris_validation>', new_rules)
                fp.write(new)
        valid_data_dict, required_field_names, \
            notrequired_field_names = xml_to_dict(test_xml)
        self.assertIsNotNone(valid_data_dict)
        self.assertIn("RE42", required_field_names)
        self.assertIn("NR42", notrequired_field_names)
        self.assertEqual(valid_data_dict['RE42'],
                 {'mode': ['Q', 'P', 'W', 'J'],
                  'reg_ex': '^.+$', 'required': True})
        self.assertEqual(valid_data_dict['NR42'], {'max_length': '42'})
        with open(test_xml, 'w') as fp:
            new = new.replace("NR42", "DE42")
            fp.write(new)
        valid_data_dict, required_field_names, \
            notrequired_field_names = xml_to_dict(test_xml)
        self.assertNotIn("NR42", notrequired_field_names)
        self.assertIn("DE42", notrequired_field_names)
        self.assertEqual(valid_data_dict['DE42'], {'max_length': '42'})
        os.remove(test_xml)


if __name__ == "__main__":
    unittest.main()
