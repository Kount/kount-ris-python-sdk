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
from request import ASTAT, BCRSTAT, CURRENCYTYPE #, MERCHANTACKNOWLEDGMENT, REFUNDCBSTAT, SHIPPINGTYPESTAT, INQUIRYMODE
from inquiry import Inquiry
from pprint import pprint
import uuid
from util.payment import CardPayment
from util.cartitem import CartItem
from util.address import Address
from test_api_kount import Client
from local_settings import url_api, kountAPIkey


class Utilities(unittest.TestCase):
    RIS_ENDPOINT = "https://risk.test.kount.net"
    MERCHANT_ID = 999666
    BILLING_ADDRESS = Address("1234 North B2A1 Tree Lane South", None, "Albuquerque", "NM", "87101", "US")
    SHIPPING_ADDRESS = Address("567 West S2A1 Court North", None, "Gnome", "AK", "99762", "US")

    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4())

    @staticmethod
    def default_inquiry(session_id):
        result = Inquiry()
        #~ inquiry_mode = INQUIRYMODE.DEFAULT
        result.shipping_address(Utilities.SHIPPING_ADDRESS)
        result.shipping_name("SdkShipToFN SdkShipToLN")
        result.billing_address(Utilities.BILLING_ADDRESS)
        unique_id = session_id[:21]  
        result.currency_set(CURRENCYTYPE.USD)
        result.total_set(123456)
        result.cash(4444)
        result.billing_phone_number("555-867-5309")
        result.shipping_phone_number("555-777-1212")
        result.email_client("sdkTest@kountsdktestdomain.com")
        result.customer_name("SdkTestFirstName SdkTestLastName")
        result.unique_customer_id(unique_id)
        result.website("DEFAULT")
        result.email_shipping("sdkTestShipToEmail@kountsdktestdomain.com")
        result.ip_address("131.206.45.21")
        cart_item = []
        cart_item.append(CartItem("SPORTING_GOODS", "SG999999", "3000 CANDLEPOWER PLASMA FLASHLIGHT", 2, 68990))
        result.shopping_cart(cart_item)
        result.version("1.0.0")
        result.merchant_set(Utilities.MERCHANT_ID)
        payment = CardPayment("0007380568572514")
        result.payment_set(payment)
        result.session_set(session_id)
        order_id = session_id[:11]
        result.order_number(order_id)
        result.merchant_acknowledgment_set("YES")
        result.authorization_status(ASTAT.Approve)
        result.avs_zip_reply(BCRSTAT.MATCH)
        result.avs_address_reply(BCRSTAT.MATCH)
        result.avs_cvv_reply(BCRSTAT.MATCH)
        return result


class TestInquiry(unittest.TestCase):
    def setUp(self):
        session_id = Utilities.generate_unique_id()
        self.result = Utilities.default_inquiry(session_id = session_id)

    def test_utilities(self):
        #~ session_id = str(uuid.uuid4())
        result = self.result
        #~ print(112221, result.params)
        #~ self.maxDiff = None
        expected = {'AUTH': 'A',
            'AVST': 'M',
            'AVSZ': 'M',
            'B2A1': '1234 North B2A1 Tree Lane South',
            'B2A2': None,
            'B2CC': 'US',
            'B2CI': 'Albuquerque',
            'B2PC': '87101',
            'B2PN': '555-867-5309',
            'B2ST': 'NM',
            'BPREMISE': '',
            'BSTREET': '',
            'CURR': 'USD',
            'CVVR': 'M',
            'EMAL': 'sdkTest@kountsdktestdomain.com',
            'IPAD': '131.206.45.21',
            'LAST4': '2514',
            'MACK': 'Y',
            'MERC': 999666,
            'NAME': 'SdkTestFirstName SdkTestLastName',
            'PENC': '',
            'PROD_DESC[0]': '3000 CANDLEPOWER PLASMA FLASHLIGHT',
            'PROD_ITEM[0]': 'SG999999',
            'PROD_PRICE[0]': 68990,
            'PROD_QUANT[0]': 2,
            'PROD_TYPE[0]': 'SPORTING_GOODS',
            'PTOK': '0007380568572514',
            'PTYP': 'CARD',
            'S2A1': '567 West S2A1 Court North',
            'S2A2': None,
            'S2CC': 'US',
            'S2CI': 'Gnome',
            'S2EM': 'sdkTestShipToEmail@kountsdktestdomain.com',
            'S2NM': 'SdkShipToFN SdkShipToLN',
            'S2PC': '99762',
            'S2PN': '555-777-1212',
            'S2ST': 'AK',
            'SDK': 'Python 3.6',
            'SDK_VERSION': 'Sdk-Ris-Python-1.0.0',
            'SITE': 'DEFAULT',
            'SPREMISE': '',
            'SSTREET': '',
            'TOTL': 123456,
            'VERS': '1.0.0'}
        actual = result.params
        del(actual['UNIQ'])
        del(actual['SESS'])
        del(actual['ORDR'])
        self.assertEqual(result.params, expected)

