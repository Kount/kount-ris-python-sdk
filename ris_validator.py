#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

from util.cartitem import CartItem
import re
from util.ris_validation_exception import RisValidationException
from util.validation_error import ValidationError
from util.xmlparser import xml_to_dict
from util.risexception import RisException
from json_test import example_data_na as example_data



class RisValidator(object):
    """
    RIS input data validator class.
    """

    def ris_validator(self, params={}):
        """Client side validate the data to be passed to RIS.
        kwargs
            params - Map of data parameters from request, 
            raise RisValidationException - Ris validation exception 
            return List of errors encountered as util.ValidationError objects
        """
        self.errors = []
        xml_to_dict1 = xml_to_dict()
        #print(22222222222222222222, xml_to_dict1)
        #print("--"*30, xml_to_dict1.keys())
        #print(111111111111111111111, params)
        errors = []
        for p in params:
            
            try:
                p_xml = xml_to_dict1[p.split("[")[0]]
            except KeyError as e:
                print("===============================missing in xml - ", p)
                #required_err = ValidationError(field=p, value=params[p])
                required_err = ValidationError(value=params[p])
                errors.append(required_err)
                #raise ValidationError(p)
            regex = p_xml.get('reg_ex', None)
            mode_dict = p_xml.get('mode', None)
            mode = params['MODE']
            if not len(params[p]):
                print("+++++++++++++++ empty =", params[p], p)
                continue
            max_length = p_xml.get('max_length', None)
            if max_length:
                if int(p_xml['max_length']) < len(params[p]) :
                    required_err = "max_length " + len(params[p]) + " invalid for " + p
                    errors.append(required_err)
                    raise ValidationError(name, regex)
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
        cart_items = []
        cart_items_number = max(len(product_type), len(product_name), len(product_description), len(product_quantity), len(product_price))
        for ci in range(cart_items_number):
            c = CartItem()
            c.product_type = params.get(product_type[ci], "")
            c.name = params.get(product_name[ci], "")
            c.description = params.get(product_description[ci], "")
            c.quantity = params.get(product_quantity[ci], "")
            c.price = params.get(product_price[ci], "")
            cart_items.append(c)
            if not len(c.quantity) or not len(c.price) or not len(c.name) or not len(c.product_type):
                required_err = "CartItem - mandatory field missed %s"%c.to_string()
                errors.append(required_err)
        print("cart_items", cart_items)
        if len(errors):
            raise RisValidationException("Validation process failed", errors)
        return errors


print(RisValidator().ris_validator(params=example_data))
