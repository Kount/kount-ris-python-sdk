#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"RIS Request superclass for Inquiry and Update"

from __future__ import absolute_import, unicode_literals, division, print_function
import logging
from .util.payment import (CardPayment, GiftCardPayment, NoPayment, Payment)
from .util.khash import Khash
from .ris_validator import RisException
from .settings import SDK_VERSION

__author__ = "Kount SDK"
__version__ = "1.0.0"
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"


class ASTAT(object):
    "Authorization status"
    Approve = 'A'
    Decline = 'D'
    Review = 'R'
    Escalate = "E"
    Review_Timeout = 'X'
    Approved_Declined_Timeout = 'Y'
    Elevated = 'C'


class BCRSTAT(object):
    "Bankcard Reply"
    MATCH = 'M'
    NO_MATCH = 'N'
    UNAVAILABLE = 'X'


class GENDER(object):
    "gender"
    MALE = 'M'
    FEMALE = 'F'


class ADDRESS(object):
    'address type'
    BILLING = 'B'
    SHIPPING = 'S'


class SHIPPINGTYPESTAT(object):
    """
    "SD". Same day shipping type.
    "ND". Next day shipping type.
    "2D". Second day shipping type.
    "ST". Standard shipping type.
    """
    SAMEDAY = 'SD'
    NEXDAY = 'ND'
    SECCONDDAY = '2D'
    STANDARD = "ST"


class REFUNDCBSTAT(object):
    """Refund charge back status.
    R - The transaction was a refund.
    C - The transaction was a chargeback.
    """
    REFUND = 'R'
    CHARGEBACK = 'C'


class MERCHANTACKNOWLEDGMENT(object):
    """merchant acknowledgment
    "Y". The product expects to ship.
    "N". The product does not expect to ship.
    """
    FALSE = 'N'
    TRUE = 'Y'


class CURRENCYTYPE(object):
    """Currency type object
    "USD". United States Dollars
    "EUR". European currency unit
    "CAD". Canadian Dollar
    "AUD". Austrailian Dollar
    "JPY". Japanese Yen
    "HKD". Hong Kong Dollar
    "NZD". Hong Kong Dollar
    """
    USD = 'USD'
    EUR = 'EUR'
    CAD = 'CAD'
    AUD = 'AUD'
    JPY = 'JPY'
    HKD = 'HKD'
    NZD = 'NZD'


class INQUIRYMODE(object):
    """
    "Q". Default inquiry mode, internet order type.
    "P". Phone order type.
    "W". Kount Central Mode W - Full Inquiry [W]ith thresholds.
    "J". Kount Central Mode J - Fast Inquiry [J]ust thresholds.
    """
    DEFAULT = 'Q'
    PHONE = 'P'
    WITHTHRESHOLDS = 'W'
    JUSTTHRESHOLDS = 'J'

logger = logging.getLogger('kount.request')


