#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""Test Cases from sdk documentation"""

import unittest
import os
import uuid

from request import (ASTAT, BCRSTAT, INQUIRYMODE,
                     CURRENCYTYPE, MERCHANTACKNOWLEDGMENT)
from inquiry import Inquiry
from update import Update, UPDATEMODE
from util.khash import Khash
from util.payment import CardPayment
from util.cartitem import CartItem
from util.address import Address
from util.xmlparser import xml_to_dict

from client import Client
from local_settings import (url_api, url_api_beta, kount_api_key,
                            kount_api_key999667, raise_errors)
from settings import resource_folder, xml_filename, sdk_version
from response import Response
from util.ris_validation_exception import RisValidationException


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

xml_filename_path = os.path.join(os.path.dirname(__file__),
                            resource_folder, xml_filename)

RIS_ENDPOINT = url_api
RIS_ENDPOINT_BETA = url_api_beta
MERCHANT_ID = '999666'
MERCHANT_ID_999667 = '999667'
EMAIL_CLIENT = "sdkTest@kountsdktestdomain.com"
BILLING_ADDRESS = Address("1234 North B2A1 Tree Lane South",
                          "", "Albuquerque", "NM", "87101", "US")
SHIPPING_ADDRESS = Address("567 West S2A1 Court North", "",
                           "Gnome", "AK", "99762", "US")
PTOK = "0007380568572514"


def generate_unique_id():
    "unique session id"
    return str(uuid.uuid4()).replace('-', '').upper()


def default_inquiry(session_id, merchant_id, email_client, ptok):
    "default_inquiry, PENC is not set"
    result = Inquiry()
    result.request_mode(INQUIRYMODE.DEFAULT)
    result.shipping_address(SHIPPING_ADDRESS)
    result.shipping_name("SdkShipToFN SdkShipToLN") #S2NM
    result.billing_address(BILLING_ADDRESS)
    result.currency_set(CURRENCYTYPE.USD)   #CURR
    result.total_set('123456') #TOTL
    result.billing_phone_number("555-867-5309") #B2PN
    result.shipping_phone_number("555-777-1212") #S2PN
    result.email_client(email_client)
    result.customer_name("SdkTestFirstName SdkTestLastName")
    result.unique_customer_id(session_id[:20]) #UNIQ
    result.website("DEFAULT") #SITE
    result.email_shipping("sdkTestShipToEmail@kountsdktestdomain.com")
    result.ip_address("4.127.51.215") #IPAD
    cart_item = []
    cart_item.append(CartItem("SPORTING_GOODS", "SG999999",
                              "3000 CANDLEPOWER PLASMA FLASHLIGHT",
                              '2', '68990'))
    result.shopping_cart(cart_item)
    result.version()
    result.version_set(sdk_version)  #0695
    result.merchant_set(merchant_id) # 999666
    #~ payment = CardPayment(PTOK)
    payment = CardPayment(ptok)
    result.payment_set(payment) #PTOK
    #~ result.params["PTOK"] = Khash.hash_payment_token(PTOK)
    result.session_set(session_id) #SESS
    result.order_number(session_id[:10])  #ORDR
    result.authorization_status(ASTAT.Approve) #AUTH
    result.avs_zip_reply(BCRSTAT.MATCH)
    result.avs_address_reply(BCRSTAT.MATCH)
    result.avs_cvv_reply(BCRSTAT.MATCH)
    result.merchant_acknowledgment_set(MERCHANTACKNOWLEDGMENT.TRUE) #"MACK"
    result.cash('4444')
    #~ result.params["PENC"] = "KHASH"
    return result


