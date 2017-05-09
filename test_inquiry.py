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
from request import ASTAT, BCRSTAT, INQUIRYMODE, CURRENCYTYPE, MERCHANTACKNOWLEDGMENT, REFUNDCBSTAT, SHIPPINGTYPESTAT
from inquiry import Inquiry
from pprint import pprint
import uuid
from util.payment import CardPayment
from util.cartitem import CartItem
from util.address import Address


RIS_ENDPOINT = "https://risk.test.kount.net"
MERCHANT_ID = 999666
BILLING_ADDRESS = Address("1234 North B2A1 Tree Lane South", None, "Albuquerque", "NM", "87101", "US")
SHIPPING_ADDRESS = Address("567 West S2A1 Court North", None, "Gnome", "AK", "99762", "US")

class TestInquiry(unittest.TestCase):
    def setUp(self):
        self.params = {}
        
        self.result = Inquiry()
        
        #~ self.inq = Utilities.defaultInquiry(session_id)

    def test_inquiry(self):
        session_id = str(uuid.uuid4())
        result = self.result
        data = self.params
        pprint(session_id )
        self.inquiry_mode = INQUIRYMODE.DEFAULT
        #~ shipping_address = Address("567 West S2A1 Court North", null, "Gnome", "AK", "99762", "US")
        result.shipping_address(SHIPPING_ADDRESS)
        result.shipping_name("SdkShipToFN SdkShipToLN")
        result.billing_address(BILLING_ADDRESS)
        unique_id = session_id[:21]  
        self.currency_type = CURRENCYTYPE.USD
        result.currency_set( CURRENCYTYPE.USD)
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
        result.merchant_set(MERCHANT_ID)
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
        print(111, result)
        self.assertTrue(data)


if __name__ == "__main__":
    unittest.main()


"""
#~ curl -k -H "X-Kount-Api-Key:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5OTk2NjYiLCJhdWQiOiJLb3VudC4xIiwiaWF0IjoxNDg4NTYzMzgzLCJzY3AiOnsia2EiOm51bGwsImtjIjpudWxsLCJhcGkiOmZhbHNlLCJyaXMiOnRydWV9fQ.u8ycf3GuUKKHpNsR8BL40VxLDGFMEpO59k6cYcku9Tc" -d "MODE=Q&S2NM=SdkTestShipToFirst+SdkShipToLast&PTOK=0055071350519059&AUTH=A&IPAD=129.173.116.98&B2CI=Albuquerque&S2CC=US&SESS=F8E874A38B7B4B6DBB71492A584A969D&TOTL=107783&B2CC=US&S2CI=Gnome&AVST=M&AVSZ=M&S2PC=99762&S2EM=sdkTestShipTo%40kountsdktestdomain.com&S2ST=AK&FRMT=JSON&VERS=0630&B2PC=87101&ORDR=F8E874A38B7B&B2PN=555+867-5309&S2PN=208+777-1212&NAME=Goofy+Grumpus&MACK=Y&SITE=DEFAULT&UAGT=Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10%5F9%5F5%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F37.0.2062.124+Safari%2F537.36&CVVR=M&CASH=4444&B2ST=NM&ANID=&MERC=999666&
#~ CURR=USD&S2A1=567+West+S2A1+Court+North&B2A1=1234+North+B2A1+Tree+Lane+South&PTYP=CARD&UNIQ=F8E874A38B7B4B6DBB71&
#~ PROD_ITEM[0]=SG999999&PROD_DESC[0]=3000+CANDLEPOWER+PLASMA+FLASHLIGHT&
#~ PROD_TYPE[0]=SPORTING%5FGOODS&PROD_QUANT[0]=2&PROD_PRICE[0]=68990&PROD_ITEM[1]=TP999999&PROD_DESC[1]=3000+HP+NUCLEAR+TOILET&PROD_TYPE[1]=SPORTING%5FGOODS2&PROD_QUANT[1]=44&PROD_PRICE[1]=1000990" https://risk.test.kount.net
#~ {"MODE":"E","ERRO":221,"ERROR_0":"221 MISSING_EMAL Cause: [Non-empty value was required in this case], Field: [EMAL], Value: []","ERROR_COUNT":1,"WARNING_COUNT":0}
"""