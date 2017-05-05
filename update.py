#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

from request import Request
from util.refund_chargeback_status import refund_chargeback_status
from util.update_mode import update_mode
from util.ris_validation_exception import RisException


class Update(Request):
	"""RIS update class.
	 defaults to update_mode WithResponse.
	 """
	def __init__(self):
		super(Update, self).__init__()
		self.set_mode(update_mode("U"))
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

	def refund_chargeback_status(self,rc_status):
		"""Set the Refund/Chargeback status: R = Refund C = Chargeback.
		Arg - rc_status, String Refund or chargeback status
		raise RisException when refund_chargeback_status is None
		"""
		if rc_status is None:
			raise RisException("rc_status can not be None")
		self.params["RFCB"] = rc_status


if __name__ == "__main__":
	r = Update()
	print(Update().params)