class TestInquiry(unittest.TestCase):
    "Inquiry class tests"
    def setUp(self):
        session_id = generate_unique_id()
        self.result = default_inquiry(
            session_id=str(session_id),
            merchant_id=MERCHANT_ID,
            email_client=EMAIL_CLIENT, ptok=PTOK)
        self.maxDiff = None

    def test_utilities(self):
        "test_utilities"
        result = self.result
        expected = {
            'ANID': '',
            'AUTH': 'A',
            'AVST': 'M',
            'AVSZ': 'M',
            'B2A1': '1234 North B2A1 Tree Lane South',
            'B2A2': '',
            'B2CC': 'US',
            'B2CI': 'Albuquerque',
            'B2PC': '87101',
            'B2PN': '555-867-5309',
            'B2ST': 'NM',
            'BPREMISE': '',
            'BSTREET': '',
            'CASH': '4444',
            'CURR': 'USD',
            'CVVR': 'M',
            'EMAL': EMAIL_CLIENT,
            'FRMT': 'JSON',
            #~ 'IPAD': '131.206.45.21',
            'LAST4': '2514',
            'MACK': 'Y',
            'MERC': '999666',
            'MODE': 'Q',
            'NAME': 'SdkTestFirstName SdkTestLastName',
            #~ 'PENC': '',
            'PROD_DESC[0]': '3000 CANDLEPOWER PLASMA FLASHLIGHT',
            'PROD_ITEM[0]': 'SG999999',
            'PROD_PRICE[0]': '68990',
            'PROD_QUANT[0]': '2',
            'PROD_TYPE[0]': 'SPORTING_GOODS',
            'PTOK': '0007380568572514',
            'PTYP': 'CARD',
            'S2A1': '567 West S2A1 Court North',
            'S2A2': '',
            'S2CC': 'US',
            'S2CI': 'Gnome',
            'S2EM': 'sdkTestShipToEmail@kountsdktestdomain.com',
            'S2NM': 'SdkShipToFN SdkShipToLN',
            'S2PC': '99762',
            'S2PN': '555-777-1212',
            'S2ST': 'AK',
            'SDK': 'CUST',
            'SDK_VERSION': 'Sdk-Ris-Python-%s' % sdk_version,
            'SITE': 'DEFAULT',
            'SPREMISE': '',
            'SSTREET': '',
            'TOTL': '123456',
            'VERS': sdk_version,
            }
        actual = result.params
        self.assertIn(expected['SDK_VERSION'], actual['SDK_VERSION'])
        del actual['UNIQ']
        del actual['IPAD']
        del actual['SDK_VERSION']
        del expected['SDK_VERSION']
        del actual['SESS']
        del actual['ORDR']
        self.assertEqual(actual, expected)


