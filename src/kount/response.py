#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
import logging
from collections import namedtuple

from .version import VERSION
from .config import SDKConfig

__author__ = SDKConfig.SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDKConfig.SDK_MAINTAINER
__email__ = SDKConfig.MAINTAINER_EMAIL
__status__ = SDKConfig.STATUS

LOG = logging.getLogger('kount.response')

KcEvent = namedtuple('KcEvent', 'decision expression code')


class Response(object):
    """RIS response data class."""
    def __init__(self, params):
        """Constructor for a response object that accepts a map of response data
        Arg - params - Response parameters:

        "VERS" -  Get the version number.
        "MODE"
        "MERC" - merchant id
        "SESS" - session id.
        "TRAN" - Get the transaction id.
        "ORDR" -Get the merchant order number.
        "ERRO" - Get a possible error code.
        "AUTO" - Get the RIS auto response (A/R/D).
        "REASON_CODE" - Get the RIS reason for the response.
        "SCOR" - Get the Kount score.
        "OMNISCORE" - Get the Kount Omniscore.
        "GEOX" - Get the geox.
        "BRND" - Get the credit card brand.
        "VELO" - Get the 6 hour velocity.
        "VMAX" - Get the 6 week velocity.
        "NETW" - Get the network type.
        "KYCF" - Get the know your customer flag.
        "REGN" - Get the region the remote device is located in.
        "KAPT" - Get the Kaptcha flag: enabled upon request and for
                 when RIS has no
        "SITE" - Get the site ID.
        "PROXY" - Get a string representing whether the remote device is
            using a proxy. return "Y" or "N"
        "EMAILS" - Get the number of transactions associated with the email.
        "HTTP_COUNTRY" - Get the two character country code setting in
                         the remote device's
        "TIMEZONE"- Get a string representing the time zone of the customer
                    as a 3 digit
        "CARDS" - Get the number of transactions associated with the credit card
        "PC_REMOTE" - Get a string representing whether the end device is a
            remotely controlled, return "Y" or "N"
        "DEVICES" - Get the number of transactions associated with the
            particular device.
        "DEVICE_LAYERS" - Get a string representing the five layers
            (OS, SSL, HTTP, Flash, JavaScript) of the remote device.
        "MOBILE_FORWARDER" - Get the mobile device's wireless appl. protocol.
        "VOICE_DEVICE" - Get a string representing whether or not the remote
            device is voice controlled. return "Y" or "N"
        "LOCALTIME" - Get local time of the remote device in the YYYY-MM-DD.
        "MOBILE_TYPE" - Get the mobile device type.
        "FINGERPRINT" - Get the device finger print.
        "FLASH" - Get a string representing whether or not the remote device
            allows flash. return "Y" or "N"
        "LANGUAGE" - Get the language setting on the remote device.
        "COUNTRY" - Get the remote device's country of origin as a 2 characters
        "JAVASCRIPT" - Get a string representing whether the remote device
            allows JavaScript. return "Y" or "N"
        "COOKIES" - Get a string representing whether the remote device allows
            cookies. return "Y" or "N"
        "MOBILE_DEVICE" - Get a string representing whether the remote device
            is a mobile device. return "Y" or "N"
        "PIP_IPAD" - Get pierced IP address.
        "PIP_LAT" - Get latitude of pierced IP address.
        "PIP_LON" - Get longitude of pierced IP address.
        "PIP_COUNTRY" - Get country of pierced IP address.
        "PIP_REGION" - Get region of pierced IP address.
        "PIP_CITY" - Get city of pierced IP address.
        "PIP_ORG" - Get organization of pierced IP address.
        "IP_IPAD" - Get proxy IP address.
        "IP_LAT" - Get latitude of proxy IP address.
        "IP_LON" - Get longitude of proxy IP address.
        "IP_COUNTRY" - Get country of proxy IP address.
        "IP_REGION" - Get region of proxy IP address.
        "IP_CITY" - Get city of proxy IP address.
        "IP_ORG" - Get organization of proxy IP address.
        "DDFS" - Get date device first seen.
        "UAS" - Get user agent string.
        "DSR" - Get device screen resolution.
        "OS" - Get operating system (derived from user agent string).
        "BROWSER" - Get browser (derived from user agent string).
        "KC_CUSTOMER_ID" - Get the Kount Central Customer ID.
        "KC_DECISION" - Get the Kount Central Decision.
        "KC_WARNING_COUNT" - Get the number of KC warnings associated with
                             the response.
        "KC_ERROR_COUNT" - Get the number of KC errors associated
                            with the response.
        "KC_TRIGGERED_COUNT" - Get the number of KC events associated
                                with the response.
        "COUNTERS_TRIGGERED" - Get the number of rules counters triggered
                                in the response.
        "MASTERCARD" - Get MasterCard Fraud Score associated
                        with the RIS transaction.
            Please contact your Kount representative to enable support for this
            feature in your merchant account.
        "RULES_TRIGGERED" - A RIS response will always contain the field
                            RULES_TRIGGERED which will be set to zero
                            if there are no rules triggered.
        "WARNING_COUNT" - Get the number of warnings associated
                            with the response.
        "ERROR_COUNT" - Get the number of errors associated with the response.
        """
        self.params = params
        LOG.debug("RIS response init = %s", params)

    def get_kc_warnings(self):
        """Get an List of the KC warnings returned by this Response."""
        warnings = []
        for i in range(int(self.params.get("KC_WARNING_COUNT", 0))):
            warn = self.params.get("KC_WARNING_%s" % i)
            if warn:
                warnings.append(warn)
        LOG.debug("RIS get_kc_warnings = %s", warnings)
        return warnings

    def get_kc_errors(self):
        """get kc errors"""
        errors = []
        for i in range(int(self.params.get("KC_ERROR_COUNT", 0))):
            err = self.params.get("KC_ERROR_%s" % i)
            if err:
                errors.append(err)
        LOG.debug("RIS get_kc_errors = %s", errors)
        return errors

    def get_kc_events(self):
        """Get an ArrayList of the KC events returned by this Response."""
        events = []
        for i in range(int(self.params.get("KC_TRIGGERED_COUNT", 0))):
            idx = i + 1
            decision = self.params.get("KC_EVENT_%s_DECISION" % idx)
            expression = self.params.get("KC_EVENT_%s_EXPRESSION" % idx)
            code = self.params.get("KC_EVENT_%s_CODE" % idx)
            events.append(KcEvent(decision, expression, code))
        LOG.debug("RIS get_kc_events = %s", events)
        return events

    def get_kc_decision(self):
        return self.params.get('KC_DECISION')

    def get_rules_triggered(self):
        """Get a Map of the rules triggered by this Response."""
        rules = {}
        rules_triggered_count = int(self.params.get("RULES_TRIGGERED", 0))
        for i in range(rules_triggered_count):
            rule_id = self.params["RULE_ID_%s" % i]
            rules[rule_id] = self.params["RULE_DESCRIPTION_%s" % i]
        LOG.debug("RIS get_rules_triggered = %s", rules)
        return rules

    def get_session_id(self):
        """ Get the session id. """
        return self.params.get('SESS')

    def get_transaction_id(self):
        """ Get the transaction id. """
        return self.params.get('TRAN')

    def get_order_id(self):
        """ Get the merchant order number. """
        return self.params.get('ORDR')

    def get_mode(self):
        """ Get the mode. """
        return self.params.get('MODE')

    def get_auto(self):
        """ Get the RIS auto response (A/R/D). """
        return self.params.get('AUTO')

    def get_velo(self):
        """ Get the 6 hour velocity. """
        return self.params.get('VELO')

    def get_vmax(self):
        """ Get the 6 week velocity. """
        return self.params.get('VMAX')

    def get_reason_code(self):
        """ Get the merchant defined decision reason code. """
        return self.params.get("REASON_CODE")

    def get_score(self):
        """ Get the Kount score. """
        return self.params.get('SCOR')

    def getOmniscore(self):
        """ Get the Kount Omni Score"""
        return self.params.get('OMNISCORE')

    def get_geox(self):
        """ Get the geox. """
        return self.params.get('GEOX')

    def get_brand(self):
        """ Get the credit card brand."""
        return self.params.get('BRND')

    def get_network(self):
        """ Get the network type."""
        return self.params.get('NETW')

    def get_know_your_customer(self):
        """ Get the know your customer flag."""
        return self.params.get('KYCF')

    def get_region(self):
        """ Get the region the remote device is located in"""
        return self.params.get('REGN')

    def get_kaptcha(self):
        """ Get the Kaptcha flag: enabled upon request and for when RIS has
          no record. """
        return self.params.get("KAPT")

    def get_site(self):
        """ Get the site ID. """
        return self.params.get("SITE")

    def get_proxy(self):
        """ Get a string representing whether the remote device is using a
        proxy.
        :return: "Y" or "N"
        """
        return self.params.get("PROXY")

    def get_mails(self):
        """ Get the number of transactions associated with the email.
         :return Number of emails
         """
        return self.params.get("EMAILS")

    def get_http_country(self):
        """ Get the two character country code setting in the remote device's
         browser.

         :return Country
         """
        return self.params.get("HTTP_COUNTRY")

    def get_time_zone(self):
        """ Get a string representing the time zone of the customer
        as a 3 digit * number.
         :return Time zone
         """
        return self.params.get("TIMEZONE")

    def get_cards(self):
        """ Get the number of transactions associated with the credit card.

         :return Number of cards
         """
        return self.params.get("CARDS")

    def get_pc_remote(self):
        """ Get a string representing whether the end device is a remotely
         controlled computer.
         :returns "Y" or "N"
         """
        return self.params.get("PC_REMOTE")

    def get_devices(self):
        """ Get the number of transactions associated with the particular
         device.
         :return Number of devices
         """
        return self.params.get("DEVICES")

    def get_device_layers(self):
        """ Get a string representing the five layers (Operating System, SSL,
          HTTP, Flash, JavaScript) of the remote device.
         :return Device layers
         """
        return self.params.get("DEVICE_LAYERS")

    def get_mobile_forwarder(self):
        """ Get the mobile device's wireless application protocol.

         :return protocol
         """
        return self.params.get("MOBILE_FORWARDER")

    def get_voice_device(self):
        """ Get a string representing whether or not the remote device is
         voice controlled.
         :return "Y" or "N"
         """
        return self.params.get("VOICE_DEVICE")

    def get_local_time(self):
        """ Get local time of the remote device in the YYYY-MM-DD format.
         :return Local time
         """
        return self.params.get("LOCALTIME")

    def get_mobile_type(self):
        """ Get the mobile device type.
         :return Mobile type
         """
        return self.params.get("MOBILE_TYPE")

    def get_finger_print(self):
        """ * Get the device finger print.
         :return Finger print
        """
        return self.params.get("FINGERPRINT")

    def get_flash(self):
        """ * Get a string representing whether or not the remote device
        allows flash.
        :return "Y" or "N"
        """
        return self.params.get("FLASH")

    def get_language(self):
        """ Get the language setting on the remote device.
         :return Language
         """
        return self.params.get("LANGUAGE")

    def get_country(self):
        """ Get the remote device's country of origin as a two character code.
         :return Country
         """
        return self.params.get("COUNTRY")

    def get_java_script(self):
        """ Get a string representing whether the remote device allows
        JavaScript.
        :return "Y" or "N"
        """
        return self.params.get("JAVASCRIPT")

    def get_cookies(self):
        """ Get a string representing whether the remote device allows cookies.
        :return "Y" or "N"
        """
        return self.params.get("COOKIES")

    def get_mobile_device(self):
        """Get a string representing whether the remote device is a
        mobile device.
         :return "Y" or "N"
         """
        return self.params.get("MOBILE_DEVICE")

    def get_pierced_ip_address(self):
        """ Get pierced IP address.
         :return Pierced IP address
         """
        return self.params.get("PIP_IPAD")

    def get_pierced_ip_address_latitude(self):
        """ Get latitude of pierced IP address.
         :return Latitude of pierced IP address
         """
        return self.params.get("PIP_LAT")

    def get_pierced_ip_address_longitude(self):
        """ Get longitude of pierced IP address.
         :return Longitude of pierced IP address
         """
        return self.params.get("PIP_LON")

    def get_pierced_ip_address_country(self):
        """ Get country of pierced IP address.
         :return Country of pierced IP address
         """
        return self.params.get("PIP_COUNTRY")

    def get_pierced_ip_address_region(self):
        """ Get region of pierced IP address.
         :return Region of pierced IP address
         """
        return self.params.get("PIP_REGION")

    def get_pierced_ip_address_city(self):
        """ * Get city of pierced IP address.
         :return City of pierced IP address
         """
        return self.params.get("PIP_CITY")

    def get_pierced_ip_address_organization(self):
        """ Get organization of pierced IP address.
         :return Organization of pierced IP address
         """
        return self.params.get("PIP_ORG")

    def get_ip_address(self):
        """ Get proxy IP address.
         :return Proxy IP address
         """
        return self.params.get("IP_IPAD")

    def get_ip_address_latitude(self):
        """ Get latitude of proxy IP address.
         :return Latitude of proxy IP address
         """
        return self.params.get("IP_LAT")

    def get_ip_address_longitude(self):
        """ Get longitude of proxy IP address.
         :return Longitude of proxy IP address
         """
        return self.params.get("IP_LON")

    def get_ip_address_country(self):
        """ Get country of proxy IP address.
         :return Country of proxy IP address
         """
        return self.params.get("IP_COUNTRY")

    def get_ip_address_region(self):
        """ Get region of proxy IP address.
         :return Region of proxy IP address
         """
        return self.params.get("IP_REGION")

    def get_ip_address_city(self):
        """ Get city of proxy IP address.
         :return City of proxy IP address
         """
        return self.params.get("IP_CITY")

    def get_ip_address_organization(self):
        """Get organization of proxy IP address.
         :return Organization of proxy IP address
         """
        return self.params.get("IP_ORG")

    def get_date_device_first_seen(self):
        """ Get date device first seen.
         :return Date device first seen
         """
        return self.params.get("DDFS")

    def get_user_agent_string(self):
        """ Get user agent string.
         :return User agent string
         """
        return self.params.get("UAS")

    def get_device_screen_resolution(self):
        """ Get device screen resolution.
        :return Device screen resolution (HxW - Height by Width)
        """
        return self.params.get("DSR")

    def get_os(self):
        """ Get operating system (derived from user agent string).
        :return OS (operating system)
        """
        return self.params.get("OS")

    def get_browser(self):
        """ Get browser (derived from user agent string).
         :return Browser
         """
        return self.params.get("BROWSER")

    def get_kc_customer_id(self):
        """ Get the Kount Central Customer ID.
         :return String KC Id
         """
        return self.params.get("KC_CUSTOMER_ID")

    def get_warnings(self):
        """get_warnings"""
        warnings = []
        for i in range(int(self.params.get("WARNING_COUNT", 0))):
            warnings.append(self.params["WARNING_%s" % i])
        LOG.debug("RIS get_warnings = %s", warnings)
        return warnings

    def get_error_code(self):
        """ Get a possible error code."""
        return self.params.get('ERRO')

    def get_errors(self):
        """Get an ArrayList of errors associated with the response."""
        errors = []
        error_count = int(self.params.get("ERROR_COUNT", 0))
        for i in range(error_count):
            errors.append(self.params["ERROR_%s" % i])
        LOG.debug("RIS get_errors= %s", errors)
        return errors

    def get_lexis_nexis_cbd_attributes(self):
        """Get LexisNexis Chargeback Defender attribute data
        associated with the RIS
        transaction. Please contact your Kount representative to enable support
        for this feature in your merchant account.
        return Map of attributes where the keys are the attribute names and the
        values are the attribute values."""
        cbd = self.get_prefixed_response_data_map("CBD_")
        LOG.debug("get_lexis_nexis_cbd_attributes = %s", cbd)
        return cbd

    def get_lexis_nexis_instant_id_attributes(self):
        """Get LexisNexis Instant ID attributes associated with the
        RIS transaction.
        Please contact your Kount representative to enable support for this
        feature in your merchant account.
        return Map of attributes where the keys are the attribute names and the
        values are the attribute values."""
        instand_id = self.get_prefixed_response_data_map("INSTANTID_")
        LOG.debug("get_lexis_nexis_instand_id_attributes = %s", instand_id)
        return instand_id

    def get_mastercard_fraud_score(self):
        """ Get MasterCard Fraud Score associated with the RIS transaction.
        Please contact your Kount representative to enable support for this
        feature in your merchant account. """
        score = self.params.get('MASTERCARD')
        LOG.debug("get_mastercard_fraud_score = %s", score)
        return score

    def get_prefixed_response_data_map(self, prefix):
        """Get a map of the response data where the keys are the RIS response
        keys that begin with a specified prefix.
        Arg: prefix - Key prefix.
        return dict of key-value pairs for a specified RIS key prefix."""
        data = {key: self.params[key] for key in self.params
                if key.startswith(prefix)}
        LOG.debug("get_prefixed_response_data_map = %s", data)
        return data

    def get_counters_triggered(self):
        """Get a map of the rules counters triggered in the response.
        return dict Key: counter name, Value: counter value.
        """
        counters = {}
        num_counters = int(self.params.get("COUNTERS_TRIGGERED", 0))
        for i in range(num_counters):
            counters[self.params["COUNTER_NAME_%s" % i]] = \
                self.params["COUNTER_VALUE_%s" % i]
        LOG.debug("get_counters_triggered = %s", counters)
        return counters

    def get_version(self):
        """ Get the version number.
        :return RIS version
        """
        return self.params.get("VERS")

    def get_merchant(self):
        """ Get the merchant id.
        :return Merchant ID
        """
        return self.params.get("MERC")
