#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved
"RIS initial inquiry class"
from __future__ import absolute_import, unicode_literals, division, print_function
from datetime import datetime
import time
import logging
from .request import (Request, CURRENCYTYPE, INQUIRYMODE,
                      GENDER, ADDRESS, SHIPPINGTYPESTAT)
from .util.cartitem import CartItem
from .util.address import Address
from .settings import SDK_VERSION

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


# common logger for inquiry and request
logger = logging.getLogger('kount.request')


class Inquiry(Request):
    """RIS initial inquiry class.
        Contains specific methods for setting various inquiry properties
        Class constructor. Sets the RIS mode to "Inquiry" ("Q"),
        sets currency to "USD", and sets the Python SDK identifier.
        The mode and currency can be adjusted by called
        INQUIRYMODE and CURRENCYTYPE methods respectively.
        """
    def __init__(self):
        self.params = {}
        self.version()
        self.params["SDK"] = "CUST"
        self.params["ANID"] = ""
        self.params["FRMT"] = "JSON"
        self.inquiry_mode = INQUIRYMODE.DEFAULT
        self.currency_type = CURRENCYTYPE.USD
        logger.debug('Inquiry: %s', self.params)

    def version(self):
        "SDK_Type-RIS_VERSION-SDK_BUILD_DATETIMESTAMP"
        datestr = datetime.now().strftime('%Y%m%d%H%M')
        vers = "Sdk-Ris-Python-%s-%s" % (SDK_VERSION, datestr)
        assert len(vers) == 32
        self.params["SDK_VERSION"] = vers
        logger.debug('SDK_VERSION = %s', vers)

    def cash(self, cash):
        """Set cash amount of any feasible goods.
            Arg: cash - int, cash amount of any feasible goods"""
        self.params["CASH"] = cash
        logger.debug('CASH = %s', cash)

    def date_of_birth(self, dob=datetime.today()):
        """Set the date of birth in the format YYYY-MM-DD.
         Arg: dob - Date of birth
         """
        self.params["DOB"] = dob.strftime('%Y-%m-%d')
        logger.debug('DOB = %s', dob)

    def gender_user(self, gender):
        """Set the gender. Either M(ale) of F(emale).
            Acceptable values: GENDER
            Arg: - gender"""
        if gender in GENDER:
            self.params["GENDER"] = gender
        logger.debug('GENDER = %s', gender)

    def user_defined_field(self, label, value):
        """Set a user defined field.
            Arg: label - The name of the user defined field
            Arg: value - The value of the user defined field
        """
        self.params["UDF[%s]" % label] = value
        logger.debug('UDF[%s] = %s', label, value)

    def request_mode(self, mode):
        """Set the request mode.
            Acceptable values are: INQUIRYMODE
            Arg: mode - Mode of the request
        """
        if mode in vars(INQUIRYMODE).values():
            self.params["MODE"] = mode
            logger.debug('MODE = %s', mode)
        else:
            logger.error('MODE = %s', mode)
            raise ValueError('Required MODE')

    def currency_set(self, currency):
        """Set the three character ISO-4217 currency code.
            Arg: currency - Type of currency, CURRENCYTYPE
        """
        logger.debug('CURR = %s', currency)
        self.params["CURR"] = currency

    def total_set(self, total=0):
        """Set the total amount in lowest possible denomination of currency.
            Arg: total - Transaction amount in lowest possible
            denomination of given currency
        """
        logger.debug('TOTL = %s', total)
        self.params["TOTL"] = total

    def email_client(self, email_add):
        """Set the email address of the client.
            Arg: email - Email address of the client
        """
        logger.debug('EMAL = %s', email_add)
        self.params["EMAL"] = email_add

    def customer_name(self, c_name):
        """the name of the client or company.
            Arg: c_name - Name of the client or company
         """
        logger.debug('NAME = %s', c_name)
        self.params["NAME"] = c_name

    def _address(self, adr_type, address):
        """Set the address.
            Arg: address - The billing or shipping address; type Address
            adr_type - billing or shipping, values in ['B', 'S']
        """
        assert isinstance(address, Address)
        self.params[adr_type+"2A1"] = address.address1
        self.params["%s2A2" % adr_type] = address.address2
        self.params["%s2CI" % adr_type] = address.city
        self.params["%s2ST" % adr_type] = address.state
        self.params["%s2PC" % adr_type] = address.postal_code
        self.params["%s2CC" % adr_type] = address.country
        self.params["%sPREMISE" % adr_type] = address.premise
        self.params["%sSTREET" % adr_type] = address.street

    def billing_address(self, address):
        """Set the billing address.
            Arg: address - The billing address, type Address
            Address
        """
        logger.debug("B2A1 = %s, B2A2 = %s, B2CI = %s, B2ST = %s, "
                     "B2PC = %s, B2CC = %s, BPREMISE = %s, BSTREET = %s",
                     address.address1, address.address2, address.city,
                     address.state, address.postal_code, address.country,
                     address.premise, address.street)
        self._address(ADDRESS.BILLING, address)

    def shipping_address(self, address):
        """Set the shipping address.
            Arg: address - The shipping address, type Address
        """
        logger.debug("S2A1 = %s, S2A2 = %s, S2CI = %s, S2ST = %s, "
                     "S2PC = %s, S2CC = %s, SPREMISE = %s, SSTREET = %s",
                     address.address1, address.address2, address.city,
                     address.state, address.postal_code, address.country,
                     address.premise, address.street)
        self._address(ADDRESS.SHIPPING, address)

    def billing_phone_number(self, billing_phone=""):
        """Set the billing phone number.
            Arg: billing_phone - Billing phone number
         """
        logger.debug('billing phone = %s', billing_phone)
        self.params["B2PN"] = billing_phone

    def shipping_phone_number(self, shipping_phone):
        """Set the shipping phone number.
            Arg: shipping_phone - shipping phone number
         """
        logger.debug('S2PN = %s', shipping_phone)
        self.params["S2PN"] = shipping_phone

    def shipping_name(self, ship_name=""):
        """Set the shipping name.
            Arg: ship_name - Shipping name
        """
        logger.debug('S2NM = %s', ship_name)
        self.params["S2NM"] = ship_name

    def email_shipping(self, shipping_email):
        """Set the shipping email address of the client.
            Arg: shipping_email - shipping email
        """
        logger.debug('S2EM = %s', shipping_email)
        self.params["S2EM"] = shipping_email

    def unique_customer_id(self, unique_customer):
        """Set the unique ID or cookie set by merchant.
            Arg: unique_customer - Customer-unique ID or cookie set by merchant.
        """
        logger.debug('UNIQ = %s', unique_customer)
        self.params["UNIQ"] = unique_customer

    def ip_address(self, ip_adr):
        """Set the IP address. ipaddress
        Arg: ip_adr - IP Address of the client
        """
        logger.debug('IPAD = %s', ip_adr)
        self.params["IPAD"] = str(ip_adr)

    def user_agent(self, useragent):
        """Set the user agent string of the client.
        Arg: useragent - user agent string of the client
        """
        logger.debug('UAGT = %s', useragent)
        self.params["UAGT"] = useragent

    def timestamp(self, time_stamp=int(time.time())):
        """Set the timestamp (in seconds) since the UNIX epoch
            for when the UNIQ value was set.
            Arg: time_stamp -  The timestamp
        """
        logger.debug('EPOC = %s', time_stamp)
        self.params["EPOC"] = time_stamp

    def shipment_type(self, shipment):
        """Set shipment type
            Arg: shipment -  type SHIPPINGTYPESTAT
        """
        logger.debug('SHTP = %s', shipment)
        if shipment in vars(SHIPPINGTYPESTAT):
            self.params["SHTP"] = shipment
        else:
            raise ValueError("shipment must be in SHIPPINGTYPESTAT")

    def anid(self, anid_order):
        """Set the anid
            Automatic Number Identification (ANI) submitted with order.
            If the ANI cannot be determined,
            merchant must pass 0123456789 as the ANID.
            This field is only valid for MODE=P RIS submissions.
            Arg: anid_order - Anid of the client
        """
        self.params["ANID"] = anid_order
        logger.debug('ANID = %s', anid_order)

    def company_name(self, name):
        """Set the name of the company.
        Arg: name - Name of the company
        """
        logger.debug('NAME = %s', name)
        self.params["NAME"] = name

    def website(self, web_site):
        """Set the website.
            Arg: site - the website
        """
        logger.debug('SITE = %s', web_site)
        self.params["SITE"] = web_site

    def shopping_cart(self, cart):
        """Set the shopping cart.
            Arg: cart - Cart items in the shopping cart, type Cart
        """
        for index, cart in enumerate(cart):
            assert isinstance(cart, CartItem)
            logger.debug("PROD_TYPE[%i] = %s, PROD_ITEM[%i] = %s, "
                         "PROD_DESC[%i] = %s, PROD_QUANT[%i] = %s, "
                         "PROD_PRICE[%i] = %s",
                         index, cart.product_type,
                         index, cart.item_name,
                         index, cart.description,
                         index, cart.quantity,
                         index, cart.price)
            self.params["PROD_TYPE[%i]" % index] = cart.product_type
            self.params["PROD_ITEM[%i]" % index] = cart.item_name
            self.params["PROD_DESC[%i]" % index] = cart.description
            self.params["PROD_QUANT[%i]" % index] = cart.quantity
            self.params["PROD_PRICE[%i]" % index] = cart.price
