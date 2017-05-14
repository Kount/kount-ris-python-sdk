#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


import unittest
import logging
import os
import uuid

from request import ASTAT, BCRSTAT, INQUIRYMODE, CURRENCYTYPE, MERCHANTACKNOWLEDGMENT #, REFUNDCBSTAT, SHIPPINGTYPESTAT
from inquiry import Inquiry
from pprint import pprint
from util.payment import CardPayment
from util.cartitem import CartItem
from util.address import Address
from test_api_kount import Client
from local_settings import url_api, kountAPIkey
from settings import resource_folder, xml_filename, sdk_version
from util.xmlparser import xml_to_dict
from response import Response
from local_settings import url_api
xml_filename_path = os.path.join(os.path.dirname(__file__),
                            resource_folder, xml_filename)

initial = {'MODE':'Q',
    'Merchant (MERC)':'999666',
    'NAME':'SdkTestFirstName SdkTestLastName',
    'PTOK':'0007380568572514',
    'LAST4':'2514',
    'VERS':'0695',
    'EMAL':'sdkTest@kountsdktestdomain.com',
    'SITE':'DEFAULT',
    'FRMT':'JSON',
    'CURR':'USD',
    'TOTL':'123456',
    'CASH':'4444',
    'B2A1':'1234 North B2A1 Tree Lane South',
    'B2CI':'Albuquerque',
    'B2ST':'NM',
    'B2CC':'US',
    'B2PC':'87101',
    'B2PN':'555-867-5309',
    'S2NM':'SdkShipToFN SdkShipToLN',
    'S2EM':'sdkTestShipToEmail@kountsdktestdomain.com',
    'S2A1':'567 West S2A1 Court North',
    'S2CI':'Gnome',
    'S2ST':'AK',
    'S2CC':'US',
    'S2PC':'99762',
    'S2PN':'555-777-1212',
    'PTYP':'CARD',
    'SESS':'generate random session id - 32 character',
    'UNIQ':'truncate SESS to 20 characters',
    'ORDR':'truncate the UNIQ to 10 characters',
    'IPAD':'131.206.45.21',
    'MACK':'Y',
    'AUTH':'A',
    'AVSZ':'M',
    'AVST':'M',
    'CVVR':'M',
    'PROD_TYPE[0]':'SPORTING_GOODS',
    'PROD_ITEM[0]':'SG999999',
    'PROD_DESC[0]':'3000 CANDLEPOWER PLASMA FLASHLIGHT',
    'PROD_QUANT[0]':'2',
    'PROD_PRICE[0]':'68990',
}


RIS_ENDPOINT = url_api
MERCHANT_ID = '999666'
BILLING_ADDRESS = Address("1234 North B2A1 Tree Lane South", "", "Albuquerque", "NM", "87101", "US")
SHIPPING_ADDRESS = Address("567 West S2A1 Court North", "", "Gnome", "AK", "99762", "US") #S2A1 S2CI S2ST S2PC S2CC

def generate_unique_id():
    return str(uuid.uuid4()).replace('-', '').upper()

