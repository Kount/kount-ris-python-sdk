#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

import re
from util.cartitem import CartItem
from util.ris_validation_exception import RisValidationException
from util.validation_error import ValidationError
from util.xmlparser import xml_to_dict
#~ from util.risexception import RisException
from json_test import example_data_na as example_data

from settings import resource_folder, xml_filename
import os
#~ from local_settings import url_api
xml_filename_path = os.path.join(os.path.dirname(__file__),
                            resource_folder, xml_filename)

class RisValidator(object):
    """
    RIS input data validator class.
    """

    def __init__(self):
        self.xml_to_dict1 = xml_to_dict(xml_filename_path)

    def ris_validator(self, params={}):
        """Client side validate the data to be passed to RIS.
        kwargs
            params - Map of data parameters from request, 
            raise RisValidationException - Ris validation exception 
            return List of errors encountered as util.ValidationError objects
        """
        self.errors = []
        errors = []
        for p in params:
            try:
                p_xml = self.xml_to_dict1[p.split("[")[0]]
            except KeyError as e:
                #print("===============================missing in xml - ", p)
                pass
            regex = p_xml.get('reg_ex', None)
            mode_dict = p_xml.get('mode', None)
            mode = params['MODE']
            if not len(params[p]):
                #print("empty =", params[p], p)
                continue
            max_length = p_xml.get('max_length', None)
            if max_length:
                if int(p_xml['max_length']) < len(params[p]) :
                    required_err = "max_length " + len(params[p]) + " invalid for " + p
                    errors.append(required_err)
                    raise ValidationError(params[p], regex)
            if (regex is not None) and not re.match(regex, params[p]):
                required_err = "Regex " + p_xml['reg_ex'] + " invalid for" + p
                errors.append(required_err)
                raise ValidationError(field=p, value=params[p], pattern=regex)
            if mode is not None and mode_dict is not None:
                if mode in mode_dict:
                    print("mode in mode_dict,", mode, mode_dict)
                else:
                    print("mode NNNNot in mode_dict,", mode, mode_dict)
                    required_err = "Mode " + mode + " invalid for" + p
                    errors.append(required_err)
                    raise ValidationError(p, mode)
        product_type = sorted([cpt for cpt in params if cpt.startswith("PROD_TYPE[")])
        product_name = sorted([cpt for cpt in params if cpt.startswith("PROD_ITEM[")])
        product_description = sorted([cpt for cpt in params if cpt.startswith("PROD_DESC[")])
        product_quantity = sorted([cpt for cpt in params if cpt.startswith("PROD_QUANT[")])
        product_price = sorted([cpt for cpt in params if cpt.startswith("PROD_PRICE[")])
        # cart_items = []
        cart_items_number = max(len(product_type), len(product_name), len(product_description), len(product_quantity), len(product_price))
        for ci in range(cart_items_number):
            c = CartItem()
            try:
                c.product_type = params[product_type[ci]]
                c.item_name = params[product_name[ci]]
                c.description = params[product_description[ci]]
                c.quantity = params[product_quantity[ci]]
                c.price = params[product_price[ci]]
                # cart_items.append(c)
            except KeyError as e:
                required_err = "CartItem - mandatory field missed %s. %s"%(c.to_string(), e)
                errors.append(required_err)
        #print("cart_items", [c.to_string() for c in cart_items])
        if len(errors):
            raise RisValidationException("Validation process failed", errors)
        return errors

print(RisValidator().ris_validator(params=example_data))
