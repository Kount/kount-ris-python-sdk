#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"class RisValidator"
import re
import os
import logging
from util.cartitem import CartItem
from util.ris_validation_exception import RisValidationException
from util.validation_error import ValidationError
from util.xmlparser import xml_to_dict
from settings import resource_folder, xml_filename
from local_settings import raise_errors as raise_err

xml_filename_path = os.path.join(
    os.path.dirname(__file__), resource_folder, xml_filename)
logger = logging.getLogger('kount.request')

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


class RisValidator(object):
    """
    RIS input data validator class.
    """

    def __init__(self, raise_errors=raise_err):
        """parse against xml file provided is sdk"""
        self.errors = []
        self.xml_2_dict, self.required_field_names,\
            self.notrequired_field_names =\
            xml_to_dict(xml_filename_path)
        self.raise_errors = raise_errors

    def ris_validator(self, params, xml_2_dict):
        """Client side validate the data to be passed to RIS.
        kwargs
            params - Map of data parameters from request,
            xml_2_dict - python dict
            raise RisValidationException - Ris validation exception
            return List of errors encountered as util.ValidationError objects
        """
        errors = []
        empty = []
        missing_in_xml = []
        required_err = []
        for param in params:
            if params[param] is None or isinstance(params[param], bool):
                continue
            try:
                p_xml = xml_2_dict[param.split("[")[0]]
            except KeyError:
                missing_in_xml.append(param)
                logger.debug("missing_in_xml = %s", param)
                continue
            try:
                regex = p_xml['reg_ex']
            except KeyError:
                regex = False
            mode_dict = p_xml.get('mode', None)
            mode = params.get('MODE', "Q")
            try:
                param_len = len(str(params[param]))
            except UnicodeEncodeError:
                param_len = len(str(params[param].encode('utf-8')))
            if params[param] is not None and param_len == 0:
                empty.append(param)
                logger.debug("empty value for %s", param)
                continue
            max_length = p_xml.get('max_length', None)
            if max_length:
                if int(p_xml['max_length']) < param_len:
                    required_err = "max_length %s invalid for %s" % (
                        param_len, param)
                    errors.append(required_err)
                    logger.debug(required_err)
            if regex and isinstance(param, str) and \
                    isinstance(params[param], str):
                if not re.match(regex, params[param]):
                    required_err = "Regex %s invalid for %s" % (
                        p_xml['reg_ex'], param)
                    errors.append(required_err)
                    logger.debug("required_err %s", required_err)
            if mode is not None and mode_dict is not None:
                if params[param] == "" and mode in mode_dict:
                    required_err = "Invalid parameter [%s] "\
                                   "for mode [%s]" % (param, mode)
                    errors.append(required_err)
                    logger.debug("required_err %s", required_err)
                    raise ValidationError(param, mode)
                if params[param] != "" and mode not in mode_dict:
                    required_err = "Mode %s invalid for %s" % (mode, param)
                    errors.append(required_err)
                    logger.debug("required_err %s", required_err)
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
                logger.debug("cart = %s", cart.to_string())
            except KeyError as kye:
                required_err = "CartItem - mandatory field missed "\
                               "%s. %s" % (cart.to_string(), kye)
                errors.append(required_err)
                logger.debug("required_err %s", required_err)
            except IndexError as ine:
                required_err = "CartItem -  %s. %s" % (cart.to_string(), ine)
                logger.debug("required_err %s", required_err)
                errors.append(required_err)
        self.errors = errors
        if len(errors) and self.raise_errors:
            raise RisValidationException("Validation process failed", errors)
        logger.debug("errors = %s, missing_in_xml = %s, empty = %s",
                     errors, missing_in_xml, empty)
        return errors, missing_in_xml, empty
