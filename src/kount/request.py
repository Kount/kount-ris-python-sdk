#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""RIS Request superclass for Inquiry and Update"""

import logging

from .config import SDKConfig
from .util.khash import Khash
from .util import payment as payments
from .version import VERSION

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"

LOG = logging.getLogger('kount.request')


class _RisType(object):

    __CACHED_ATTRS = None

    @classmethod
    def is_valid(cls, val):
        attrs = cls.__CACHED_ATTRS
        if attrs is None:
            attrs = {
                v for k, v in vars(cls).items() if not k.startswith('_')
            }
            cls.__CACHED_ATTRS = attrs
        return val in attrs


class AuthStatus(_RisType):
    """Authorization status"""
    APPROVE = 'A'
    DECLINE = 'D'
    REVIEW = 'R'
    ESCALATE = "E"
    REVIEW_TIMEOUT = 'X'
    APPROVED_DECLINED_TIMEOUT = 'Y'
    ELEVATED = 'C'


class BankcardReply(_RisType):
    """Bankcard Reply"""
    MATCH = 'M'
    NO_MATCH = 'N'
    UNAVAILABLE = 'X'


class Gender(_RisType):
    """gender"""
    MALE = 'M'
    FEMALE = 'F'


class AddressType(_RisType):
    """address type"""
    BILLING = 'B'
    SHIPPING = 'S'


class ShippingType(_RisType):
    """
    "SD". Same day shipping type.
    "ND". Next day shipping type.
    "2D". Second day shipping type.
    "ST". Standard shipping type.
    """
    SAME_DAY = 'SD'
    NEXT_DAY = 'ND'
    SECOND_DAY = '2D'
    STANDARD = "ST"


class RefundChargebackStatus(_RisType):
    """Refund charge back status.
    R - The transaction was a refund.
    C - The transaction was a chargeback.
    """
    REFUND = 'R'
    CHARGEBACK = 'C'


class MerchantAcknowledgment(_RisType):
    """merchant acknowledgment
    "Y". The product expects to ship.
    "N". The product does not expect to ship.
    """
    FALSE = 'N'
    TRUE = 'Y'


class CurrencyType(_RisType):
    """Currency type object
    "USD". United States Dollars
    "EUR". European currency unit
    "CAD". Canadian Dollar
    "AUD". Australian Dollar
    "JPY". Japanese Yen
    "HKD". Honk Kong Dollar
    "NZD". New Zealand Dollar
    """
    USD = 'USD'
    EUR = 'EUR'
    CAD = 'CAD'
    AUD = 'AUD'
    JPY = 'JPY'
    HKD = 'HKD'
    NZD = 'NZD'


class InquiryMode(_RisType):
    """
    "Q". Default inquiry mode, internet order type.
    "P". Phone order type.
    "W". Kount Central Mode W - Full Inquiry [W]ith thresholds.
    "J". Kount Central Mode J - Fast Inquiry [J]ust thresholds.
    """
    DEFAULT = 'Q'
    PHONE = 'P'
    WITH_THRESHOLDS = 'W'
    JUST_THRESHOLDS = 'J'


