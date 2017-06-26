#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
from __future__ import absolute_import, unicode_literals, division, print_function
import logging

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"

logger = logging.getLogger('kount.response')


class KcEvent(object):
    """A class that represents a Kount Central event.
    The event object contains three fields: decision, expression, and code.
    """

    def __init__(self, decision, expression, code):
        """Constructor for an event object.
        Args:
        event_decision - The decision for the event
        event_expression - The expression for the event
        event_code - The event code
        """
        self.event_decision = decision
        self.event_expression = expression
        self.event_code = code
        logger.debug("KcEvent - event_decision = %s, "
                     "event_expression = %s, event_code= %s",
                     decision, expression, code)


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
        logger.debug("RIS response init = %s", params)

    def get_kc_warnings(self):
        "Get an List of the KC warnings returned by this Response."
        warnings = []
        warning_count = int(self.params["WARNING_COUNT"])
        for i in range(warning_count):
            warnings.append(self.params["WARNING_%s" % i])
        logger.debug("RIS get_kc_warnings = %s", warnings)
        return warnings

    def get_kc_errors(self):
        "get kc errors"
        errors = []
        error_count = int(self.params["KC_ERROR_COUNT"])
        for i in range(error_count):
            errors.append(self.params["KC_ERROR_%s" % i])
        logger.debug("RIS get_kc_errors = %s", errors)
        return errors

    def get_kc_events_count(self):
        "get_kc_events_count"
        event_count = int(self.params["KC_TRIGGERED_COUNT"])
        logger.debug("RIS get_kc_event_count = %s", event_count)
        return event_count

    def get_kc_events(self):
        """Get an ArrayList of the KC events returned by this Response."""
        events = {}
        event_count = int(self.params["KC_TRIGGERED_COUNT"])
        for i in range(event_count):
            events["KC_EVENT_%s_DECISION" % (i+1)] = \
                self.params["KC_EVENT_%s_DECISION" % (i + 1)]
            events["KC_EVENT_%s_EXPRESSION" % (i+1)] = \
                self.params["KC_EVENT_%s_EXPRESSION" % (i + 1)]
            events["KC_EVENT_%s_CODE" % (i+1)] =\
                self.params["KC_EVENT_%s_CODE" % (i + 1)]
        logger.debug("RIS get_kc_events = %s", events)
        return events

    def get_rules_triggered(self):
        """Get a Map of the rules triggered by this Response."""
        rules = {}
        rules_triggered_count = int(self.params["RULES_TRIGGERED"])
        for i in range(rules_triggered_count):
            rule_id = self.params["RULE_ID_%s" % i]
            rules[rule_id] = self.params["RULE_DESCRIPTION_%s" % i]
        logger.debug("RIS get_rules_triggered = %s", rules)
        return rules

    def get_warnings(self):
        "get_warnings"
        warnings = []
        warning_count = int(self.params["WARNING_COUNT"])
        for i in range(warning_count):
            warnings.append(self.params["WARNING_%s" % i])
        logger.debug("RIS get_warnings = %s", warnings)
        return warnings

    def get_errors(self):
        """Get an ArrayList of errors associated with the response."""
        errors = []
        error_count = int(self.params["ERROR_COUNT"])
        for i in range(error_count):
            errors.append(self.params["ERROR_%s" % i])
        logger.debug("RIS get_errors= %s", errors)
        return errors

    def get_lexis_nexis_cbd_attributes(self):
        """Get LexisNexis Chargeback Defender attribute data
        associated with the RIS
        transaction. Please contact your Kount representative to enable support
        for this feature in your merchant account.
        return Map of attributes where the keys are the attribute names and the
        values are the attribute values."""
        cbd = self.get_prefixed_response_data_map("CBD_")
        logger.debug("get_lexis_nexis_cbd_attributes = %s", cbd)
        return cbd

    def get_lexis_nexis_instant_id_attributes(self):
        """Get LexisNexis Instant ID attributes associated with the
        RIS transaction.
        Please contact your Kount representative to enable support for this
        feature in your merchant account.
        return Map of attributes where the keys are the attribute names and the
        values are the attribute values."""
        instand_id = self.get_prefixed_response_data_map("INSTANTID_")
        logger.debug("get_lexis_nexis_instand_id_attributes = %s", instand_id)
        return instand_id

    def get_prefixed_response_data_map(self, prefix):
        """Get a map of the response data where the keys are the RIS response
        keys that begin with a specified prefix.
        Arg: prefix - Key prefix.
        return dict of key-value pairs for a specified RIS key prefix."""
        data = {key: self.params[key] for key in self.params
                if key.startswith(prefix)}
        logger.debug("get_prefixed_response_data_map = %s", data)
        return data

    def get_counters_triggered(self):
        """Get a map of the rules counters triggered in the response.
        return dict Key: counter name, Value: counter value.
        """
        counters = {}
        num_counters = int(self.params["COUNTERS_TRIGGERED"])
        for i in range(num_counters):
            counters[self.params["COUNTER_NAME_%s" % i]] =\
                     self.params["COUNTER_VALUE_%s" % i]
        logger.debug("get_counters_triggered = %s", counters)
        return counters
