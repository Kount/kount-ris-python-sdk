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
                add1 -- Address 1 (default empty string)
                add2 -- Address 2 (default empty string)
                cty -- City (default empty string)
                st -- State (default empty string)
                pc -- Postal code (default empty string)
                ctry -- Country (default empty string)
                prem -- Premise (default empty string)
                str -- Street (default empty string);
    """

    #~ def __init__(self, add1, add2, cty, st, pc, ctry, **kargs):
    def __init__(self, **kargs):
        """Address constructor.
            _varname - protected variable
            """
        #~ "Address, line 1."
        self._address1 = kargs.get("add1", "")
        #~ "Address, line 2."
        self._address2 = kargs.get("add2", "")
        #~ "City"
        self._city = kargs.get("cty", "")
        #~ "State"
        self._state = kargs.get("st", "")
        #~ "Postal code"
        self._postal_code = kargs.get("pc", "")
        #~ "Country"
        self._country = kargs.get("ctry", "")
        #~ "Premise"
        self._premise = kargs.get("prem", "")
        #~ "Street"
        self._street = kargs.get("str", "")

    def set_address1(self, add1):
        """method Set address 1
            Keyword arguments:
                add1 -- Address 1
            >>> a = Address()
            >>> a.set_address1("address exmpl")
            >>> a.set_address1()
            Traceback (most recent call last):
                ...
            TypeError: set_address1() takes exactly 2 arguments (1 given)
        """
        self._address1 = add1

    def set_address2(self, add2):
        """method Set address 2
            Keyword arguments:
                add2 -- Address 2
            >>> a = Address()
            >>> a.set_address2("address exmpl")
            >>> a.set_address2()
            Traceback (most recent call last):
                ...
            TypeError: set_address2() takes exactly 2 arguments (1 given)

        """
        self._address2 = add2

    def set_city(self, cty):
        """method Set City
            Keyword arguments:
                cty -- City
            >>> a = Address()
            >>> a.set_city("city exmpl")
            >>> a.set_city()
            Traceback (most recent call last):
                ...
            TypeError: set_city() takes exactly 2 arguments (1 given)
        """
        self._city = cty

    def set_state(self, st):
        """method Set State
            Keyword arguments:
                st -- State
            >>> a = Address()
            >>> a.set_state("state exmpl")
            >>> a.set_state()
            Traceback (most recent call last):
                ...
            TypeError: set_state() takes exactly 2 arguments (1 given)

        """
        self._state = st

    def set_country(self, ctry):
        """method Set Country
            Keyword arguments:
                ctry -- Country
            >>> a = Address()
            >>> a.set_country("USA")
            >>> a.set_country()
            Traceback (most recent call last):
                ...
            TypeError: set_country() takes exactly 2 arguments (1 given)
        """
        self._country = ctry

    def set_postal_code(self, pc):
        """method Set Postal code
            Keyword arguments:
                pc -- postal_code
            >>> a = Address()
            >>> a.set_postal_code(1e100)
            >>> a.set_postal_code("42")
            >>> a.set_postal_code(42)
            >>> a.set_postal_code("ala bala")
            >>> a.set_postal_code("<script>alert(42)</script>")
            >>> a.set_postal_code()
            Traceback (most recent call last):
                ...
            TypeError: set_postal_code() takes exactly 2 arguments (1 given)
        """
        self._postal_code = pc

    def set_premise(self, prem):
        """method Set Premise
            Keyword arguments:
                prem -- premise
            >>> a = Address()
            >>> a.set_premise("42")
            >>> a.set_premise()
            Traceback (most recent call last):
                ...
            TypeError: set_premise() takes exactly 2 arguments (1 given)
        """
        self.premise = prem

    def set_street(self, str):
        """method Set Street
            Keyword arguments:
                str -- street
        """
        self._street = str

    def get_address1(self):
        """method get Address1
            return Address 1
        """
        return self._address1

    def get_address2(self):
        """method get Address2
            return Address 2
        """
        return self._address2

    def get_city(self):
        """method get City
            return City
        """
        return self._city

    def get_state(self):
        """method get State
            return State
        """
        return self._state

    def get_postal_code(self):
        """method get Postal code
            return postal code
            >>> a = Address()
            >>> a.get_postal_code()
            ''
            >>> a.get_postal_code(1e100)
            Traceback (most recent call last):
                ...
            TypeError: get_postal_code() takes exactly 1 argument (2 given)
            """
        return self._postal_code

    def get_street(self):
        """method get Street
            return street
        """
        return self._street

    def get_premise(self):
        """method get Premise
            return premise
        """
        return self._premise

    def get_country(self):
        """method get Country
            return Country
        """
        return self._country


if __name__ == "__main__":
    import doctest
    doctest.testmod()
