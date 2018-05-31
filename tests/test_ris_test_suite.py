#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""Test Cases from sdk documentation"""
import unittest

import pytest

from kount.request import (AuthStatus, BankcardReply, InquiryMode,
                           CurrencyType, MerchantAcknowledgment)
from kount.request import Update, UpdateMode
from kount.util.khash import Khash
from kount.client import Client
from kount.util.cartitem import CartItem
from kount.ris_validator import RisValidationException
from kount.util.payment import CardPayment
from kount.version import VERSION

from .test_basic_connectivity import generate_unique_id, default_inquiry

__author__ = "Kount SDK"
__version__ = VERSION
__maintainer__ = "Kount SDK"
__email__ = "sdkadmin@kount.com"
__status__ = "Development"

# raise_errors - if  True - raise errors instead of logging in debugger
_RAISE_ERRORS = False

PTOK = "0007380568572514"
EMAIL_CLIENT = "sdkTest@kountsdktestdomain.com"


@pytest.mark.usefixtures("merchant_id", "api_key", "api_url")
class TestRisTestSuite(unittest.TestCase):
    """Ris Test Suite
        default logging errors instead fo raising
        to raise errors - put raise_errors=True in Client:
        Client(url=URL_API, key=KOUNT_API_KEY,
               timeout=TIMEOUT, RAISE_ERRORS=True)
    """
    merchant_id = None
    api_key = None
    api_url = None

    maxDiff = None

    def setUp(self):
        self.session_id = generate_unique_id()[:32]
        self.payment = CardPayment(PTOK, khashed=False)
        self.client = Client(self.api_url, self.api_key,
                             raise_errors=_RAISE_ERRORS)

    def inquiry(self):
        return default_inquiry(
            merchant_id=self.merchant_id,
            session_id=self.session_id,
            email_client=EMAIL_CLIENT,
            payment=self.payment)

    def test_1_ris_q_1_item_required_field_1_rule_review(self):
        """test_1_ris_q_1_item_required_field_1_rule_review"""
        res = self.client.process(self.inquiry())
        self.assertIsNotNone(res)
        self.assertEqual("R", res.get_auto())
        self.assertEqual(0, len(res.get_warnings()))
        expected = ['Review if order total > $1000 USD']
        actual = sorted(res.get_rules_triggered().values())
        self.assertEqual(expected, actual)
        self.assertEqual(self.session_id, res.get_session_id())
        self.assertEqual(res.get_session_id()[:10], res.get_order_id())

    def test_2_ris_q_multi_cart_items2optional_fields2rules_decline(self):
        """test_2_ris_q_multi_cart_items2optional_fields2rules_decline
        cart_item - PROD_TYPE[0, PROD_ITEM[0], PROD_DESC[0]
                    PROD_QUANT[0],PROD_PRICE[0]"""
        inq = self.inquiry()
        inq.set_user_agent(
            "Mozilla/5.0 (Macintosh; "
            "Intel Mac OS X 10_9_5) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/37.0.2062.124 "
            "Safari/537.36")
        inq.set_total(123456789)
        cart_items = [
            CartItem(
                "cart item type 0", "cart item 0",
                "cart item 0 description", 10, 1000),
            CartItem(
                "cart item type 1", "cart item 1",
                "cart item 1 description", 11, 1001),
            CartItem(
                "cart item type 2", "cart item 2",
                "cart item 1 description", 12, 1002)]
        inq.set_shopping_cart(cart_items)
        res = self.client.process(inq)
        self.assertIsNotNone(res)
        self.assertEqual("D", res.get_auto())
        self.assertEqual(0, len(res.get_warnings()))
        expected = sorted(
            {'1024842': 'Review if order total > $1000 USD',
             '1024844': 'Decline if order total > $1000000 USD'}.values())
        actual = sorted(res.get_rules_triggered().values())
        self.assertEqual(expected, actual)

    def test_3_ris_q_with_user_defined_fields(self):
        """test_3_ris_q_with_user_defined_fields"""
        udf1 = "ARBITRARY_ALPHANUM_UDF"
        udf2 = "ARBITRARY_NUMERIC_UDF"
        inq = self.inquiry()
        inq.set_user_defined_field(udf1, "alphanumeric trigger value")
        inq.set_user_defined_field(udf2, "777")
        res = self.client.process(inq)
        self.assertIsNotNone(res)
        self.assertEqual("R", res.get_auto())
        self.assertEqual(3, len(res.get_rules_triggered()))
        self.assertEqual(0, len(res.get_warnings()))
        self.assertEqual(0, len(res.get_errors()))
        self.assertEqual(0, len(res.get_counters_triggered()))
        expected = sorted(
            {'1025086': 'review if %s contains "trigger"' % udf1,
             '1024842': 'Review if order total > $1000 USD',
             '1025088': "review if %s == 777" % udf2}.values())
        actual = sorted(res.get_rules_triggered().values())
        self.assertEqual(expected, actual)

    def test_4_ris_q_hard_error_expected(self):
        """test_4_ris_q hard_error_expected,
        overwrite the PTOK value to induce an error in the RIS"""
        inq = self.inquiry()
        inq.params["PENC"] = "KHASH"
        inq.params["PTOK"] = "BADPTOK"
        res = self.client.process(inq)
        self.assertIsNotNone(res)
        self.assertEqual(
            ["332 BAD_CARD Cause: [PTOK invalid format], "
             "Field: [PTOK], Value: [hidden]"],
            res.get_errors())
        self.assertEqual("E", res.get_mode())
        self.assertEqual(332, res.get_error_code())
        self.assertEqual(0, len(res.get_warnings()))

    def test_5_ris_q_warning_approved(self):
        """test_5_ris_q_warning_approved"""
        inq = self.inquiry()
        inq.set_total(1000)
        label = "UDF_DOESNOTEXIST"
        mesg = "throw a warning please!"
        inq.set_user_defined_field(label, mesg)
        res = self.client.process(inq)
        self.assertIsNotNone(res)
        self.assertEqual("A", res.get_auto())
        self.assertEqual(2, len(res.get_warnings()))
        self.assertEqual(res.get_warnings()[0],
                         "399 BAD_OPTN Field: [UDF], Value: "
                         "[%s=>%s]" % (label, mesg))
        self.assertEqual(res.get_warnings()[1],
                         "399 BAD_OPTN Field: [UDF], Value: "
                         "[The label [%s]"
                         " is not defined for merchant ID [%s].]" % (
                             label, self.merchant_id))

    def test_6_ris_q_hard_soft_errors_expected(self):
        """test_6_ris_q_hard_soft_errors_expected"""
        inq = self.inquiry()
        inq.params["PENC"] = "KHASH"
        inq.params["PTOK"] = "BADPTOK"
        label = "UDF_DOESNOTEXIST"
        mess = "throw a warning please!"
        inq.params["UDF[%s]" % label] = mess
        res = self.client.process(inq)
        self.assertIsNotNone(res)
        self.assertEqual("E", res.get_mode())
        self.assertEqual(332, res.get_error_code())
        self.assertEqual(1, len(res.get_errors()))
        self.assertEqual(
            [("332 BAD_CARD Cause: [PTOK invalid format], "
              "Field: [PTOK], Value: [hidden]")],
            res.get_errors())
        warnings = res.get_warnings()
        self.assertEqual(2, len(warnings))
        self.assertEqual(
            "399 BAD_OPTN Field: [UDF], Value: [%s=>%s]"
            % (label, mess), warnings[0])
        self.assertEqual(
            "399 BAD_OPTN Field: [UDF], Value: [The label [%s] "
            "is not defined for merchant ID [%s].]"
            % (label, self.merchant_id), warnings[1])

    def test_7_ris_w2_kc_rules_review(self):
        """test_7_ris_w2_kc_rules_review"""
        inq = self.inquiry()
        inq.set_request_mode(InquiryMode.WITH_THRESHOLDS)
        inq.set_total(10001)
        inq.set_kount_central_customer_id("KCentralCustomerOne")
        res = self.client.process(inq)
        self.assertIsNotNone(res)
        self.assertEqual(res.get_kc_decision(), 'R')
        self.assertEqual(len(res.get_kc_warnings()), 0)
        self.assertEqual(len(res.get_kc_events()), 2)
        events = res.get_kc_events()
        print(events)
        self.assertEqual(events[0].code, 'billingToShippingAddressReview')
        self.assertEqual(events[1].expression, '10001 > 10000')
        self.assertEqual(events[0].decision, 'R')
        self.assertEqual(events[1].code, 'orderTotalReview')
        self.assertEqual(events[0].expression, '5053 > 1')
        self.assertEqual(events[1].decision, 'R')

    def test_8_ris_j_1_kount_central_rule_decline(self):
        """test_8_ris_j_1_kount_central_rule_decline"""
        inq = self.inquiry()
        inq.set_request_mode(InquiryMode.JUST_THRESHOLDS)
        inq.set_total(1000)
        inq.set_kount_central_customer_id("KCentralCustomerDeclineMe")
        if not _RAISE_ERRORS:
            res = self.client.process(inq)
            self.assertIsNotNone(res)
            self.assertEqual("D", res.get_kc_decision())
            self.assertEqual(0, len(res.get_kc_warnings()))
            kc_events = res.get_kc_events()
            self.assertEqual(1, len(kc_events), )
            self.assertEqual(kc_events[0].code, "orderTotalDecline")
        else:
            self.assertRaises(RisValidationException,
                              self.client.process, inq)

    def test_9_mode_u_after_mode_q(self):
        """test_9_mode_u_after_mode_q"""
        res = self.client.process(self.inquiry())
        self.assertIsNotNone(res)
        transaction_id = res.get_transaction_id()
        session_id = res.get_session_id()
        order_id = res.get_order_id()

        update1 = Update()
        update1.set_mode(UpdateMode.NO_RESPONSE)
        update1.set_transaction_id(transaction_id)
        update1.set_merchant(self.merchant_id)
        update1.set_session_id(session_id)
        update1.set_order_number(order_id)
        # PTOK has to be khashed manually because of its explicit setting
        token_new = "5386460135176807"
        update1.params["PTOK"] = Khash.get().hash_payment_token(token_new)
        update1.params["LAST4"] = token_new[-4:]
        update1.params["FRMT"] = 'JSON'
        update1.set_khash_payment_encoding(True)
        update1.set_merchant_acknowledgment(MerchantAcknowledgment.TRUE)
        update1.set_authorization_status(AuthStatus.APPROVE)
        update1.set_avs_zip_reply(BankcardReply.MATCH)
        update1.set_avs_address_reply(BankcardReply.MATCH)
        update1.set_avs_cvv_reply(BankcardReply.MATCH)
        res = self.client.process(update1)
        self.assertIsNotNone(res)
        self.assertEqual("U", res.get_mode())
        self.assertIsNone(res.get_geox())
        self.assertIsNone(res.get_score())
        self.assertIsNone(res.get_auto())

    def test_10_mode_x_after_mode_q(self):
        """test_10_mode_x_after_mode_q
        PTOK has to be khashed manually because of
        its explicit setting"""
        res = self.client.process(self.inquiry())
        self.assertIsNotNone(res)
        transaction_id = res.get_transaction_id()
        session_id = res.get_session_id()
        order_id = res.get_order_id()
        update1 = Update()
        update1.set_mode(UpdateMode.WITH_RESPONSE)
        update1.set_transaction_id(transaction_id)
        update1.set_merchant(self.merchant_id)
        update1.set_session_id(session_id)
        update1.set_order_number(order_id)
        token_new = "5386460135176807"
        update1.set_khash_payment_encoding(self.payment.khashed)
        if self.payment.khashed:
            token_new = Khash.get().hash_payment_token(token_new)
        update1.params["PTOK"] = token_new
        update1.params["LAST4"] = token_new[-4:]
        update1.params["FRMT"] = 'JSON'
        update1.set_merchant_acknowledgment(MerchantAcknowledgment.TRUE)
        update1.set_authorization_status(AuthStatus.APPROVE)
        update1.set_avs_zip_reply(BankcardReply.MATCH)
        update1.set_avs_address_reply(BankcardReply.MATCH)
        update1.set_avs_cvv_reply(BankcardReply.MATCH)
        res = self.client.process(update1)
        self.assertIsNotNone(res)
        self.assertEqual("X", res.get_mode())
        self.assertIsNotNone(res.get_geox())
        self.assertIsNotNone(res.get_score())
        self.assertIsNotNone(res.get_auto())

    def test_11_mode_p(self):
        res = self.client.process(self.inquiry())
        self.assertIsNotNone(res)
        inq = self.inquiry()
        inq.set_request_mode(InquiryMode.PHONE)
        inq.set_anid("2085551212")
        inq.set_total(1000)
        res = self.client.process(inq)
        self.assertIsNotNone(res)
        self.assertEqual("P", res.get_mode())
        self.assertEqual("A", res.get_auto())

    def test_14_ris_q_using_payment_encoding_mask_valid(self):
        """test_14_ris_q_using_payment_encoding_mask_valid"""
        ptok_2 = "370070XXXXX9797"
        last4 = ptok_2[-4:]
        penc = 'MASK'
        res = self.client.process(self.inquiry())
        self.assertIsNotNone(res)
        inq = self.inquiry()
        inq.params['LAST4'] = last4
        inq.params['PTOK'] = ptok_2
        inq.params['PENC'] = penc
        res = self.client.process(inq)
        self.assertIsNotNone(res)
        self.assertEqual("AMEX", res.get_brand())

    def test_15_ris_q_using_payment_encoding_mask_error(self):
        """test_15_ris_q_using_payment_encoding_mask_error"""
        ptok_2 = "370070538959797"
        last4 = ptok_2[-4:]
        penc = 'MASK'
        inq = self.inquiry()
        res = self.client.process(inq)
        self.assertIsNotNone(res)
        inq.params['LAST4'] = last4
        inq.params['PTOK'] = ptok_2
        inq.params['PENC'] = penc
        res = self.client.process(inq)
        self.assertIsNotNone(res)
        self.assertEqual({
            'ERRO': 340,
            'ERROR_0':
                '340 BAD_MASK Cause: [value [%s] did not match regex '
                '/^\\d{6}X{5,9}\\d{1,4}$/], Field: [PTOK], Value: '
                '[%s]' % (ptok_2, ptok_2),
            'ERROR_COUNT': 1,
            'MODE': 'E',
            'WARNING_COUNT': 0}, res.params)


class TestRisTestSuiteKhashed(TestRisTestSuite):
    """Ris Test Suite Khashed
        default logging errors instead fo raising
        to raise errors - put raise_errors=True in Client:
        Client(url=URL_API, key=KOUNT_API_KEY,
               timeout=TIMEOUT, RAISE_ERRORS=True)
    """
    maxDiff = None

    def setUp(self):
        self.session_id = generate_unique_id()[:32]
        self.payment = CardPayment(PTOK)
        self.client = Client(self.api_url, self.api_key,
                             raise_errors=_RAISE_ERRORS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
