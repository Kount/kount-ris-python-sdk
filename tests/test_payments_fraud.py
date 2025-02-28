#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk
# Copyright (C) 2025 Kount an Equifax Company All Rights Reserved.
"Test Payments Fraud Integration"

import pytest
import unittest

from .test_inquiry import generate_unique_id, PTOK

from kount.util.cartitem import CartItem
from kount.client import Client
from kount.request import InquiryMode
from kount.inquiry import Inquiry
from kount.util.payment import CardPayment
from kount.config import SDKConfig
from kount.version import VERSION

__author__ = SDKConfig.SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDKConfig.SDK_MAINTAINER
__email__ = SDKConfig.MAINTAINER_EMAIL
__status__ = SDKConfig.STATUS


@pytest.mark.usefixtures("migration_mode_enabled", "pf_client_id", "pf_auth_endpoint", "pf_api_endpoint", "pf_api_key")
class TestPaymentsFraud(unittest.TestCase):
    """Test Payments Fraud"""
    def setUp(self):
        self.session_id = str(generate_unique_id())
        self.client = Client(
            api_url='',
            api_key='',
            raise_errors=True,
            migration_mode_enabled=self.migration_mode_enabled,
            pf_client_id=self.pf_client_id,
            pf_auth_endpoint=self.pf_auth_endpoint,
            pf_api_endpoint=self.pf_api_endpoint,
            pf_api_key=self.pf_api_key,
        )

    def test_happy_path(self):
        if not self.migration_mode_enabled:
            self.skipTest("Migration mode not enabled")

        """test_happy_path"""
        inq = Inquiry()
        inq.set_request_mode(InquiryMode.DEFAULT)
        payment = CardPayment(PTOK, khashed=False)
        inq.set_masked_payment(payment)
        cart_items = list()
        cart_items.append(CartItem("SPORTING_GOODS", "SG999999",
                                   "3000 CANDLEPOWER PLASMA FLASHLIGHT",
                                   '2', '68990'))
        inq.set_shopping_cart(cart_items)


        response = self.client.process(inq)

        self.assertTrue(response.get_auto() != 'E')


if __name__ == '__main__':
    unittest.main(
        #~ defaultTest="TestPaymentType.test_payments_fraud"
        )
