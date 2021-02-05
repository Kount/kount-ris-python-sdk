#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved
"""RIS initial inquiry class"""
import time

import ipaddress
import logging
from datetime import datetime

from .config import SDKConfig
from .request import (Request, CurrencyType, InquiryMode,
                      Gender, AddressType, ShippingType)
from .util.address import Address
from .util.cartitem import CartItem
from .version import VERSION

__author__ = SDKConfig.SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDKConfig.SDK_MAINTAINER
__email__ = SDKConfig.MAINTAINER_EMAIL
__status__ = SDKConfig.STATUS


# common logger for inquiry and request
LOG = logging.getLogger('kount.request')


class Inquiry(Request):
    """RIS initial inquiry class.
        Contains specific methods for setting various inquiry properties
        Class constructor. Sets the RIS mode to "Inquiry" ("Q"),
        sets currency to "USD", and sets the Python SDK identifier.
        The mode and currency can be adjusted by called
        InquiryMode and CurrencyType methods respectively.
        """
    def __init__(self):
        super(Inquiry, self).__init__()
        self.version()
        self.params["SDK"] = "CUST"
        self.params["ANID"] = ""
        self.params["FRMT"] = "JSON"
        self.params["VERS"] = SDKConfig.SDK_VERSION
        self.inquiry_mode = InquiryMode.DEFAULT
        self.currency_type = CurrencyType.USD
        LOG.debug('Inquiry: %s', self.params)

    def version(self):
        """SDK_Type-RIS_VERSION-SDK_BUILD_DATETIMESTAMP"""
        datestr = datetime.now().strftime('%Y%m%d%H%M')
        vers = "Sdk-Ris-Python-%s-%s" % (SDKConfig.SDK_VERSION, datestr)
        assert len(vers) == 32
        self.set_param("SDK_VERSION", vers)

    def set_cash(self, cash):
        """Set cash amount of any feasible goods.
            Arg: cash - int, cash amount of any feasible goods"""
        self.set_param("CASH", cash)

    def set_date_of_birth(self, dob):
        """Set the date of birth in the format YYYY-MM-DD.
         Arg: dob - Date of birth
         """
        self.set_param("DOB", dob)

    def set_gender(self, gender):
        """Set the gender. Either M(ale) of F(emale).
            Acceptable values: GENDER
            Arg: - gender"""
    
        self.set_param("GENDER", gender)

    def set_user_defined_field(self, label, value):
        """Set a user defined field.
            Arg: label - The name of the user defined field
            Arg: value - The value of the user defined field
        """
        self.set_param("UDF[%s]" % label, value)

    def set_request_mode(self, mode):
        """Set the request mode.
            Acceptable values are: InquiryMode
            Arg: mode - Mode of the request
        """
        self.set_param("MODE", mode)
    

    def set_currency(self, currency):
        """Set the three character ISO-4217 currency code.
            Arg: currency - Type of currency, CurrencyType
        """
        self.set_param("CURR", currency)

    def set_total(self, total=0):
        """Set the total amount in lowest possible denomination of currency.
            Arg: total - Transaction amount in lowest possible
            denomination of given currency
        """
        self.set_param("TOTL", total)

    def set_email_client(self, email_addr):
        """Set the email address of the client.
            Arg: email - Email address of the client
        """
        self.set_param("EMAL", email_addr)

    def set_customer_name(self, c_name):
        """the name of the client or company.
            Arg: c_name - Name of the client or company
         """
        self.set_param("NAME", c_name)

    def _address(self, adr_type, address):
        """Set the address.
            Arg: address - The billing or shipping address; type Address
            adr_type - billing or shipping, values in ['B', 'S']
        """
        if not isinstance(address, Address):
            raise ValueError
        self.params[adr_type + "2A1"] = address.address1
        self.params["%s2A2" % adr_type] = address.address2
        self.params["%s2CI" % adr_type] = address.city
        self.params["%s2ST" % adr_type] = address.state
        self.params["%s2PC" % adr_type] = address.postal_code
        self.params["%s2CC" % adr_type] = address.country
        self.params["%sPREMISE" % adr_type] = address.premise
        self.params["%sSTREET" % adr_type] = address.street

    def set_billing_address(self, address):
        """Set the billing address.
            Arg: address - The billing address, type Address
            Address
        """
        LOG.debug("B2A1 = %s, B2A2 = %s, B2CI = %s, B2ST = %s, "
                  "B2PC = %s, B2CC = %s, BPREMISE = %s, BSTREET = %s",
                  address.address1, address.address2, address.city,
                  address.state, address.postal_code, address.country,
                  address.premise, address.street)
        self._address(AddressType.BILLING, address)

    def set_shipping_address(self, address):
        """Set the shipping address.
            Arg: address - The shipping address, type Address
        """
        LOG.debug("S2A1 = %s, S2A2 = %s, S2CI = %s, S2ST = %s, "
                  "S2PC = %s, S2CC = %s, SPREMISE = %s, SSTREET = %s",
                  address.address1, address.address2, address.city,
                  address.state, address.postal_code, address.country,
                  address.premise, address.street)
        self._address(AddressType.SHIPPING, address)

    def set_billing_phone_number(self, billing_phone=""):
        """Set the billing phone number.
            Arg: billing_phone - Billing phone number
         """
        self.set_param("B2PN", billing_phone)

    def set_shipping_phone_number(self, shipping_phone):
        """Set the shipping phone number.
            Arg: shipping_phone - shipping phone number
         """
        self.set_param("S2PN", shipping_phone)

    def set_shipping_name(self, ship_name=""):
        """Set the shipping name.
            Arg: ship_name - Shipping name
        """
        self.set_param("S2NM", ship_name)

    def set_email_shipping(self, shipping_email):
        """Set the shipping email address of the client.
            Arg: shipping_email - shipping email
        """
        self.set_param("S2EM", shipping_email)

    def set_unique_customer_id(self, unique_customer):
        """Set the unique ID or cookie set by merchant.
           Arg: unique_customer - Customer-unique ID or cookie set by merchant.
        """
        self.set_param("UNIQ", unique_customer)

    def set_ip_address(self, ip_adr):
        """Set the IP address. ipaddress
        Arg: ip_adr - IP Address of the client
        """
        ipaddress.ip_address(ip_adr)
        self.set_param("IPAD", ip_adr)

    def set_user_agent(self, useragent):
        """Set the user agent string of the client.
        Arg: useragent - user agent string of the client
        """
        self.set_param("UAGT", useragent)

    def set_timestamp(self, time_stamp=None):
        """Set the timestamp (in seconds) since the UNIX epoch
            for when the UNIQ value was set.
            Arg: time_stamp -  The timestamp
        """
        if time_stamp is None:
            time_stamp = time.time()
        self.set_param("EPOC", time_stamp)

    def set_shipment_type(self, shipment):
        """Set shipment type
            Arg: shipment -  type ShippingType
        """

        self.set_param("SHTP", shipment)

    def set_anid(self, anid_order):
        """Set the anid
            Automatic Number Identification (ANI) submitted with order.
            If the ANI cannot be determined,
            merchant must pass 0123456789 as the ANID.
            This field is only valid for MODE=P RIS submissions.
            Arg: anid_order - Anid of the client
        """
        self.set_param("ANID", anid_order)

    def set_company_name(self, name):
        """Set the name of the company.
        Arg: name - Name of the company
        """
        self.set_param("NAME", name)

    def set_website(self, web_site):
        """Set the website.
            Arg: site - the website
        """
        self.set_param("SITE", web_site)

    def set_shopping_cart(self, cart):
        """Set the shopping cart.
            Arg: cart - Cart items in the shopping cart, type Cart
        """
        for index, item in enumerate(cart):
            if not isinstance(item, CartItem):
                raise ValueError('Invalid cart item: %s', % item)
                LOG.debug("PROD_TYPE[%i] = %s, PROD_ITEM[%i] = %s, "
                      "PROD_DESC[%i] = %s, PROD_QUANT[%i] = %s, "
                      "PROD_PRICE[%i] = %s",
                      index, item.product_type,
                      index, item.item_name,
                      index, item.description,
                      index, item.quantity,
                      index, item.price)

            self.params["PROD_TYPE[%i]" % index] = item.product_type
            self.params["PROD_ITEM[%i]" % index] = item.item_name
            self.params["PROD_DESC[%i]" % index] = item.description
            self.params["PROD_QUANT[%i]" % index] = item.quantity
            self.params["PROD_PRICE[%i]" % index] = item.price
