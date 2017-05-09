#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


from datetime import datetime
import ipaddress
import time
from request import Request
#~ from request import ASTAT, BCRSTAT, MERCHANTACKNOWLEDGMENT, REFUNDCBSTAT, SHIPPINGTYPESTAT
from request import  CURRENCYTYPE, INQUIRYMODE


class Inquiry(Request):
    """RIS initial inquiry class.
        Contains specific methods for setting various inquiry properties 
        Class constructor. Sets the RIS mode to "Inquiry" ("Q"), sets currency to
        "USD", and sets the Python SDK identifier. The mode and currency can be
        adjusted by called IncuiryMode(mode) and CurrencyType(mode) methods respectively.
        """
    #~ def __init__(self):
        #~ self.params["SDK_VERSION"] = "Sdk-Ris-Python-1.0.0"
    def version(self, value):
        self.params["SDK_VERSION"] = "Sdk-Ris-Python-%s"%value

    def inquiry(self):
        self.inquiry_mode = INQUIRYMODE.DEFAULT
        self.currency_type = CURRENCYTYPE.USD

    def cash(self, cash=0):
        """Set cash amount of any feasible goods.
            Arg: cash - int, cash amount of any feasible goods"""
        self.cash = cash

    def date_of_birth(self, dob=datetime.today()):
        """Set the date of birth in the format YYYY-MM-DD.
         Arg: dob - Date of birth
         """
        self.params["DOB"] = dob.strftime('%Y-%m-%d')

    def gender_user(self, gender="M"):
        """Set the gender. Either M(ale) of F(emale).
            Acceptable values: 'M' or 'F'
            Arg: - gender"""
        self.params["GENDER"] = gender

    def user_defined_field(self, label, value):
        """Set a user defined field.
            Arg: label - The name of the user defined field
            Arg: value - The value of the user defined field
        """
        self.params["UDF[%s]"%label] = value

    def request_mode(self, mode):
        """Set the request mode.
            Acceptable values are: "Q", "P", "W", "J"
            Arg: mode - Mode of the request
        """
        self.params["MODE"] = mode

    def currency_set(self, currency):
        """Set the three character ISO-4217 currency code.
            Arg: currency - Type of currency, eg, USD, EUR...
        """
        self.params["CURR"] = currency

    def total_set(self, total=0):
        """Set the total amount in lowest possible denomination of currency.
            Arg: total - Transaction amount in lowest possible denomination of given currency
        """
        self.params["TOTL"] = total

    def email_client(self, email_add):
        """Set the email address of the client.
            Arg: email - Email address of the client
        """
        self.params["EMAL"] = email_add

    def customer_name(self, c_name):
        """the name of the client or company.
            Arg: c_name - Name of the client or company
         """
        self.params["NAME"] = c_name

    def _address(self, adr_type, address):
        """Set the address.
            Arg: address - The billing or shipping address
            adr_type - billing or shipping, values in ['B', 'S']
        """
        if adr_type not in 'BS':
            raise ValueError("address type must be B or S.")
        self.params[adr_type+"2A1"] = address.address1
        self.params["%s2A2"%adr_type] = address.address2
        self.params["%s2CI"%adr_type] = address.city
        self.params["%s2ST"%adr_type] = address.state
        self.params["%s2PC"%adr_type] = address.postal_code
        self.params["%s2CC"%adr_type] = address.country
        self.params["%sPREMISE"%adr_type] = address.premise
        self.params["%sSTREET"%adr_type] = address.street

    def billing_address(self, address):
        """Set the billing address.
            Arg: address - The billing address
            address1="", address2="", city="", state="", postal_code="", country="", premise="", street=""
        """
        self._address('B', address)

    def shipping_address(self, address):
        """Set the shipping address.
            Arg: address - The shipping address
        """
        self._address('S', address)
        
    def billing_phone_number(self, billing_phone=""):
        """Set the billing phone number.
            Arg: billing_phone - Billing phone number
         """
        self.params["B2PN"] = billing_phone

    def shipping_phone_number(self, shipping_phone=""):
        """Set the shipping phone number.
            Arg: shipping_phone - shipping phone number
         """
        self.params["S2PN"] = shipping_phone

    def shipping_name(self, ship_name=""):
        """Set the shipping name.
            Arg: ship_name - Shipping name
        """
        self.params["S2NM"] = ship_name

    def email_shipping(self, shipping_email=""):
        """Set the shipping email address of the client.
            Arg: shipping_email - shipping email
        """
        self.params["S2EM"] = shipping_email

    def unique_customer_id(self, unique_customer):
        """Set the unique ID or cookie set by merchant.
            Arg: unique_customer - Customer-unique ID or cookie set by merchant.
        """
        self.params["UNIQ"] = unique_customer

    def ip_address(self, ip_adr = ""):
        """Set the IP address.
        Arg: ip_adr - IP Address of the client
        """
        self.params["IPAD"] = str(ipaddress.IPv4Address(ip_adr))

    def user_agent(self, useragent = ""):
        """Set the user agent string of the client.
        Arg: useragent - user agent string of the client
        """
        self.params["UAGT"] = useragent

    def timestamp(self, time_stamp = int(time.time())):
        """Set the timestamp (in seconds) since the UNIX epoch for when the UNIQ value was set.
            Arg: time_stamp -  The timestamp
        """
        self.params["EPOC"] = time_stamp

    def shipment_type(self, shipment = ""):
        """Set shipment type
            Arg: shipment -  Ship type
            Accepted values: "SD" - Same Day, "ND" - Next Day, "2D" - Second Day, "ST" - Standard
        """
        self.params["SHTP"] = shipment

    def anid(self, anid_order=""):
        """Set the anid
            Automatic Number Identification (ANI) submitted with order. If the ANI cannot be determined, 
            merchant must pass 0123456789 as the ANID. This field is only valid for MODE=P RIS submissions.
            Arg: anid_order - Anid of the client
        """
        self.params.put("ANID", anid_order);

    def company_name(self, name):
        """Set the name of the company.
        Arg: name - Name of the company
        """
        self.params["NAME"] = name

    def website(self, web_site):
        """Set the website.
            Arg: site - the website
        """
        self.params["SITE"] = web_site

    def shopping_cart(self, cart):
        """Set the shopping cart.
            Arg: cart - Cart items in the shopping cart
        """
        for index, c in enumerate(cart):
            self.params["PROD_TYPE[%i]"%index] = c.product_type
            self.params["PROD_ITEM[%i]"%index] = c.item_name
            self.params["PROD_DESC[%i]"%index] = c.description
            self.params["PROD_QUANT[%i]"%index] = c.quantity
            self.params["PROD_PRICE[%i]"%index] = c.price
