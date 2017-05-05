#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


def refund_chargeback_status(value):
	"""refund charge back status.
		value - R - The transaction was a refund.",
		"C" - The transaction was a chargeback.
	"""
	rcs_dict = {
		"R": "REFUND",
		"C": "CHARGEBACK"
		}
	message = "required - R or C"
	try:
		value = value.upper()
	except AttributeError:
		raise KeyError(message)
	try:
		return rcs_dict[value]
	except KeyError as e:
		raise KeyError(message)