class TestRisTestSuite(unittest.TestCase):
    
    #~ private static final Logger logger = Logger.getLogger(TestRisTestSuite.class);
    
    client = Client(url_api, kountAPIkey)
    
    session_id = None
    inq = Inquiry()
    
    def reset_id_and_inquiry(self):
        self.session_id = Utilities.generate_unique_id()
        self.inq = Utilities.default_inquiry(self.session_id)

    def setUp(self):
        self.reset_id_and_inquiry()
        self.server_url = Utilities.RIS_ENDPOINT
        self.session_id = Utilities.generate_unique_id()

    def test_ris_q_1_item_required_field_1_rule_review_1(self):
        #~ logger.debug("running test_ris_q_1_item_required_field_1_rule_review_1");
        
        response = self.client.process(self.inq)
        print(11111, response)
        #~ logger.trace(response.toString());
        
        self.assertEquals("R", response.params["AUTO"]);
        self.assertEquals(0, int(response.params["WARNING_COUNT"]))
        self.assertEquals(1, response.get_rules_triggered())
        self.assertEquals(self.session_id, response.params["SESS"])
        self.assertEquals(self.session_id.substring(0, 10), response.params["ORDR"])
"""
	@Test
	public void testRisQMultiCartItemsTwoOptionalFieldsTwoRulesDecline_2() throws RisException {
		logger.debug("running testRisQMultiCartItemsTwoOptionalFieldsTwoRulesDecline_2");
		
		inq.setUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36");
		inq.setTotal(123456789);
		inq.setCart(Arrays.asList(
				new CartItem("cart item type 0", "cart item 0", "cart item 0 description", 10, 1000),
				new CartItem("cart item type 1", "cart item 1", "cart item 1 description", 11, 1001),
				new CartItem("cart item type 2", "cart item 2", "cart item 2 description", 12, 1002)
			));
		
		Response response = client.process(inq);
		logger.trace(response.toString());
		
		assertEquals("D", response.getAuto());
		assertEquals(0, response.getWarningCount());
		assertEquals(2, response.getRulesTriggered().size());
	}
	
	@Test
	public void testRisQWithUserDefinedFields_3() throws RisException {
		logger.debug("running testRisQWitUserDefinedFields_3");
		
		inq.setParm("UDF[ARBITRARY_ALPHANUM_UDF]", "alphanumeric trigger value");
		inq.setParm("UDF[ARBITRARY_NUMERIC_UDF]", "777");
		
		Response response = client.process(inq);
		logger.trace(response.toString());
		
		boolean alphaNumericTriggered = false;
		boolean numericTriggered = false;
		
		for (int i = 0; i < response.getRulesTriggered().size(); i++) {
			String rdx = response.getParm("RULE_DESCRIPTION_" + i);
			if (rdx.contains("ARBITRARY_ALPHANUM_UDF")) {
				alphaNumericTriggered = true;
				logger.debug("[alpha-numeric rule] triggered");
			} else if (rdx.contains("ARBITRARY_NUMERIC_UDF")) {
				numericTriggered = true;
				logger.debug("[numeric rule] triggered");
			}
		}
		
		assertTrue("One or both rules were not found in the response", (alphaNumericTriggered && numericTriggered));
	}
	
	@Test
	public void testRisQHardErrorExpected_4() throws RisException {
		logger.debug("running testRisQHardErrorExpected_4");
		
		// overwrite the PTOK value to induce an error in the RIS
		inq.setParm("PTOK", "BADPTOK");
		
		Response response = client.process(inq);
		logger.trace(response.toString());
		
		assertEquals("E", response.getMode());
		assertEquals("332", response.getErrorCode());
		assertEquals(1, response.getErrorCount());
		assertEquals("332 BAD_CARD Cause: [PTOK invalid format], Field: [PTOK], Value: [hidden]", response.getErrors().get(0));
	}
	
	@Test
	public void testRisQWarningApproved_5() throws RisException {
		logger.debug("running testRisQWarningApproved_5");
		
		inq.setParm("TOTL", "1000");
		inq.setParm("UDF[UDF_DOESNOTEXIST]", "throw a warning please!");
		
		Response response = client.process(inq);
		logger.trace(response.toString());
		
		assertEquals("A", response.getAuto());
		assertEquals(2, response.getWarningCount());
		
		boolean throwAWarningPlease = false;
		boolean notDefinedForMerchant = false;
		
		for (String warning : response.getWarnings()) {
			if (warning.equals("399 BAD_OPTN Field: [UDF], Value: [UDF_DOESNOTEXIST=>throw a warning please!]")) {
				throwAWarningPlease = true;
				logger.debug("[throw a warning please] found");
			} else if (warning.equals("399 BAD_OPTN Field: [UDF], Value: [The label [UDF_DOESNOTEXIST] is not defined for merchant ID [999666].]")) {
				notDefinedForMerchant = true;
				logger.debug("[not defined for merchant] found");
			}
		}
		
		assertTrue("One or both warnings were not found in response", (throwAWarningPlease && notDefinedForMerchant));
	}
	
	@Test
	public void testRisQHardSoftErrorsExpected_6() throws RisException {
		logger.debug("running testRisQHardSoftErrorsExpected_6");
		
		inq.setParm("PTOK", "BADPTOK");
		inq.setParm("UDF[UDF_DOESNOTEXIST]", "throw a warning please!");
		
		Response response = client.process(inq);
		logger.trace(response.toString());
		
		assertEquals("E", response.getMode());
		assertEquals("332", response.getErrorCode());
		assertEquals(1, response.getErrorCount());
		assertEquals("332 BAD_CARD Cause: [PTOK invalid format], Field: [PTOK], Value: [hidden]", response.getErrors().get(0));
		
		assertEquals(2, response.getWarningCount());
		
		boolean throwAWarningPlease = false;
		boolean notDefinedForMerchant = false;
		
		for (String warning : response.getWarnings()) {
			if (warning.equals("399 BAD_OPTN Field: [UDF], Value: [UDF_DOESNOTEXIST=>throw a warning please!]")) {
				throwAWarningPlease = true;
				logger.debug("[throw a warning please] found");
			} else if (warning.equals("399 BAD_OPTN Field: [UDF], Value: [The label [UDF_DOESNOTEXIST] is not defined for merchant ID [999666].]")) {
				notDefinedForMerchant = true;
				logger.debug("[not defined for merchant] found");
			}
		}
		
		assertTrue("One or both warnings were not found in response", (throwAWarningPlease && notDefinedForMerchant));
	}
	
	@Test
	public void testRisWTwoKCRulesReview_7() throws RisException {
		logger.debug("running testRisWTwoKCRulesReview_7");
		
		inq.setMode(InquiryMode.KC_FULL_INQUIRY_W);
		inq.setTotal(10001);
		inq.setKcCustomerId("KCentralCustomerOne");
		
		Response response = client.process(inq);
		logger.trace(response.toString());
		
		assertEquals("R", response.getKcDecision());
		assertEquals(0, response.getWarningCount());
		assertEquals(0, response.getKcWarningCount());
		assertEquals(2, response.getKcEventCount());
		
		boolean billingToShipping = false;
		boolean orderTotal = false;
		
		for (KcEvent event : response.getKcEvents()) {
			if (event.getCode().equals("billingToShippingAddressReview") && event.getDecision().equals("R")) {
				billingToShipping = true;
				logger.debug("[billing to shipping event] found");
			} else if (event.getCode().equals("orderTotalReview") && event.getDecision().equals("R")) {
				orderTotal = true;
				logger.debug("[order total event] found");
			}
		}
		
		assertTrue("One or both events were not found in the response", (billingToShipping && orderTotal));
	}
	
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
	}
}
"""

if __name__ == "__main__":
    unittest.main(defaultTest = "TestRisTestSuite")
