#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"RIS update"
from request import Request
from util.ris_validation_exception import RisException

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


class UPDATEMODE:
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
        self.params["MODE"] = str(mode)

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