def default_inquiry(session_id):
    "PENC is not set"
    result = Inquiry()
    result.request_mode(INQUIRYMODE.DEFAULT)
    result.shipping_address(SHIPPING_ADDRESS)
    result.shipping_name("SdkShipToFN SdkShipToLN") #S2NM
    result.billing_address(BILLING_ADDRESS)

    result.currency_set(CURRENCYTYPE.USD)   #CURR
    result.total_set('123456') #TOTL
    result.billing_phone_number("555-867-5309") #B2PN
    result.shipping_phone_number("555-777-1212") #S2PN
    result.email_client("sdkTest@kountsdktestdomain.com")
    result.customer_name("SdkTestFirstName SdkTestLastName")
    result.unique_customer_id(session_id[:20]) #UNIQ
    result.website("DEFAULT") #SITE
    result.email_shipping("sdkTestShipToEmail@kountsdktestdomain.com")
    result.ip_address("") #IPAD
    cart_item = []
    cart_item.append(CartItem("SPORTING_GOODS", "SG999999", "3000 CANDLEPOWER PLASMA FLASHLIGHT", '2', '68990')) # PROD_TYPE[0, PROD_ITEM[0], PROD_DESC[0] PROD_QUANT[0],PROD_PRICE[0]
    result.shopping_cart(cart_item)
    result.version()
    result.version_set(sdk_version)  #0695
    result.merchant_set(MERCHANT_ID) # 999666
    payment = CardPayment("0007380568572514")
    print("payment.last4============", payment.payment_token, payment, payment.last4)
    result.payment_set(payment) #PTOK
    result.session_set(session_id) #SESS
    result.order_number(session_id[:10])  #ORDR 
    result.authorization_status(ASTAT.Approve) #AUTH
    result.avs_zip_reply(BCRSTAT.MATCH)
    result.avs_address_reply(BCRSTAT.MATCH)
    result.avs_cvv_reply(BCRSTAT.MATCH)
    result.merchant_acknowledgment_set(MERCHANTACKNOWLEDGMENT.TRUE) #"MACK"
    result.cash('4444')
    return result


class TestInquiry(unittest.TestCase):
    def setUp(self):
        session_id = generate_unique_id()
        self.result = default_inquiry(session_id = str(session_id))
        self.maxDiff = None

    def test_utilities(self):
        #~ session_id = str(uuid.uuid4())
        result = self.result
        #~ self.maxDiff = None
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
            'EMAL': 'sdkTest@kountsdktestdomain.com',
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
            'SDK_VERSION': 'Sdk-Ris-Python-%s'%sdk_version,
            'SITE': 'DEFAULT',
            'SPREMISE': '',
            'SSTREET': '',
            'TOTL': '123456',
            'VERS': sdk_version,
            }
        actual = result.params
        self.assertIn(expected['SDK_VERSION'], actual['SDK_VERSION'] )
        del(actual['UNIQ'])
        del(actual['IPAD'])
        del(actual['SDK_VERSION'])
        del(expected['SDK_VERSION'])
        del(actual['SESS'])
        del(actual['ORDR'])
        self.assertEqual(actual, expected)

