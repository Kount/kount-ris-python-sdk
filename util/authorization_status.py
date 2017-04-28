#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


authorization_status_dict = {"A": "Approve", "D": "Decline", "R": "Review", "E": "Escalate", "C": "Elevated",
                                              "X": "Review_Timeout", "Y": "Approved_Declined_Timeout"}

def authorization_status(auth):
    """A - Approve
        D - Decline
        R - Review
        E - Escalate
        Additional status codes displayed in the AWC.
        C - Original transaction was approved but due to dynamic scoring the transaction now has an elevated score and may require reevaluation.
        X - Transaction was flagged for review but never acted upon and has timed out.
        Y - Original transaction was approved but updated with AUTH=D and then timed out.
        >>> a = authorization_status({})
        Traceback (most recent call last):
            ...
        KeyError
        >>> a = authorization_status()
        Traceback (most recent call last):
            ...
        TypeError: authorization_status() takes exactly 1 argument (0 given)
        >>> a = authorization_status("a ")
        >>> a = authorization_status("A ")
        >>> a = authorization_status("A")
        >>> a = authorization_status("aA")
        Traceback (most recent call last):
            ...
        KeyError
        >>> a = authorization_status(42)
        Traceback (most recent call last):
            ...
        KeyError
    """
    auth = str(auth).strip().upper()
    return authorization_status_dict[auth]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
