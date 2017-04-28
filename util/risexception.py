#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"


class RisException(Exception):
    """RIS exeption class:
            message - exception message
            cause - exception cause"""


if __name__ == "__main__":
    c = RisException("REQUIRED", "jjjsssssssj")
    raise c
    raise RisException(message="REQUIRED", cause="jjjj", kwargs={})
