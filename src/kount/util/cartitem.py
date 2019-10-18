#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved
"CartItem class"

from __future__ import absolute_import, unicode_literals, division, \
    print_function

from kount.version import VERSION
from kount.config import SDKConfig

__author__ = SDKConfig.SDK_AUTHOR
__version__ = VERSION
__maintainer__ = SDKConfig.SDK_MAINTAINER
__email__ = SDKConfig.MAINTAINER_EMAIL
__status__ = SDKConfig.STATUS


class CartItem(object):
    """A class that represents a shopping cart item.
    kwargs -
        product_type - the product type
        item_name - name of the item
        description - description
        quantity - quantity
        price - the price of the item
    """
    def __init__(self, product_type="", item_name="",
                 description="", quantity="", price=""):
        "Constructor for a cart item."
        self.product_type = product_type
        self.item_name = item_name
        self.description = description
        self.quantity = quantity
        self.price = price

    def __str__(self):
        "String representation of this shopping cart item"
        cart = "Product Type: %s\nItem Name: %s\nDescription:"\
               "%s\nQuantity: %s\nPrice: %s\n" % (
                   self.product_type, self.item_name, self.description,
                   self.quantity, self.price)
        return cart