class TestRisTestSuite(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None
        #~ self.reset_id_and_inquiry
        self.session_id = generate_unique_id()[:32]
        result = default_inquiry(self.session_id)
        self.inq = result
        self.server_url = RIS_ENDPOINT
        self.client = Client(url_api, kountAPIkey)
        self.result = default_inquiry(session_id = self.session_id)
        self.xml_to_dict1, self.required_field_names, self.notrequired_field_names = xml_to_dict(xml_filename_path)
        self.log()

    def log(self):
        self.logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
                '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("running %s"%self._testMethodName)
    
    def reset_id_and_inquiry(self):
        self.session_id = generate_unique_id()
        result = default_inquiry(self.session_id)
        self.inq = result

    def test_1_ris_q_1_item_required_field_1_rule_review(self):
        res = self.client.process(params=self.inq.params)
        res_json = res.json()
        self.assertIsNotNone(res_json)
        rr = Response(res)
        self.assertEqual("R", res_json["AUTO"])
        self.assertEqual(0, res.json()["WARNING_COUNT"])
        self.assertEqual( {'1024842': 'Review if order total > $1000 USD'}, rr.get_rules_triggered())
        self.assertEqual(res.json()["SESS"], res_json["SESS"])
        self.assertEqual(res.json()["SESS"][:10], res_json["ORDR"])

    def test_2_ris_q_multi_cart_items2optional_fields2rules_decline(self):
        self.maxDiff = None
        self.inq.user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36")
        self.inq.total_set(123456789)
        cart_item = []
        cart_item.append(CartItem("cart item type 0", "cart item 0", "cart item 0 description", 10, 1000)) # PROD_TYPE[0, PROD_ITEM[0], PROD_DESC[0] PROD_QUANT[0],PROD_PRICE[0]
        cart_item.append(CartItem("cart item type 1", "cart item 1", "cart item 1 description", 11, 1001)) # PROD_TYPE[0, PROD_ITEM[0], PROD_DESC[0] PROD_QUANT[0],PROD_PRICE[0]
        cart_item.append(CartItem("cart item type 2", "cart item 2", "cart item 1 description", 12, 1002)) # PROD_TYPE[0, PROD_ITEM[0], PROD_DESC[0] PROD_QUANT[0],PROD_PRICE[0]
        self.inq.shopping_cart(cart_item)
        res = self.client.process(params=self.inq.params)
        res_json = res.json()
        self.assertIsNotNone(res_json)
        self.logger.debug(res_json)
        rr = Response(res)
        self.assertEqual("D", res_json["AUTO"])
        self.assertEqual(0, res.json()["WARNING_COUNT"])
        #~ print(rr.get_rules_triggered())
        self.assertEqual({'1024842': 'Review if order total > $1000 USD',
                          '1024844': 'Decline if order total > $1000000 USD'},
                          rr.get_rules_triggered())

    def test_3_ris_q_with_user_defined_fields(self):
        self.maxDiff = None
        self.inq.params["UDF[ARBITRARY_ALPHANUM_UDF]"] = "alphanumeric trigger value"
        self.inq.params["UDF[ARBITRARY_NUMERIC_UDF]"] = "777"
        res = self.client.process(params=self.inq.params)
        res_json = res.json()
        self.assertIsNotNone(res_json)
        self.logger.debug(res_json)
        rr = Response(res)
        self.assertEqual("R", res_json["AUTO"])
        self.assertEqual(3, res_json["RULES_TRIGGERED"])
        self.assertEqual(0, res.json()["WARNING_COUNT"])
        #~ print(rr.get_rules_triggered())
        self.assertEqual({'1025086': 'review if ARBITRARY_ALPHANUM_UDF contains "trigger"',
                        '1024842': 'Review if order total > $1000 USD',
                        '1025088': 'review if ARBITRARY_NUMERIC_UDF == 777'},
                        rr.get_rules_triggered())
        self.logger.debug("[alpha-numeric rule] triggered")
        self.logger.debug("[numeric rule] triggered")

    def test_4_ris_q_hard_error_expected(self):
        self.maxDiff = None
        #~ overwrite the PTOK value to induce an error in the RIS
        self.inq.params["PTOK"] = "BADPTOK"
        res = self.client.process(params=self.inq.params)
        res_json = res.json()
        self.assertIsNotNone(res_json)
        self.logger.debug(res_json)
        rr = Response(res)
        #~ print('res_json44444444444444444444444444444444444')
        #~ pprint(res_json)
        #~ 'WARNING_0': '399 BAD_OPTN Cause: [LAST4 does not match last 4 characters in '
                     #~ 'payment token], Field: [LAST4], Value: [2514]',
        self.assertEqual("E", rr.params['MODE'])
        self.assertNotEqual(['332 BAD_CARD Cause: [Too short], Field: [PTOK], Value: [hidden]'], rr.get_errors())
        self.assertEqual('332 BAD_CARD Cause: [PTOK invalid format], Field: [PTOK], Value: [hidden]', rr.get_errors())
        self.assertEqual(332, rr.params['ERRO'])
        self.assertEqual(0, rr.params['WARNING_COUNT'])

    def test_5_ris_q_warning_approved(self):
        self.maxDiff = None
        self.inq.params["TOTL"] = "1000"
        self.inq.params["UDF[UDF_DOESNOTEXIST]"] = "throw a warning please!"
        res = self.client.process(params=self.inq.params)
        res_json = res.json()
        self.assertIsNotNone(res_json)
        self.logger.debug(res_json)
        rr = Response(res)
        self.assertEqual("A", rr.params['AUTO'])
        self.assertEqual(2,res.json()["WARNING_COUNT"])
        self.assertEqual(rr.params['WARNING_0'], '399 BAD_OPTN Field: [UDF], Value: [UDF_DOESNOTEXIST=>throw a warning please!]')
        self.assertEqual(rr.params['WARNING_1'], '399 BAD_OPTN Field: [UDF], Value: [The label [UDF_DOESNOTEXIST] is not defined for merchant ID [999666].]')
        self.logger.debug("[throw a warning please] found")
        self.logger.debug("[not defined for merchant] found")

    def test_6_ris_q_hard_oft_errors_expected(self):
        self.maxDiff = None
        #~ self.logger.debug("running testRisQHardSoftErrorsExpected_6");
        self.inq.params["PTOK"] = "BADPTOK"
        self.inq.params["UDF[UDF_DOESNOTEXIST]"] = "throw a warning please!"
        res = self.client.process(params=self.inq.params)
        res_json = res.json()
        self.assertIsNotNone(res_json)
        rr = Response(res)
        print('res_json44444444444444444444444444444444444')
        pprint(res_json)
        self.logger.debug(res_json)
        self.assertEqual("E", rr.params['MODE'])
        self.assertEqual(332, rr.params['ERRO'])
        self.assertEqual(1, rr.params['ERROR_COUNT'])
        self.assertEqual("332 BAD_CARD Cause: [PTOK invalid format], Field: [PTOK], Value: [hidden]", rr.get_errors())
        self.assertEquals("399 BAD_OPTN Field: [UDF], Value: [UDF_DOESNOTEXIST=>throw a 'warning please!]", rr.params["WARNING_0"])
        self.assertEquals("399 BAD_OPTN Field: [UDF], Value: [The label [UDF_DOESNOTEXIST] is not defined for merchant ID [999666].]", rr.params["WARNING_2"])
        self.assertEqual(2, res.json()["WARNING_COUNT"])
        self.logger.debug("[throw a warning please] found")
        self.logger.debug("[not defined for merchant] found")

    def test_7_ris_w2_kc_rules_review(self):
        self.maxDiff = None
        print(INQUIRYMODE.WITHTHRESHOLDS)
        self.inq.request_mode(INQUIRYMODE.WITHTHRESHOLDS)
        self.inq.total_set(10001)
        self.inq.kount_central_customer_id("KCentralCustomerOne")
        res = self.client.process(params=self.inq.params)
        res_json = res.json()
        self.assertIsNotNone(res_json)
        rr = Response(res)
        self.logger.debug(res_json)
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
        self.logger.debug("[%s] found"%events['KC_EVENT_1_CODE'])
        self.logger.debug("[%s] found"%events['KC_EVENT_2_CODE'])
        #~ 'KC_EVENT_0_DECISION'
"""
	@Test
	public void testRisJOneKountCentralRuleDecline_8() throws RisException {
		logger.debug("running testRisJOneKountCentralRuelDecline_8");
		inq.setMode(InquiryMode.KC_QUICK_INQUIRY_J);
		inq.setTotal(1000);
		inq.setKcCustomerId("KCentralCustomerDeclineMe");
		
		Response response = client.process(inq);
		logger.trace(response.toString());
		
		assertEquals("D", response.getKcDecision());
		assertEquals(0, response.getKcWarningCount());
		assertEquals(1, response.getKcEventCount());
		
		assertEquals("D", response.getKcEvents().get(0).getDecision());
		assertEquals("orderTotalDecline", response.getKcEvents().get(0).getCode());
	}
	
	@Test
	public void testModeUAfterModeQ_9() throws RisException, NoSuchAlgorithmException {
		logger.debug("running testModeUAfterModeQ_9");
		
		Response response = client.process(inq);
		logger.trace(response.toString());
		
		String transactionId = response.getTransactionId();
		String sessionId = response.getSessionId();
		String orderId = response.getOrderNumber();
		
		Update update = new Update();
		update.setMode(UpdateMode.NO_RESPONSE);
		update.setVersion("0695");
		update.setTransactionId(transactionId);
		update.setMerchantId(Utilities.MERCHANT_ID);
		update.setSessionId(sessionId);
		update.setOrderNumber(orderId);
		// PTOK has to be khashed manually because of its explicit setting
		update.setParm("PTOK", Khash.hashPaymentToken("5386460135176807"));
		update.setParm("LAST4", "6807");
		update.setMerchantAcknowledgment(MerchantAcknowledgment.YES);
		update.setAuthorizationStatus(AuthorizationStatus.APPROVED);
		update.setAvsZipReply(BankcardReply.MATCH);
		update.setAvsAddressReply(BankcardReply.MATCH);
		update.setCvvReply(BankcardReply.MATCH);
		
		Response updateResponse = client.process(update);
		logger.trace(updateResponse.toString());

		assertEquals("U", updateResponse.getMode());
		assertEquals(transactionId, updateResponse.getTransactionId());
		assertEquals(sessionId, updateResponse.getSessionId());
		
		assertNull(updateResponse.getAuto());
		assertNull(updateResponse.getScore());
		assertNull(updateResponse.getGeox());
	}
	
	@Test
	public void testModeXAfterModeQ_10() throws RisException, NoSuchAlgorithmException {
		logger.debug("running testModeXAfterModeQ_10");
		
		Response response = client.process(inq);
		logger.trace(response.toString());
		
		String transactionId = response.getTransactionId();
		String sessionId = response.getSessionId();
		String orderId = response.getOrderNumber();
		
		Update update = new Update();
		update.setMode(UpdateMode.WITH_RESPONSE);
		update.setVersion("0695");
		update.setMerchantId(Utilities.MERCHANT_ID);
		update.setTransactionId(transactionId);
		update.setSessionId(sessionId);
		update.setOrderNumber(orderId);
		// PTOK has to be khashed manually because of its explicit setting
		update.setParm("PTOK", Khash.hashPaymentToken("5386460135176807"));
		update.setParm("LAST4", "6807");
		update.setMerchantAcknowledgment(MerchantAcknowledgment.YES);
		update.setAuthorizationStatus(AuthorizationStatus.APPROVED);
		update.setAvsZipReply(BankcardReply.MATCH);
		update.setAvsAddressReply(BankcardReply.MATCH);
		update.setCvvReply(BankcardReply.MATCH);
		
		Response updateResponse = client.process(update);
		logger.trace(updateResponse.toString());
		
		assertEquals("X", updateResponse.getMode());
		assertEquals(transactionId, updateResponse.getTransactionId());
		assertEquals(sessionId, updateResponse.getSessionId());
		assertEquals(orderId, updateResponse.getOrderNumber());
		
		assertNotNull(updateResponse.getAuto());
		assertNotNull(updateResponse.getScore());
		assertNotNull(updateResponse.getGeox());
	}
	
	@Test
	public void testModeP_11() throws RisException {
		logger.debug("running testModeP_11");;
		
		inq.setMode(InquiryMode.PHONE_ORDER);
		inq.setAnid("2085551212");
		inq.setTotal(1000);
		
		Response response = client.process(inq);
		logger.trace(response.toString());
		
		assertEquals("P", response.getMode());
		assertEquals("A", response.getAuto());

"""
if __name__ == "__main__":
    unittest.main(
        #~ defaultTest = "TestRisTestSuite.test_ris_q_1_item_required_field_1_rule_review_1"
        defaultTest = "TestRisTestSuite.test_7_ris_w2_kc_rules_review"
        #~ defaultTest = "TestInquiry"
        )
