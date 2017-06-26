Payment Types
==============================

The Kount RIS Python SDK defines a group of objects representing various
payment types. Using those payment types with the
``Request.set_payment(...)`` method automatically sets the required
``PTYP`` parameter and other parameters corresponding to the selected
payment type.

Supported payment types: 

* ``CardPayment`` 

* ``CheckPayment`` 

* ``GiftCardPayment`` 

* ``GooglePayment`` 

* ``GreenDotMoneyPakPayment``

* ``PaypalPayment``

* ``Apple Pay``

* ``BPAY``

* ``Carte Bleue``

* ``ELV``

* ``GiroPay``

* ``Interac``

* ``Mercado Pago``

* ``Neteller``

* ``POLi``

* ``Single Euro Payments Area``

* ``Skrill/Moneybookers``

* ``Sofort``

* ``Token``

There are also several "system" payment types: 

* ``NoPayment`` 

* ``BillMeLaterPayment``
