#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


def update_mode(value):
	"""Update mode types.
		value - U - Get no RIS response with the update.
		X - Get a RIS response with the update.
	"""
	update_dict = {
		"U": "NO_RESPONSE",
		"X": "WITH_RESPONSE"
		}
	message = "required - U or X"
	try:
		value = value.upper()
	except AttributeError:
		raise KeyError(message)
	try:
		return update_dict[value]
	except KeyError as e:
		raise KeyError(message)
