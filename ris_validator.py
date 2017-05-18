#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
import re
import os
from util.cartitem import CartItem
from util.ris_validation_exception import RisValidationException
from util.validation_error import ValidationError
from util.xmlparser import xml_to_dict
#~ from util.risexception import RisException

from settings import resource_folder, xml_filename

from local_settings import raise_errors
xml_filename_path = os.path.join(os.path.dirname(__file__),
                            resource_folder, xml_filename)
#~ from pprint import pprint


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"



class RisValidator(object):
    """
    RIS input data validator class.
    """

    def __init__(self, raise_errors=raise_errors):
        """parse against xml file provided is sdk
        """
        self.errors = []
        self.xml_to_dict1, self.required_field_names,\
            self.notrequired_field_names =\
            xml_to_dict(xml_filename_path)
        self.raise_errors = raise_errors

    def ris_validator(self, params, xml_to_dict1):
        """Client side validate the data to be passed to RIS.
        kwargs
            params - Map of data parameters from request,
            raise RisValidationException - Ris validation exception
            return List of errors encountered as util.ValidationError objects
        """
        errors = []
        empty = []
        missing_in_xml = []
        required_err = []
        for param in params:
            if params[param] is None:
                continue
            try:
                p_xml = xml_to_dict1[param.split("[")[0]]
            except KeyError:
                missing_in_xml.append(param)
                continue
            regex = p_xml.get('reg_ex', None)
            mode_dict = p_xml.get('mode', None)
            mode = params.get('MODE', "Q")
            if params[param] is not None and len(str(params[param])) == 0:
                empty.append(param)
                continue
            max_length = p_xml.get('max_length', None)
            if max_length:
                if int(p_xml['max_length']) < len(params[param]):
                    required_err = "max_length %s invalid for %s" % (
                        len(params[param]), param)
                    errors.append(required_err)
                    #~ raise ValidationError(params[param], regex)
            if (regex is not None) and not re.match(regex, str(params[param])):
                required_err = "Regex %s invalid for %s" % (
                    p_xml['reg_ex'], param)
                errors.append(required_err)
                #~ raise ValidationError(field=param,
                                      #~ value=params[param], pattern=regex)
            if mode is not None and mode_dict is not None:
                #~ 'ANID': {'max_length': '64', 'mode': ['P'], 'required': True},
                if params[param] == "" and mode in mode_dict:
                    required_err = "Invalid parameter [%s] "\
                                   "for mode [%s]"%(param, mode)
                    errors.append(required_err)
                    raise ValidationError(param, mode)
                if params[param] != "" and mode not in mode_dict:
                     #~ 'PROD_QUANT': {'mode': ['Q', 'P', 'W'], 'reg_ex': '^[0-9]+$'},
                    required_err = "Mode %s invalid for %s" % (mode, param)
                    errors.append(required_err)
                    #~ raise ValidationError(param, mode)
        product_type = sorted(
            [cpt for cpt in params if cpt.startswith("PROD_TYPE[")])
        product_name = sorted(
            [cpt for cpt in params if cpt.startswith("PROD_ITEM[")])
        product_description = sorted(
            [cpt for cpt in params if cpt.startswith("PROD_DESC[")])
        product_quantity = sorted(
            [cpt for cpt in params if cpt.startswith("PROD_QUANT[")])
        product_price = sorted(
            [cpt for cpt in params if cpt.startswith("PROD_PRICE[")])
        # cart_items = []
        cart_items_number = max(len(product_type), len(product_name),
                                len(product_description), len(product_quantity),
                                len(product_price))
        for cin in range(cart_items_number):
            cart = CartItem()
            try:
                cart.product_type = params[product_type[cin]]
                cart.item_name = params[product_name[cin]]
                cart.description = params[product_description[cin]]
                cart.quantity = params[product_quantity[cin]]
                cart.price = params[product_price[cin]]
                # cart_items.append(c)
            except KeyError as kye:
                required_err = "CartItem - mandatory field missed "\
                               "%s. %s" % (cart.to_string(), kye)
                errors.append(required_err)
            except IndexError as ine:
                required_err = "CartItem -  %s. %s" % (cart.to_string(), ine)
                errors.append(required_err)
        self.errors = errors
        if len(errors) and self.raise_errors:
            raise RisValidationException("Validation process failed", errors)
        return errors, missing_in_xml, empty
