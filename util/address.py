#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


class Address(object):
    """An class representing a street address.
        Keyword arguments:
                address1 -- Address 1 (default empty string)
                address2 -- Address 2 (default empty string)
                city -- City (default empty string)
                state -- State (default empty string)
                postal_code -- Postal code (default empty string)
                country -- Country (default empty string)
                premise -- Premise (default empty string)
                street -- Street (default empty string);
    """

    def __init__(self, address1="", address2="", city="", state="", postal_code="", country="", premise="", street=""):
    #~ def __init__(self, **kargs):
        """Address constructor."""
        #~ "Address, line 1."
        self.address1 = address1
        #~ "Address, line 2."
        self.address2 = address2
        #~ "City"
        self.city = city
        #~ "State"
        self.state = state
        #~ "Postal code"
        self.postal_code = postal_code
        #~ "Country"
        self.country = country
        #~ "Premise"
        self.premise = premise
        #~ "Street"
        self.street = street


if __name__ == "__main__":
    import doctest
    doctest.testmod()
