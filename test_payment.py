import unittest
from util.payment import (BillMeLaterPayment, CardPayment, CheckPayment, GiftCardPayment, GooglePayment,
    GreenDotMoneyPakPayment, NoPayment, Payment, PaypalPayment)


class TestPaymentType(unittest.TestCase):
    def setUp(self):
        self.test = 1234567890*1000000000

    def test_giftcardpayment(self ):
        pt = GiftCardPayment(gift_card_number = self.test)
        self.assertTrue(isinstance(pt, GiftCardPayment))
        self.assertEqual(pt.last4, str(self.test)[-4:])
        self.assertFalse(pt.khashed)
        self.assertEqual(pt.payment_type, "GIFT")
        self.assertEqual(pt.payment_token, str(self.test))

    def test_payments(self):
        t = (Payment, BillMeLaterPayment, CardPayment, CheckPayment, GiftCardPayment, GooglePayment,
        GreenDotMoneyPakPayment, NoPayment, Payment, PaypalPayment)
        payment_dict = {
            "BLML": BillMeLaterPayment(self.test),
            "CARD": CardPayment(self.test),
            "CHEK": CheckPayment(self.test),
            "GIFT": GiftCardPayment(self.test),
            "GOOG": GooglePayment(self.test),
            "GDMP": GreenDotMoneyPakPayment(self.test),
            "NONE": NoPayment(),
            "PYPL": PaypalPayment(self.test),
            }
        pt = []
        for s in payment_dict:
            c = payment_dict[s]
            if isinstance(c, NoPayment):
                self.assertEqual(c.last4, "NONE")
                self.assertIsNone(c.payment_token)
            else:
                self.assertEqual(c.last4, str(self.test)[-4:])
                self.assertEqual(c.payment_token, str(self.test))
            self.assertFalse(c.khashed)
            self.assertEqual(c.payment_type, s)
            pt.append(payment_dict[s])
            self.assertIsInstance(payment_dict[s], t)


if __name__ == "__main__":
    unittest.main()