class Request(object):
    """RIS Request superclass for Inquiry and Update."""

    def __init__(self):
        "Map containing data that will be sent to RIS."
        self.params = {}
        self.params['VERS'] = SDK_VERSION
        self.khash_payment_encoding(True)
        self.params["SDK"] = "python"
        self.payment = None
        self.close_on_finish = None
        Khash.verify()

    def khash_payment_encoding(self, enabled=True):
        """Set KHASH payment encoding.
        Arg: enabled Boolean
        """
        if enabled:
            self.params["PENC"] = "KHASH"
        else:
            self.params["PENC"] = None
        logger.debug("PENC = %s", self.params["PENC"])

    def params_set(self, key, value):
        """Set a parm for the request.
        Args:
           key - The key for the parm
           value - The value for the parm
        """
        self.params[key] = value
        logger.debug("%s = %s", key, value)

    def version_set(self, version):
        """Set the version number.
        Args: version - The SDK version
        """
        self.params["VERS"] = version
        logger.debug("VERS = %s", version)

    def session_set(self, session_id):
        """Set the session id. Must be unique over a 30-day span
        Args: session_id -  Id of the current session
        """
        self.params["SESS"] = session_id
        logger.debug("SESS = %s", session_id)

    def merchant_set(self, merchant_id):
        """Set the merchant id.
        Args: merchant_id - Merchant ID
        """
        self.params["MERC"] = merchant_id
        logger.debug("MERC = %s", merchant_id)

    def kount_central_customer_id(self, customer_id):
        """Set the Kount Central Customer ID.
        Args: customer_id - KC Customer ID
        """
        self.params["CUSTOMER_ID"] = customer_id
        logger.debug("CUSTOMER_ID = %s", customer_id)

    def order_number(self, order_number):
        """Set the order number.
        Args: order_number - Merchant unique order number
        """
        self.params["ORDR"] = order_number
        logger.debug("ORDR = %s", order_number)

    def merchant_acknowledgment_set(self, ma_type):
        """Set the merchant acknowledgment.
        Merchants acknowledgement to ship/process the order.
        The MACK field must be set as MERCHANTACKNOWLEDGMENT.TRUE
        if personal data is to be
        collected to strengthen the score.
        Args: ma_type - merchant acknowledgment type
        """
        self.params["MACK"] = ma_type
        logger.debug("MACK = %s", ma_type)

    def authorization_status(self, auth_status):
        """Set the Authorization Status.
        Authorization Status returned to merchant from processor.
        Acceptable values for the
        AUTH field are ASTAT. In orders where AUTH=A will
        aggregate towards order velocity of the persona while
        orders where AUTH=D will
        decrement the velocity of the persona.
        Args: auth_status - Auth status by issuer
        """
        self.params["AUTH"] = auth_status
        logger.debug("AUTH = %s", auth_status)

    def avs_zip_reply(self, avs_zip_reply):
        """Set the Bankcard AVS zip code reply.
        Address Verification System Zip Code verification response
        returned to merchant from
        processor. Acceptable values are BCRSTAT.
        Args: avs_zip_reply - Bankcard AVS zip code reply
        """
        self.params["AVSZ"] = avs_zip_reply
        logger.debug("AVSZ = %s", avs_zip_reply)

    def avs_address_reply(self, avs_address_reply):
        """Set the Bankcard AVS street addres reply.
        Address Verification System Street verification response
        returned to merchant from processor. Acceptable values are BCRSTAT.
        Args: avs_address_reply - Bankcard AVS street address reply
        """
        self.params["AVST"] = avs_address_reply
        logger.debug("AVST = %s", avs_address_reply)

    def avs_cvv_reply(self, cvv_reply):
        """Set the Bankcard CVV/CVC/CVV2 reply.
        Card Verification Value response returned to merchant from processor.
        Acceptable values are BCRSTAT
        Args: cvv_reply -  Bankcard CVV/CVC/CVV2 reply
        """
        self.params["CVVR"] = cvv_reply
        logger.debug("CVVR = %s", cvv_reply)

    def payment_set(self, payment):
        """ Set a payment.
            Depending on the payment type, various request parameters are set:
            PTOK, PTYP, LAST4.
            If payment token hashing is not possible, the PENC parameter is set
            to empty string.
            Args: payment -  Payment
        """
        if "PENC" in self.params and not (isinstance(payment, NoPayment))\
                and not payment.khashed:
            try:
                if isinstance(payment, GiftCardPayment):
                    merchant_id = int(self.params["MERC"])
                    payment.payment_token = Khash.hash_gift_card(
                        merchant_id, payment.payment_token)
                else:
                    payment.payment_token = Khash.hash_payment_token(
                        payment.payment_token)
                payment.khashed = True
                self.params["PENC"] = "MASK"
                logger.debug("payment.khashed=%s, 'PENC'=%s",
                    payment.khashed, self.params["PENC"])
            except ValueError as nfe:
                logger.debug("Error converting Merchant ID to integer"
                             " value. Set a valid Merchant ID. %s",
                             str(nfe))
                raise nfe
            except Exception as nsae:
                logger.debug("Unable to create payment token hash. Caught %s"
                             " KHASH payment encoding disabled", str(nsae))
                #Default to plain text payment tokens
                self.params["PENC"] = ""
        self.params["PTOK"] = payment.payment_token
        self.params["PTYP"] = payment.payment_type
        self.params["LAST4"] = payment.last4
        logger.debug("payment ['PTOK']= %s, ['PTYP']=%s, ['LAST4']=%s",
                     payment.payment_token, payment.payment_type,
                     payment.last4)

    def mask_token(self, token):
        """Encodes the provided payment token according to the MASK
           encoding scheme
           Args: token -  the Payment token for this request
           return - MASK-encoded token
        """
        encoded = token[0:6]
        for _ in range(6, len(token) - 4, 1):
            encoded.append('X')
        encoded.append(token[-4:])
        logger.debug("mask_token = %s", token)
        return encoded

    def set_payment(self, ptyp, ptok):
        """ Set a payment by payment type and payment token.
        The payment type parameter provided is checked
        if it's one of the predefined payment types
        and Payment is created appropriately
        Args: ptyp - See SDK documentation for a list of accepted payment types
        ptok - The payment token
        """
        self.payment = Payment(ptyp, ptok)
        logger.debug("mask_token = %s", self.payment)

    def payment_masked(self, payment):
        """Sets a card payment and masks the card number in the following way:
        First 6 characters remain as they are, following characters up to the
        last 4 are replaced with the 'X' character, last 4 characters
        remain as they are.
        If the provided Payment parameter is not a card payment,
        standard encoding will be applied.
        This method sets the following RIS Request fields:
        PTOK, PTYP, LAST4, PENC.
        Args: payment - card payment
        """
        token = payment.payment_token
        if isinstance(self.payment, CardPayment) and not payment.khashed:
            token = self.mask_token(token)
            self.params["PTOK"] = token
            self.params["PTYP"] = payment.payment_type
            self.params["LAST4"] = payment.last4
            self.params["PENC"] = "MASK"
            logger.debug("PTOK = %s, PTYP= %s, LAST4=%s, PENC=MASK",
                         token, payment.payment_type, payment.last4)
            return self
        else:
            self.params["PTOK"] = token
            logger.debug("Payment Masked: provided payment is not "
                         "a CardPayment, applying khash instead of masking")
            return self.set_payment(payment, token)

    def expiration_date(self, month, year):
        """Set Card Expiration Date.
           Args: month - String Month in two digit format: MM.
                 year - String Year in four digit format: YYYY.
        """
        self.params["CCMM"] = month
        self.params["CCYY"] = year
        logger.debug("expiration_date CCMM=%s, CCYY=%s", month, year)

    def is_set_khash_payment_encoding(self):
        """Check if KHASH payment encoding has been set.
           return boolean TRUE when set.
        """
        encoded = "PENC" in self.params and self.params["PENC"] == "KHASH"
        logger.debug("is_set_khash_payment_encoding = %s", encoded)
        return encoded

    def set_close_on_finish(self, close_on_finish):
        """Set a flag for the request transport.
           Arg: close_on_finish - Sets the close_on_finish flag
           return boolean TRUE when set.
        """
        self.close_on_finish = close_on_finish
        logger.debug("close_on_finish = %s", close_on_finish)


class UPDATEMODE(object):
    "UPDATEMODE - U, X"
    NO_RESPONSE = 'U'
    WITH_RESPONSE = 'X'


class Update(Request):
    """RIS update class.
     defaults to update_mode WithResponse.
     """
    def __init__(self):
        super(Update, self).__init__()
        self.set_mode(UPDATEMODE.NO_RESPONSE)
        del self.params["SDK"]

    def set_mode(self, mode):
        """Set the mode.
        Args - mode - Mode of the request
        raise RisException when mode is None"""
        if mode is None:
            raise RisException("Mode can not be None")
        if mode in 'UX':
            self.params["MODE"] = mode

    def set_transaction_id(self, transaction_id):
        """Set the transaction id.
        Arg - transaction_id, String Transaction id
        """
        self.params["TRAN"] = transaction_id

    def refund_chargeback_status(self, rc_status):
        """Set the Refund/Chargeback status: R = Refund C = Chargeback.
        Arg - rc_status, String Refund or chargeback status
        raise RisException when refund_chargeback_status is None
        """
        if rc_status in 'RC':
            self.params["RFCB"] = rc_status
        else:
            raise RisException("rc_status can not be None")
