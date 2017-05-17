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

from settings import resource_folder, xml_filename
import os
#~ from local_settings import url_api
xml_filename_path = os.path.join(os.path.dirname(__file__),
                            resource_folder, xml_filename)
#~ from pprint import pprint


class RisValidator(object):
    """
    RIS input data validator class.
    """

    def __init__(self):
        self.xml_to_dict1, self.required_field_names, self.notrequired_field_names = xml_to_dict(xml_filename_path)
        #~ print("self.required_field_names = ", self.required_field_names)
        #~ print("self.notrequired_field_names = ", self.notrequired_field_names)

    #~ def ris_validator(self, params, required_field_names, notrequired_field_names):
        #~ req - list with required fields, notreq - list with notrequired fields,
    def ris_validator(self, params, xml_to_dict1):
        """Client side validate the data to be passed to RIS.
        kwargs
            params - Map of data parameters from request,
            raise RisValidationException - Ris validation exception
            return List of errors encountered as util.ValidationError objects
        """
        #~ print("xml_to_dict1", xml_to_dict1)
        self.errors = []
        errors = []
        empty = []
        missing_in_xml = []
        required_err = []
        REQUIRED_FIELDS = [
            'anid', # Automatic Number Identification
            'auth', # A or D, for accept or decline
            'curr', # Country of currency submitted on order (USD)
            'emal', # Customer's email
            'ipad', # IP Address of Customer
            'mack', # Merchant's acknowledgement to ship/process the order (Y)
            'merc', # Merchant ID assigned to merchant by Kount
            'mode', # Q, P, D, U
            'ptok', # Payment token
            'ptyp', # Payment type (CARD = Credit Card)
            'sess', # Unique Session ID
            'site', # Website Identifier of where order originated
            'totl', # Total amount in currency (in pennies)
            'tran', # Kount transaction ID (required for update modes U and X)
            'vers'  # Version of Kount
            ]
        """for r in REQUIRED_FIELDS:
            if r.upper() not in params:
                required_err.append(r)
                print('required_err', r)
                raise ValidationError(r)"""
        for p in params:
            if params[p] is None:
                continue
            try:
                p_xml = xml_to_dict1[p.split("[")[0]]
            except KeyError:
                missing_in_xml.append(p)
                continue
            regex = p_xml.get('reg_ex', None)
            mode_dict = p_xml.get('mode', None)
            mode = params.get('MODE', "Q")
            if params[p] is not None and len(str(params[p])):
                empty.append(p)
                continue
            max_length = p_xml.get('max_length', None)
            if max_length:
                if int(p_xml['max_length']) < len(params[p]):
                    required_err = "max_length %s invalid for %s" % (
                        len(params[p]), p)
                    errors.append(required_err)
                    raise ValidationError(params[p], regex)
            if (regex is not None) and not re.match(regex, params[p]):
                print(333, p, regex)
                required_err = "Regex " + p_xml['reg_ex'] + " invalid for " + p
                errors.append(required_err)
                raise ValidationError(field=p, value=params[p], pattern=regex)
            if mode is not None and mode_dict is not None:
                #~ 'ANID': {'max_length': '64', 'mode': ['P'], 'required': True},
                if params[p] == "" and mode in mode_dict:
                    required_err = "Invalid parameter [%s] "\
                                   "for mode [%s]"%(p, mode)
                    errors.append(required_err)
                    raise ValidationError(p, mode)
                if params[p] != "" and mode not in mode_dict:
                    required_err = "Mode " + mode + " invalid for " + p
                    errors.append(required_err)
                    raise ValidationError(p, mode)
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
        if len(errors):
            raise RisValidationException("Validation process failed", errors)
        return errors, missing_in_xml, empty
