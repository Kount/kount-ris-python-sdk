#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""parse Kount's validation xml to python dict, used in RisValidator"""
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.

from __future__ import absolute_import, unicode_literals, division, print_function
import xml.etree.ElementTree as ET

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


def xml_to_dict(xml_filename_path):
    "parse xml to_python dict"
    with open(xml_filename_path, 'r'):
        tree = ET.parse(xml_filename_path)
        root = tree.getroot()
    valid_data_dict = {}
    required_field_names = []
    notrequired_field_names = []
    for child in root:
        param_name = child.attrib['name']
        current = valid_data_dict[param_name] = {}
        required = child.find('required')
        if required is not None:
            required_field_names.append(param_name)
            current['required'] = True
            mode_tags = required.findall('mode')
            if mode_tags != []:
                current["mode"] = [m.text for m in mode_tags]
        else:
            notrequired_field_names.append(param_name)
        reg_ex = child.find('reg_ex')
        if reg_ex is not None:
            current["reg_ex"] = reg_ex.text
        max_length = child.find('max_length')
        if max_length is not None:
            current["max_length"] = max_length.text
    assert len(valid_data_dict.keys()) == len(root)
    return valid_data_dict, required_field_names, notrequired_field_names
