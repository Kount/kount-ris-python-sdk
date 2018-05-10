#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""Test Xml Parser"""
import unittest
import tempfile
import os
from kount.config import SDKConfig
from kount.util.xmlparser import xml_to_dict
from kount.version import VERSION

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class TestXmlParser(unittest.TestCase):
    """Test Xml Parser"""
    maxDiff = None

    def test_xml_to_dict(self):
        """assert the new rools are parsed properly to python dict"""
        xml_file = SDKConfig.get_rules_xml_file()
        test_xml = xml_file.replace(".xml", "_test.xml")
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
        tmp = tempfile.mktemp(suffix=os.path.basename(test_xml))
        with open(xml_file, 'r') as source:
            with open(tmp, 'w') as out:
                new = source.read().replace('</ris_validation>', new_rules)
                out.write(new)
        valid_data_dict, required_field_names, \
            not_required_field_names = xml_to_dict(tmp)
        self.assertIsNotNone(valid_data_dict)
        self.assertIn("RE42", required_field_names)
        self.assertIn("NR42", not_required_field_names)
        self.assertEqual(valid_data_dict['RE42'],
                         {'mode': ['Q', 'P', 'W', 'J'],
                          'reg_ex': '^.+$', 'required': True})
        self.assertEqual(valid_data_dict['NR42'], {'max_length': '42'})
        with open(tmp, 'w') as out:
            new = new.replace("NR42", "DE42")
            out.write(new)
        valid_data_dict, required_field_names, \
            not_required_field_names = xml_to_dict(tmp)
        self.assertNotIn("NR42", not_required_field_names)
        self.assertIn("DE42", not_required_field_names)
        self.assertEqual(valid_data_dict['DE42'], {'max_length': '42'})
        os.remove(tmp)


if __name__ == "__main__":
    unittest.main()
