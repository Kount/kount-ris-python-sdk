Integration tests
=================

1. test\_ris\_test\_suite.py
2. test\_basic\_connectivity.py
3. test\_api\_kount.py

The Kount RIS Python SDK comes with a suite of integration tests,
covering the various request modes and service behavior. Some of the
internal SDK functionality is also covered by those test cases.

Each Kount client, upon negotiating an NDA, is going to receive the
following configuration data: 

* RIS server URL 

* Merchant ID 

* API key 

* SALT phrase used in encrypting sensitive data.

Setting SALT phrase
-------------------

In order to run the set of integration tests, it is required to
correctly set the SALT phrase in **Khas class**. Feel free to set as a
system variable, put it in local\_settings.pt /Django users/, etc.
Configure it in settings.py

::

    class Khash(object):
        """
        Uninstantiable class constructor.
        Class for creating Kount RIS KHASH encoding payment tokens.
        """
        iv = SALT

If the default salt replaced with the correct one, all tests in run
test\_khash.py will be executed. Else the integration tests with salt
will fail with

::

    ValueError: Configured SALT phrase is incorrect.

They easily can be skipped because the \_@unittest.skipIf\_.

::

    class TestKhash(unittest.TestCase):
        "Khash class test cases"
        def setUp(self):
            self.k = Khash
            self.list_for_hash = ["4111111111111111", '5199185454061655',
                                  4259344583883]
            self.expected = ['WMS5YA6FUZA1KC', '2NOQRXNKTTFL11', 'FEXQI1QS6TH2O5']
            self.merchant_id = '666666'

        @unittest.skipIf("fake salt" in Khash.salt, "Please, configure the salt in kount.settings "
                         "with salt from Kount")
        def test_token_valid(self):
            ...

| Within the test suite /*tests/test\_basic\_connectivity.py*/, there's
  a test class named ``TestBasicConnectivity``. Inside, there are two
  test cases, expecting predefined results (check the [[Predictive
  Response\|Predictive-Response]] section). This class can easily be
  edited with your personal merchant data in order to test correct
  connectivity to the RIS server.
| Fields that need to be modified are: 

  * MERCHANT\_ID 
  * URL\_API 
  * TIMEOUT # request timeout in seconds 
  * RAISE\_ERRORS # if True -  raise errors instead of logging with **logger.error**

unit tests:
-----------

1. test\_address.py
2. test\_payment.py
3. test\_inquiry.py
4. test\_ris\_validation\_exception.py
5. test\_ris\_validator.py
6. test\_validation\_error.py
7. test\_xmlparser.py
8. test\_khash.py
9. json\_test.py - example data from
   https://kopana.atlassian.net/wiki/display/KS/Testing

resources:
----------

1. resources/validate.xml - Kount xml, used for request's validation
2. resources/correct\_salt\_cryp.py - sha-256 of the correct salt, used
   for validation
