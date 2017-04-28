#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

import unittest
from util.ris_validation_exception import RisException
from util.inquiry_mode import InquiryMode


class TestInquiryMode(unittest.TestCase):
    def test_inquiry_mode_valid(self ):
        for self.mode in ["Q", "P", "W", "J", " Q", " P ", "  W ", " j "]:
            im = InquiryMode(self.mode)
            self.is_instance(im)

    def test_inquiry_mode_p(self):
        im = InquiryMode("p")
        self.assertEqual(im.value, "P")
        self.is_instance(im)

    def test_inquiry_mode_empty(self):
        im = InquiryMode("")
        self.assertEqual(im.value, "Q")
        self.is_instance(im)

    def test_inquiry_mode_incorrect(self):
        im = InquiryMode(42)
        self.assertEqual(im.value, "Q")
        self.is_instance(im)

    def test_inquiry_mode_incorrect_string(self):
        for bad_mode in ["42", "<script>alert(42)</script>"]:
            with self.assertRaises(RisException):
                im = InquiryMode(bad_mode)
                self.assertEqual(str(im),
                "Expected mode in ['Q', 'P', 'W', 'J'], received [%s]."%bad_mode)
                self.assertFalse(isinstance(im, InquiryMode))
                self.assertTrue(isinstance(im, RisException))

    def test_inquiry_mode_none(self):
        im = InquiryMode(None)
        self.assertEqual(im.value, "Q")
        self.is_instance(im)


    def is_instance(self, im):
        self.assertTrue(isinstance(im, InquiryMode))

if __name__ == "__main__":
     unittest.main(
        #~ defaultTest="TestInquiryMode.test_inquiry_mode_missing"
     )
