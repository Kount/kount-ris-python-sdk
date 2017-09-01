SDK Integration & Unit Tests
=========================================


Integration tests
=================

1. test\_ris\_test\_suite.py
2. test\_basic\_connectivity.py
3. test\_api\_kount.py
4. json\_test.py - Example curl call:

::

   curl -k -H "X-Kount-Api-Key: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5OTk2NjYiLCJhdWQiOiJLb3VudC4xIiwiaWF0IjoxNDk0NTM0Nzk5LCJzY3AiOnsia2EiOm51bGwsImtjIjpudWxsLCJhcGkiOmZhbHNlLCJyaXMiOnRydWV9fQ.eMmumYFpIF-d1up_mfxA5_VXBI41NSrNVe9CyhBUGck" -d "MODE=Q&LAST4=2514&PROD_ITEM[]=SG999999&PROD_DESC[]=3000+CANDLEPOWER+PLASMA+FLASHLIGHT&S2NM=SdkTestShipToFirst+SdkShipToLast&PTOK=0007380568572514&AUTH=A&IPAD=4.127.51.215&B2CI=Albuquerque&S2CC=US&SESS=088E9F4961354D4F90041988B8D5C66B&TOTL=123456&PROD_QUANT[]=2&B2CC=US&S2CI=Gnome&AVST=M&EMAL=curly.riscaller15%40kountqa.com&AVSZ=M&S2PC=99762&S2EM=sdkTestShipTo%40kountsdktestdomain.com&S2ST=AK&FRMT=JSON&VERS=0695&B2PC=87101&ORDR=088E9F496135&PROD_TYPE[]=SPORTING%5FGOODS&B2PN=555+867-5309&S2PN=208+777-1212&NAME=Goofy+Grumpus&MACK=Y&SITE=DEFAULT&PROD_PRICE[]=68990&UAGT=Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10%5F9%5F5%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F37.0.2062.124+Safari%2F537.36&CVVR=M&CASH=4444&B2ST=NM&ANID=&MERC=999666&CURR=USD&S2A1=567+West+S2A1+Court+North&B2A1=1234+North+B2A1+Tree+Lane+South&PTYP=CARD&UNIQ=088E9F4961354D4F9004" https://risk.beta.kount.net

should result in this response:

.. code-block:: none

   {"VERS":"0695","MODE":"Q","TRAN":"PTPN0Z04P8Y6","MERC":"999666","SESS":"088E9F4961354D4F90041988B8D5C66B",
   "ORDR":"088E9F496135","AUTO":"R","SCOR":"29","GEOX":"US","BRND":null,"REGN":null,"NETW":"N","KAPT":"N","CARDS":"1",
   "DEVICES":"1","EMAILS":"1","VELO":"0","VMAX":"0","SITE":"DEFAULT","DEVICE_LAYERS":"....","FINGERPRINT":null,
   "TIMEZONE":null,"LOCALTIME":" ","REGION":null,"COUNTRY":null,"PROXY":null,"JAVASCRIPT":null,"FLASH":null,"COOKIES":null,
   "HTTP_COUNTRY":null,"LANGUAGE":null,"MOBILE_DEVICE":null,"MOBILE_TYPE":null,"MOBILE_FORWARDER":null,
   "VOICE_DEVICE":null,"PC_REMOTE":null,"RULES_TRIGGERED":1,"RULE_ID_0":"1024842","RULE_DESCRIPTION_0":
   "Review if order total > $1000 USD","COUNTERS_TRIGGERED":0,"REASON_CODE":null,"DDFS":null,"DSR":null,"UAS":null,
   "BROWSER":null,"OS":null,"PIP_IPAD":null,"PIP_LAT":null,"PIP_LON":null,"PIP_COUNTRY":null,"PIP_REGION":null,"PIP_CITY":null,
   "PIP_ORG":null,"IP_IPAD":null,"IP_LAT":null,"IP_LON":null,"IP_COUNTRY":null,"IP_REGION":null,"IP_CITY":null,"IP_ORG":null,"WARNING_COUNT":0}

The Kount RIS Python SDK comes with a suite of integration tests,
covering the various request modes and service behavior. Some of the
internal SDK functionality is also covered by those test cases.

Each Kount client, upon negotiating an NDA, is going to receive the
following configuration data: 

* RIS server URL 

* Merchant ID 

* API key 

* configurationKey used in encrypting sensitive data.

Setting configurationKey 
--------------------------------------

In order to run the set of integration tests, it is required to
correctly set the configurationKey in **Khash class**. Feel free to set as a
system variable, put it in local\_settings.pt /Django users/, etc.
Configure it in settings.py

::

    class Khash(object):
        """
        Uninstantiable class constructor.
        Class for creating Kount RIS KHASH encoding payment tokens.
        """
        iv = configurationKey

If the default configurationKey replaced with the correct one, all tests in run
test\_khash.py will be executed. Else the integration tests with configurationKey 
will fail with

::

    ValueError: Configured configurationKey is incorrect.

They easily can be skipped because the \@unittest.skipIf\.

::

    class TestKhash(unittest.TestCase):
        "Khash class test cases"
        def setUp(self):
            self.k = Khash
            self.list_for_hash = ["4111111111111111", '5199185454061655',
                                  4259344583883]
            self.expected = ['WMS5YA6FUZA1KC', '2NOQRXNKTTFL11', 'FEXQI1QS6TH2O5']
            self.merchant_id = '666666'

        @unittest.skipIf("fake configurationKey" in Khash.iv, "Please, configure the configurationKey in kount.settings "
                         "with configurationKey from Kount")
        def test_token_valid(self):
            ...

| Within the test suite `test_basic_connectivity.py <https://github.com/Kount/kount-ris-python-sdk/blob/master/tests/test_basic_connectivity.py>`_, there's
  a test class named `TestBasicConnectivity <https://github.com/Kount/kount-ris-python-sdk/blob/master/tests/test_basic_connectivity.py>`_. Inside, there are two
  test cases, expecting predefined results (check the :ref:`Predictive Response` section). This class can easily be
  edited with your personal merchant data in order to test correct
  connectivity to the RIS server.
| Fields that need to be modified are: 

  * MERCHANT\_ID 
  * URL\_API 
  * TIMEOUT # request timeout in seconds 
  * RAISE\_ERRORS # if True -  raise errors instead of logging with **logger.error**

unit tests:
-------------------

1. test\_address.py
2. test\_payment.py
3. test\_inquiry.py
4. test\_ris\_validation\_exception.py
5. test\_ris\_validator.py
6. test\_validation\_error.py
7. test\_xmlparser.py
8. test\_khash.py

resources:
--------------------------

1. `resources/validate.xml <https://github.com/Kount/kount-ris-python-sdk/tree/master/resources/validate.xml>`_ - Kount xml, used for request's validation
2.  `resources/correct\_key\_cryp.py  <https://github.com/Kount/kount-ris-python-sdk/tree/master/resources/correct\_key\_cryp.py>`_- sha-256 of the correct configurationKey, used for validation
