#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"class RisValidator, RisException, RisValidationException RisResponseException"

import logging
import os
import re

from .util.xmlparser import xml_to_dict
from .util.cartitem import CartItem
from .util.validation_error import ValidationError
from .version import VERSION

LOG = logging.getLogger('kount.request')

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class RisValidator(object):
    """
    RIS input data validator class.
    """

    _xml_rules_cache = dict()

    def __init__(self, xml_file_path, raise_errors=False):
        """parse against xml file provided is sdk"""

        self.errors = []

        if not os.path.exists(xml_file_path):
            raise ValueError("%s not found" % xml_file_path)
        res = self._xml_rules_cache.get(xml_file_path)
        if res is None:
            res = xml_to_dict(xml_file_path)
            self._xml_rules_cache[xml_file_path] = res

        self.xml_2_dict, self.required, self.notrequired = res

        self.raise_errors = raise_errors

    def ris_validator(self, params):
        """Client side validate the data to be passed to RIS.
        kwargs
            params - Map of data parameters from request,
            xml_2_dict - python dict
            raise RisValidationException - Ris validation exception
            return List of errors encountered as util.ValidationError objects
        """
        errors = []
        if len(params) <= 1:
            required_missing = "All required fields are missing %s" % params
            LOG.debug(required_missing)
            if self.raise_errors:
                raise RisValidationException(required_missing)
        empty = []
        missing_in_xml = []
        for key, val in params.items():
            if val is None or isinstance(val, bool):
                continue
            try:
                p_xml = self.xml_2_dict[key.split("[")[0]]
            except KeyError:
                missing_in_xml.append(key)
                LOG.debug("missing_in_xml = %s", key)
                continue
            try:
                regex = p_xml['reg_ex']
            except KeyError:
                regex = False
            mode_dict = p_xml.get('mode', None)
            mode = params.get('MODE', "Q")
            try:
                param_len = len(str(val))
            except UnicodeEncodeError:
                param_len = len(str(val.encode('utf-8')))
            if val is not None and param_len == 0:
                empty.append(key)
                LOG.debug("empty value for %s", key)
                continue
            max_length = p_xml.get('max_length', None)
            if max_length:
                if int(p_xml['max_length']) < param_len:
                    required_err = "max_length %s invalid for %s" % (
                        param_len, key)
                    errors.append(required_err)
                    LOG.debug(required_err)
            try:
                param_str = str(key)
                params_param_str = str(val)
            except UnicodeEncodeError:
                param_str = str(key.encode('utf8'))
                params_param_str = str(val.encode('utf8'))
            if regex and param_str and params_param_str:
                if not re.match(regex, params_param_str):
                    required_err = "Regex %s invalid for %s" % (
                        p_xml['reg_ex'], param_str)
                    errors.append(required_err)
                    LOG.debug("required_err %s", required_err)
            if mode is not None and mode_dict is not None:
                if val == "" and mode in mode_dict:
                    required_err = "Invalid parameter [%s] "\
                                   "for mode [%s]" % (key, mode)
                    errors.append(required_err)
                    LOG.debug("required_err %s", required_err)
                    raise ValidationError(key, mode)
                if val != "" and mode not in mode_dict:
                    required_err = "Mode %s invalid for %s" % (mode, key)
                    errors.append(required_err)
                    LOG.debug("required_err %s", required_err)
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
        cart_items_number = max(len(product_type),
                                len(product_name),
                                len(product_description),
                                len(product_quantity),
                                len(product_price))
        for cin in range(cart_items_number):
            cart = CartItem()
            try:
                cart.product_type = params[product_type[cin]]
                cart.item_name = params[product_name[cin]]
                cart.description = params[product_description[cin]]
                cart.quantity = params[product_quantity[cin]]
                cart.price = params[product_price[cin]]
                LOG.debug("cart = %s", cart)
            except KeyError as kye:
                required_err = ("CartItem - mandatory field missed %s. %s" %
                                (cart, kye))
                errors.append(required_err)
                LOG.debug("required_err %s", required_err)
            except IndexError as ine:
                required_err = "CartItem -  %s. %s" % (cart, ine)
                LOG.debug("required_err %s", required_err)
                errors.append(required_err)
        self.errors = errors
        if errors and self.raise_errors:
            raise RisValidationException("Validation process failed", errors)
        LOG.debug("errors = %s, missing_in_xml = %s, empty = %s",
                  errors, missing_in_xml, empty)
        return errors, missing_in_xml, empty


ERROR_MESSAGES = {
    201: 'Missing version',
    202: 'Missing mode',
    203: 'Missing merchant ID',
    204: 'Missing session ID',
    205: 'Missing transaction ID',
    211: 'Missing currency type',
    212: 'Missing total',
    221: 'Missing email',
    222: 'Missing anid',
    231: 'Missing payment type',
    232: 'Missing card number',
    233: 'Missing check micro',
    234: 'Missing PayPal ID',
    235: 'Missing Payment Token',
    241: 'Missing IP address',
    251: 'Missing merchant acknowledgement',
    261: 'Missing post body',
    301: 'Bad version',
    302: 'Bad mode',
    303: 'Bad merchant ID',
    304: 'Bad session ID',
    305: 'Bad trasaction ID',
    311: 'Bad currency type',
    312: 'Bad total',
    321: 'Bad anid',
    331: 'Bad payment type',
    332: 'Bad card number',
    333: 'Bad check micro',
    334: 'Bad PayPal ID',
    335: 'Bad Google ID',
    336: 'Bad Bill Me Later ID',
    341: 'Bad IP address',
    351: 'Bad merchant acknowledgement',
    399: 'Bad option',
    401: 'Extra data',
    402: "Mismatched payment - type: you provided payment "
         "information in a field that did not match the payment type",
    403: 'Unnecessary anid',
    404: 'Unnecessary payment token',
    501: 'Unauthorized request',
    502: 'Unauthorized merchant',
    503: 'Unauthorized IP address',
    504: 'Unauthorized passphrase',
    601: 'System error',
    701: 'The transaction ID specified in the update was not found.'
}


class RisException(Exception):
    """RIS exeption class:
        message - exception message
        cause - exception cause"""


class RisValidationException(RisException):
    """Ris validation exception class.
        kwargs -
            message - exception message
            cause - cause
            errors - list of errors encountered.
            """
    def __init__(self, message="", errors=None, cause=""):
        # Call the base class constructor with the parameters it needs
        self.message = message
        self.errors = [] if errors is None else errors
        self.cause = cause
        super(RisValidationException, self).__init__(
            self.message, self.cause, self.errors)


class RisResponseException(RisException):
    """Response exception
        kwargs -
            exception_code - Ris exception code
    """
    def __init__(self, exception_code):
        msg = ERROR_MESSAGES.get(exception_code)
        if msg is None:
            msg = 'Unexpected error code: %s' % exception_code
        super(RisResponseException, self).__init__(msg)
        self.exception_code = exception_code
