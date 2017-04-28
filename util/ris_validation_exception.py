#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

from settings import error_messages

class RisException(Exception):
    """RIS exeption class:
            message - exception message
            cause - exception cause"""


class RisValidationException(RisException):
    """Ris validation exception class.
        kwargs -
            message - exception message
            cause - cause
            errors - list of errors encountered.
            """
    def __init__(self, message="", errors=[], cause=""):
        # Call the base class constructor with the parameters it needs
        self.message = message
        self.errors = errors
        self.cause = cause
        super(RisValidationException, self).__init__(self.message, self.cause, self.errors)


class RisResponseException(RisException):
    """Response exception
        kwargs -
            exception_code - Ris exception code
            """
    def __init__(self, exception_code):
        self.exception_code = error_messages[exception_code]
        super(RisResponseException, self).__init__(self.exception_code)


if __name__ == "__main__":
    c = RisException("REQUIRED", "42")
    #~ raise c
    #~ raise RisException("REQUIRED", "42")
    #~ c = RisValidationException("REQUIRED", "42")
    #~ raise c
    #~ raise RisValidationException(message="REQUIRED", cause="42", errors=[1, 2, 3])
    c = RisResponseException(301)
    raise c
    raise RisValidationException(message="REQUIRED", cause="42", errors=[1, 2, 3])
