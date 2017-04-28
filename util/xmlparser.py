#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

import os
from os.path import isfile, join
import xml.etree.ElementTree as ET
from settings import resource_folder, xml_filename


def xml_to_dict():
    xml_filename_path = os.path.join(os.path.dirname(__file__), '..',
                                                           resource_folder, xml_filename)
    if not isfile(xml_filename_path):
        raise IOError("Missing file %s ", xml_filename_path)
    with open(xml_filename_path, 'r') as valid_xml:
        tree = ET.parse(xml_filename_path)
        root = tree.getroot()
    valid_data_dict = {}
    for child in root:
        param_name = child.attrib['name']
        current = valid_data_dict[param_name] = {}
        required = child.find('required')
        if required is not None and required.findall('mode') != []:
            current["mode"] = [m.text for m in required.findall('mode')]
        reg_ex = child.find('reg_ex')
        if reg_ex is not None:
            current["reg_ex"] = reg_ex.text
        max_length = child.find('max_length')
        if max_length is not None:
            current["max_length"] = max_length.text
    assert(len(valid_data_dict.keys()) == len(root))
    return valid_data_dict