class TestRisTestSuite(unittest.TestCase):
    """Ris Test Suite
        default logging errors instead fo raising
        to raise errors - put raise_errors=True in Client:
        Client(url=url_api, key=kount_api_key, raise_errors=True)
    """
    def setUp(self):
        self.maxDiff = None
        self.session_id = generate_unique_id()[:32]
        self.client = Client(RIS_ENDPOINT_BETA, kount_api_key)
        self.inq = default_inquiry(session_id=self.session_id,
                                   merchant_id=MERCHANT_ID,
                                   email_client=EMAIL_CLIENT,
                                   ptok=PTOK)
        self.xml_to_dict1, self.required_field_names,\
            self.notrequired_field_names = \
            xml_to_dict(xml_filename_path)

    def test_1_ris_q_1_item_required_field_1_rule_review(self):
        "test_1_ris_q_1_item_required_field_1_rule_review"
        res_json = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res_json)
        rr = Response(res_json)
        self.assertEqual("R", res_json["AUTO"])
        self.assertEqual(0, res_json["WARNING_COUNT"])
        expected = ['Review if order total > $1000 USD']
        actual = sorted(rr.get_rules_triggered().values())
        self.assertEqual(expected, actual)
        self.assertEqual(res_json["SESS"], res_json["SESS"])
        self.assertEqual(res_json["SESS"][:10], res_json["ORDR"])

    def test_2_ris_q_multi_cart_items2optional_fields2rules_decline(self):
        """test_2_ris_q_multi_cart_items2optional_fields2rules_decline
        cart_item - PROD_TYPE[0, PROD_ITEM[0], PROD_DESC[0]
                    PROD_QUANT[0],PROD_PRICE[0]"""
        self.inq.user_agent(
            "Mozilla/5.0 (Macintosh; "\
            "Intel Mac OS X 10_9_5) AppleWebKit/537.36 "\
            "(KHTML, like Gecko) Chrome/37.0.2062.124 "\
            "Safari/537.36")
        self.inq.total_set(123456789)
        cart_item = []
        cart_item.append(CartItem(
            "cart item type 0", "cart item 0",
            "cart item 0 description", 10, 1000))
        cart_item.append(CartItem(
            "cart item type 1", "cart item 1",
            "cart item 1 description", 11, 1001))
        cart_item.append(CartItem(
            "cart item type 2", "cart item 2",
            "cart item 1 description", 12, 1002))
        self.inq.shopping_cart(cart_item)
        res_json = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res_json)
        rr = Response(res_json)
        self.assertEqual("D", res_json["AUTO"])
        self.assertEqual(0, res_json["WARNING_COUNT"])
        expected = sorted(
            {'1024842': 'Review if order total > $1000 USD',
             '1024844': 'Decline if order total > $1000000 USD'}.values())
        actual = sorted(rr.get_rules_triggered().values())
        self.assertEqual(expected, actual)

    def test_3_ris_q_with_user_defined_fields(self):
        "test_3_ris_q_with_user_defined_fields"
        udf1 = "ARBITRARY_ALPHANUM_UDF"
        udf2 = "ARBITRARY_NUMERIC_UDF"
        self.inq.params["UDF[%s]" % udf1] = \
        "alphanumeric trigger value"
        self.inq.params["UDF[%s]" % udf2] = "777"
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual("R", res["AUTO"])
        self.assertEqual(3, res["RULES_TRIGGERED"])
        self.assertEqual(0, res["WARNING_COUNT"])
        expected = sorted(
            {'1025086': 'review if %s contains "trigger"' % udf1,
             '1024842': 'Review if order total > $1000 USD',
             '1025088': "review if %s == 777" % udf2}.values())
        actual = sorted(rr.get_rules_triggered().values())
        self.assertEqual(expected, actual)

    def test_4_ris_q_hard_error_expected(self):
        """test_4_ris_q_hard_error_expected,
        overwrite the PTOK value to induce an error in the RIS"""
        self.maxDiff = None
        self.inq.params["PENC"] = "KHASH"
        self.inq.params["PTOK"] = "BADPTOK"
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual(
            ["332 BAD_CARD Cause: [PTOK invalid format], "
             "Field: [PTOK], Value: [hidden]"],
            rr.get_errors())
        self.assertEqual("E", rr.params['MODE'])
        self.assertEqual(332, rr.params['ERRO'])
        self.assertEqual(0, rr.params['WARNING_COUNT'])

    def test_5_ris_q_warning_approved(self):
        "test_5_ris_q_warning_approved"
        self.inq.params["TOTL"] = "1000"
        label = "UDF_DOESNOTEXIST"
        mesg = "throw a warning please!"
        self.inq.params["UDF[%s]" % label] = mesg
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual("A", rr.params['AUTO'])
        self.assertEqual(2, res["WARNING_COUNT"])
        self.assertEqual(rr.params['WARNING_0'],
                         "399 BAD_OPTN Field: [UDF], Value: "
                         "[%s=>%s]" % (label, mesg))
        self.assertEqual(rr.params['WARNING_1'],
                         "399 BAD_OPTN Field: [UDF], Value: "
                         "[The label [%s]"
                         " is not defined for merchant ID [%s].]" % (
                             label, MERCHANT_ID))
        #~ self.logger.debug("[throw a warning please] found")
        #~ self.logger.debug("[not defined for merchant] found")

    def test_6_ris_q_hard_soft_errors_expected(self):
        "test_6_ris_q_hard_soft_errors_expected"
        self.maxDiff = None
        self.inq.params["PENC"] = "KHASH"
        self.inq.params["PTOK"] = "BADPTOK"
        label = "UDF_DOESNOTEXIST"
        mess = "throw a warning please!"
        self.inq.params["UDF[%s]" % label] = mess
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual("E", rr.params['MODE'])
        self.assertEqual(332, rr.params['ERRO'])
        self.assertEqual(1, rr.params['ERROR_COUNT'])
        self.assertEqual(
            [("332 BAD_CARD Cause: [PTOK invalid format], "
              "Field: [PTOK], Value: [hidden]")],
            rr.get_errors())
        self.assertEqual(
            "399 BAD_OPTN Field: [UDF], Value: [%s=>%s]"
            % (label, mess),
            rr.params["WARNING_0"])
        self.assertEqual(
            "399 BAD_OPTN Field: [UDF], Value: [The label [%s] "
            "is not defined for merchant ID [%s].]"
            % (label, MERCHANT_ID), rr.params["WARNING_1"])
        self.assertEqual(2, res["WARNING_COUNT"])

    def test_7_ris_w2_kc_rules_review(self):
        "test_7_ris_w2_kc_rules_review"
        self.inq.request_mode(INQUIRYMODE.WITHTHRESHOLDS)
        self.inq.total_set(10001)
        self.inq.kount_central_customer_id("KCentralCustomerOne")
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        #~ self.logger.debug(res_json)
        self.assertEqual(rr.params["KC_DECISION"], 'R')
        self.assertEqual(rr.params["KC_WARNING_COUNT"], 0)
        self.assertEqual(rr.params["KC_TRIGGERED_COUNT"], 2)
        events = rr.get_kc_events()
        self.assertEqual(events, {
            'KC_EVENT_2_CODE': 'orderTotalReview',
            'KC_EVENT_1_CODE': 'billingToShippingAddressReview',
            'KC_EVENT_2_EXPRESSION': '10001 > 10000',
            'KC_EVENT_2_DECISION': 'R',
            'KC_EVENT_1_EXPRESSION': '5053 > 1',
            'KC_EVENT_1_DECISION': 'R'}
                        )

    def test_8_ris_j_1_kount_central_rule_decline(self):
        "test_8_ris_j_1_kount_central_rule_decline"
        self.maxDiff = None
        self.inq.request_mode(INQUIRYMODE.JUSTTHRESHOLDS)
        self.inq.total_set(1000)
        self.inq.kount_central_customer_id("KCentralCustomerDeclineMe")
        if not raise_errors:
            res = self.client.process(params=self.inq.params)
            self.assertIsNotNone(res)
            rr = Response(res)
            self.assertEqual("D", rr.params['KC_DECISION'])
            self.assertEqual(0, rr.params['KC_WARNING_COUNT'])
            self.assertEqual(1, rr.get_kc_events_count())
            self.assertEqual("orderTotalDecline",
                             rr.get_kc_events()['KC_EVENT_1_CODE'])
        else:
            self.assertRaises(RisValidationException, 
                                         self.client.process, self.inq.params)

    def test_9_mode_u_after_mode_q(self):
        "test_9_mode_u_after_mode_q"
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        transaction_id = rr.params['TRAN']
        session_id = rr.params['SESS']
        order_id = rr.params['ORDR']
        update1 = Update()
        update1.set_mode(UPDATEMODE.NO_RESPONSE)
        update1.version_set(sdk_version)
        update1.set_transaction_id(transaction_id)
        update1.merchant_set(MERCHANT_ID)
        update1.session_set(session_id)
        update1.order_number(order_id)
        #~ // PTOK has to be khashed manually because of its explicit setting
        token_new = "5386460135176807"
        update1.params["PTOK"] = Khash.hash_payment_token(token_new)
        update1.params["LAST4"] = token_new[-4:]
        update1.params["FRMT"] = 'JSON'
        update1.merchant_acknowledgment_set(MERCHANTACKNOWLEDGMENT.TRUE)
        update1.authorization_status(ASTAT.Approve)
        update1.avs_zip_reply(BCRSTAT.MATCH)
        update1.avs_address_reply(BCRSTAT.MATCH)
        update1.avs_cvv_reply(BCRSTAT.MATCH)
        res = self.client.process(params=update1.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual("U", rr.params['MODE'])
        self.assertNotIn("GEOX", rr.params)
        self.assertNotIn("SCOR", rr.params)
        self.assertNotIn("AUTO", rr.params)

    def test_10_mode_x_after_mode_q(self):
        """test_10_mode_x_after_mode_q
        PTOK has to be khashed manually because of
        its explicit setting"""
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        transaction_id = rr.params['TRAN']
        session_id = rr.params['SESS']
        order_id = rr.params['ORDR']
        update1 = Update()
        update1.set_mode(UPDATEMODE.WITH_RESPONSE)
        update1.version_set(sdk_version)
        update1.set_transaction_id(transaction_id)
        update1.merchant_set(MERCHANT_ID)
        update1.session_set(session_id)
        update1.order_number(order_id)
        token_new = "5386460135176807"
        update1.params["PTOK"] = Khash.hash_payment_token(token_new)
        update1.params["LAST4"] = token_new[-4:]
        update1.params["FRMT"] = 'JSON'
        update1.merchant_acknowledgment_set(MERCHANTACKNOWLEDGMENT.TRUE)
        update1.authorization_status(ASTAT.Approve)
        update1.avs_zip_reply(BCRSTAT.MATCH)
        update1.avs_address_reply(BCRSTAT.MATCH)
        update1.avs_cvv_reply(BCRSTAT.MATCH)
        res = self.client.process(params=update1.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual("X", rr.params['MODE'])
        self.assertIn("GEOX", rr.params)
        self.assertIn("SCOR", rr.params)
        self.assertIn("AUTO", rr.params)

    def test_11_mode_p(self):
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.inq.request_mode(INQUIRYMODE.PHONE)
        self.inq.anid("2085551212")
        self.inq.total_set(1000)
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual("P", rr.params['MODE'])
        self.assertEqual("A", rr.params['AUTO'])

    def test_14_ris_q_using_payment_encoding_mask_valid(self):
        "test_14_ris_q_using_payment_encoding_mask_valid"
        ptok_2 = "370070XXXXX9797"
        last4 = ptok_2[-4:]
        penc = 'MASK'
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.inq.params['LAST4'] = last4
        self.inq.params['PTOK'] = ptok_2
        self.inq.params['PENC'] = penc
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)

        rr = Response(res)
        self.assertEqual("AMEX", rr.params['BRND'])

    def test_15_ris_q_using_payment_encoding_mask_error(self):
        "test_15_ris_q_using_payment_encoding_mask_error"
        ptok_2 = "370070538959797"
        last4 = ptok_2[-4:]
        penc = 'MASK'
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        self.inq.params['LAST4'] = last4
        self.inq.params['PTOK'] = ptok_2
        self.inq.params['PENC'] = penc
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual({
            'ERRO': 340,
            'ERROR_0':
                '340 BAD_MASK Cause: [value [%s] did not match regex '
                '/^\\d{6}X{5,9}\\d{1,4}$/], Field: [PTOK], Value: '
                '[%s]' % (ptok_2, ptok_2),
            'ERROR_COUNT': 1,
            'MODE': 'E',
            'WARNING_COUNT': 0}, rr.params)


class TestBasicConnectivity(unittest.TestCase):
    "Test Basic Connectivity"
    def setUp(self):
        self.maxDiff = None
        self.session_id = generate_unique_id()[:32]
        email_client = 'predictive@kount.com'
        self.inq = default_inquiry(self.session_id,
                                   MERCHANT_ID_999667,
                                   email_client, ptok=PTOK)
        self.inq.params["MERC"] = MERCHANT_ID_999667
        self.client = Client(RIS_ENDPOINT_BETA, kount_api_key999667)
        self.xml_to_dict1, self.req, self.notreq = xml_to_dict(
            xml_filename_path)

    def test_12_expected_score(self):
        "test_12_expected_score"
        self.inq.params["UDF[~K!_SCOR]"] = '42'
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual("42", rr.params['SCOR'])

    def test_13_expected_decision(self):
        "test_13_expected_decision"
        self.inq.params["UDF[~K!_AUTO]"] = 'R'
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        self.assertEqual("R", res["AUTO"])

    def test_17_cyrillic(self):
        "test_17_cyrillic"
        bad = 'Сирма :ы№'
        self.inq.params["S2NM"] = bad
        self.inq.params["EMAL"] = bad
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        actual = "321 BAD_EMAL Cause: [[%s is an invalid email address]"\
                 ", Field: [EMAL], Value: [%s]" % (bad, bad)
        self.assertEqual({
            u'ERRO': 321,
            u'ERROR_0': actual,
            u'ERROR_COUNT': 1, 'MODE': 'E', 'WARNING_COUNT': 0}, res)

    def test_16_expected_geox(self):
        "test_16_expected_geox"
        self.inq.params["UDF[~K!_SCOR]"] = '42'
        self.inq.params["UDF[~K!_AUTO]"] = 'D'
        self.inq.params["UDF[~K!_GEOX]"] = 'NG'
        res = self.client.process(params=self.inq.params)
        self.assertIsNotNone(res)
        rr = Response(res)
        self.assertEqual("D", res["AUTO"])
        self.assertEqual("NG", res["GEOX"])
        self.assertEqual("42", rr.params['SCOR'])


if __name__ == "__main__":
    unittest.main(
        #~ defaultTest = "TestBasicConnectivity.test_17_cyrillic"
        )