class Request(object):
    """RIS Request superclass for Inquiry and Update."""

    def __init__(self):
        """Map containing data that will be sent to RIS."""
        self.params = dict()
        self.payment = None
        self.close_on_finish = None

    def set_param(self, key, value):
        """Set a parm for the request.
        Args:
           key - The key for the parm
           value - The value for the parm
        """
        self.params[key] = value
        LOG.debug("%s = %s", key, value)

    def set_khash_payment_encoding(self, enabled=True):
        """Set KHASH payment encoding.
        Arg: enabled Boolean
        """
        self.set_param("PENC", "KHASH" if enabled else "")

    def set_version(self, version):
        """Set the version number.
        Args: version - The SDK version
        """
        self.set_param("VERS", version)

    def set_session_id(self, session_id):
        """Set the session id. Must be unique over a 30-day span
        Args: session_id -  Id of the current session
        """
        self.set_param("SESS", session_id)

    def set_merchant(self, merchant_id):
        """Set the merchant id.
        Args: merchant_id - Merchant ID
        """
        self.set_param("MERC", merchant_id)

    def set_kount_central_customer_id(self, customer_id):
        """Set the Kount Central Customer ID.
        Args: customer_id - KC Customer ID
        """
        self.set_param("CUSTOMER_ID", customer_id)

    def set_order_number(self, order_number):
        """Set the order number.
        Args: order_number - Merchant unique order number
        """
        self.set_param("ORDR", order_number)

    def set_merchant_acknowledgment(self, ma_type):
        """Set the merchant acknowledgment.
        Merchants acknowledgement to ship/process the order.
        The MACK field must be set as MerchantAcknowledgment.TRUE
        if personal data is to be
        collected to strengthen the score.
        Args: ma_type - merchant acknowledgment type
        """
        if MerchantAcknowledgment.is_valid(ma_type):
            self.set_param("MACK", ma_type)
        else:
            raise ValueError("Invalid MerchantAcknowledgment = %s" % ma_type)

    def set_authorization_status(self, auth_status):
        """Set the Authorization Status.
        Authorization Status returned to merchant from processor.
        Acceptable values for the
        AUTH field are AuthStatus. In orders where AUTH=A will
        aggregate towards order velocity of the persona while
        orders where AUTH=D will
        decrement the velocity of the persona.
        Args: auth_status - Auth status by issuer
        """
        if AuthStatus.is_valid(auth_status):
            self.set_param("AUTH", auth_status)
        else:
            raise ValueError("Invalid AuthStatus value %s" % auth_status)

    def set_avs_zip_reply(self, avs_zip_reply):
        """Set the Bankcard AVS zip code reply.
        Address Verification System Zip Code verification response
        returned to merchant from
        processor. Acceptable values are BCRSTAT.
        Args: avs_zip_reply - Bankcard AVS zip code reply
        """
        if BankcardReply.is_valid(avs_zip_reply):
            self.set_param("AVSZ", avs_zip_reply)
        else:
            raise ValueError('Invalid BankcardReply = %s' % avs_zip_reply)

    def set_avs_address_reply(self, avs_address_reply):
        """Set the Bankcard AVS street addres reply.
        Address Verification System Street verification response
        returned to merchant from processor. Acceptable values are BCRSTAT.
        Args: avs_address_reply - Bankcard AVS street address reply
        """
        if BankcardReply.is_valid(avs_address_reply):
            self.set_param("AVST", avs_address_reply)
        else:
            raise ValueError('Invalid BankcardReply = %s' % avs_address_reply)

    def set_avs_cvv_reply(self, cvv_reply):
        """Set the Bankcard CVV/CVC/CVV2 reply.
        Card Verification Value response returned to merchant from processor.
        Acceptable values are BCRSTAT
        Args: cvv_reply -  Bankcard CVV/CVC/CVV2 reply
        """
        if BankcardReply.is_valid(cvv_reply):
            self.set_param("CVVR", cvv_reply)
        else:
            raise ValueError('Invalid BankcardReply = %s' % cvv_reply)

    def set_payment(self, payment):
        """ Set a payment.
            Depending on the payment type, various request parameters are set:
            PTOK, PTYP, LAST4.
            If payment token hashing is not possible, the PENC parameter is set
            to empty string.
            Args: payment -  Payment
        """
        khasher = Khash.get()
        if "PENC" in self.params \
                and not isinstance(payment, payments.NoPayment) \
                and not payment.khashed:
            try:
                if not self.params.get("MERC"):
                    raise ValueError("merchant_id not set")
                if isinstance(payment, payments.GiftCardPayment):
                    merchant_id = int(self.params["MERC"])
                    payment.payment_token = khasher.hash_gift_card(
                        merchant_id, payment.payment_token)
                else:
                    payment.payment_token = khasher.hash_payment_token(
                        payment.payment_token)
                payment.khashed = True
                self.set_param("PENC", "MASK")
                LOG.debug("payment.khashed=%s", payment.khashed)
            except ValueError as nfe:
                LOG.debug("Error converting Merchant ID to integer"
                          " value. Set a valid Merchant ID. %s",
                          str(nfe))
                raise nfe
            except Exception as nsae:
                LOG.debug("Unable to create payment token hash. Caught %s "
                          "KHASH payment encoding disabled", str(nsae))
                # Default to plain text payment tokens
                self.params["PENC"] = ""
        if khasher.khashed(payment.payment_token):
            self.set_param("PENC", "KHASH")
        self.set_param("PTOK", payment.payment_token)
        self.set_param("PTYP", payment.payment_type)
        self.set_param("LAST4", payment.last4)

    @staticmethod
    def _mask_token(token):
        """Encodes the provided payment token according to the MASK
           encoding scheme
           Args: token -  the Payment token for this request
           return - MASK-encoded token
        """
        encoded = token[0:6]
        for _ in range(6, len(token) - 4, 1):
            encoded.append('X')
        encoded.append(token[-4:])
        LOG.debug("mask_token = %s", token)
        return encoded

    def set_payment_by_type(self, ptyp, ptok):
        """ Set a payment by payment type and payment token.
        The payment type parameter provided is checked
        if it's one of the predefined payment types
        and Payment is created appropriately
        Args: ptyp - See SDK documentation for a list of accepted payment types
        ptok - The payment token
        """
        cls = {
            "BLML": payments.BillMeLaterPayment,
            'CARD': payments.CardPayment,
            'CHECK': payments.CheckPayment,
            'GIFT': payments.GiftCardPayment,
            'GOOG': payments.GooglePayment,
            'GDMP': payments.GreenDotMoneyPakPayment,
            'NONE': payments.NoPayment,
            'PYPL': payments.PaypalPayment,
        }.get(ptyp)
        if cls is None:
            cls = payments.Payment
        self.set_payment(cls(ptyp, ptok))

    def set_masked_payment(self, payment):
        """ Sets a card payment and masks the card number in the following way:
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
        if isinstance(self.payment, payment.CardPayment) and \
                not payment.khashed:
            token = self._mask_token(token)
            self.set_param("PTOK", token)
            self.set_param("PTYP", payment.payment_type)
            self.set_param("LAST4", payment.last4)
            self.set_param("PENC", "MASK")
        else:
            self.set_param("PTOK", token)
            LOG.debug("Payment Masked: provided payment is not "
                      "a CardPayment, applying khash instead of masking")
            self.set_payment_by_type(payment, token)

    def is_set_khash_payment_encoding(self):
        """Check if KHASH payment encoding has been set.
           return boolean TRUE when set.
        """
        encoded = self.params.get("PENC") == "KHASH"
        LOG.debug("is_set_khash_payment_encoding = %s", encoded)
        return encoded

    def set_close_on_finish(self, close_on_finish):
        """Set a flag for the request transport.
           Arg: close_on_finish - Sets the close_on_finish flag
           return boolean TRUE when set.
        """
        self.close_on_finish = close_on_finish
        LOG.debug("close_on_finish = %s", close_on_finish)


class UpdateMode(_RisType):
    """UpdateMode - U, X"""
    NO_RESPONSE = 'U'
    WITH_RESPONSE = 'X'


class Update(Request):
    """RIS update class.
     defaults to update_mode WithResponse.
     """

    def __init__(self):
        super(Update, self).__init__()
        self.set_mode(UpdateMode.NO_RESPONSE)
        self.params['VERS'] = SDKConfig.SDK_VERSION
        # self.params["SDK"] = "python"
        self.set_khash_payment_encoding(True)

    def set_mode(self, mode):
        """Set the mode.
        Args - mode - Mode of the request
        """
        if UpdateMode.is_valid(mode):
            self.params["MODE"] = mode
        else:
            raise ValueError("Invalid UpdateMode: %s" % mode)

    def set_transaction_id(self, transaction_id):
        """Set the transaction id.
        Arg - transaction_id, String Transaction id
        """
        self.params["TRAN"] = transaction_id

    def set_refund_chargeback_status(self, rc_status):
        """Set the Refund/Chargeback status: R = Refund C = Chargeback.
        Arg - rc_status, String Refund or chargeback status
        """
        if RefundChargebackStatus.is_valid(rc_status):
            self.params["RFCB"] = rc_status
        else:
            raise ValueError("Invalid RefundChargebackStatus: %s" % rc_status)

