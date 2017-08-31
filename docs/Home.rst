Welcome to the kount-ris-python-sdk!
====================================================================

Kount Python RIS SDK 
----------------------------

Contains the Kount Python SDK, tests, and build/package routines.

1. What is this repository for?

    Contains sources, tests, and resources for the Kount Python SDK
    SDK version: 1.0.0
    Python 2.7.13 and 3.5.3, 3.6.1 

2. How do I get set up?  

::

   pip install kount_ris_sdk

or
   1. Clone the repository

    ::

       python setup.py install

   2. Dependencies
        * requests
        
         only for python 2.7.13, uncomment them in `requirements.txt <https://github.com/Kount/kount-ris-python-sdk/blob/master/requirements.txt>`_
         
        * pathlib


install all dependencies from `requirements.txt <https://github.com/Kount/kount-ris-python-sdk/blob/master/requirements.txt>`_  with

 
    **pip install -r requirements.txt**

3. How to build the SDK and run integration & unit tests in root directory?


:: 

    pytest tests
    python3 -m tests.test_api_kount
    python2 -m tests.test_ris_test_suite
    python -m  tests.test_basic_connectivity


The real configurationKey can be set in **local_settings.py**:

configurationKey = "replace with real configurationKey"

OR is set as *environment variable* **K_KEY** . In this case in *settings.py* uncomment this:


::

   #~ import os
   #~ try:
       #~ configurationKey = os.environ['K_KEY']
   #~ except KeyError:`
       #~ print("The default fake configurationKey set. Required actual one from Kount")


In case of correct configurationKey all tests will be executed:


::

    ~/Kount$ python3 -m pytest tests
    =============== test session starts =============================
    platform linux -- Python 3.6.1, pytest-3.1.0, py-1.4.33, pluggy-0.4.0
    metadata: {'Platform': 'Linux-4.10.0-21-generic-x86_64-with-Ubuntu-17.04-zesty', 'Plugins': {'html': '1.14.2', 'metadata': '1.5.0'}, 'Packages': {'py': '1.4.33', 'pytest': '3.1.0', 'pluggy': '0.4.0'}, 'Python': '3.6.1'}
    rootdir: /home/dani/Kount, inifile:
    plugins: metadata-1.5.0, html-1.14.2
    collected 85 items 
    
    tests/test_address.py ...
    tests/test_api_kount.py .......
    tests/test_basic_connectivity.py ..........
    tests/test_inquiry.py ...
    tests/test_khash.py ...........
    tests/test_payment.py .....
    tests/test_ris_test_suite.py ..........................
    tests/test_ris_validation_exception.py ........
    tests/test_ris_validator.py ...
    tests/test_validation_error.py ........
    tests/test_xmlparser.py .
    
    ===========================================================85 passed in 71.87 seconds ==========
    

with incorrect / missing configurationKey the integration tests will raise a **ValueError: Configured configurationKey is incorrect.**

::

    ~/Kount$ python -m pytest tests
    =========================================================================================== test session starts ============================================================================================
    platform linux2 -- Python 2.7.13, pytest-3.1.1, py-1.4.33, pluggy-0.4.0
    metadata: {'Python': '2.7.13', 'Platform': 'Linux-4.10.0-22-generic-x86_64-with-Ubuntu-17.04-zesty', 'Packages': {'py': '1.4.33', 'pytest': '3.1.1', 'pluggy': '0.4.0'}, 'Plugins': {'html': '1.14.2', 'metadata': '1.5.0'}}
    rootdir: /home/dani/Kount, inifile:
    plugins: metadata-1.5.0, html-1.14.2
    collected 27 items / 4 errors 
    
    ================================================================================================== ERRORS ==================================================================================================
    _________________________________________________________________________________ ERROR collecting tests/test_api_kount.py _________________________________________________________________________________
    tests/test_api_kount.py:14: in <module>
        import inittest
    tests/inittest.py:20: in <module>
        Khash.set_iv(iv)
    kount/util/khash.py:73: in set_iv
        cls.verify()
    kount/util/khash.py:63: in verify
        raise ValueError(mesg)
    E   ValueError: Configured configurationKey is incorrect.
    --------------------------------------------------------------------------------------------- Captured stderr ----------------------------------------------------------------------------------------------
    No handlers could be found for logger "kount.khash"
    ____________________________________________________________________________ ERROR collecting tests/test_basic_connectivity.py _____________________________________________________________________________
    tests/test_basic_connectivity.py:16: in <module>
        import inittest
    tests/inittest.py:20: in <module>
        Khash.set_iv(iv)
    kount/util/khash.py:73: in set_iv
        cls.verify()
    kount/util/khash.py:63: in verify
        raise ValueError(mesg)
    E   ValueError: Configured configurationKey is incorrect.
    ___________________________________________________________________________________ ERROR collecting tests/test_khash.py ___________________________________________________________________________________
    tests/test_khash.py:9: in <module>
        import inittest
    tests/inittest.py:20: in <module>
        Khash.set_iv(iv)
    kount/util/khash.py:73: in set_iv
        cls.verify()
    kount/util/khash.py:63: in verify
        raise ValueError(mesg)
    E   ValueError: Configured configurationKey is incorrect.
    ______________________________________________________________________________ ERROR collecting tests/test_ris_test_suite.py _______________________________________________________________________________
    tests/test_ris_test_suite.py:9: in <module>
        from test_basic_connectivity import generate_unique_id, default_inquiry
    /usr/local/lib/python2.7/dist-packages/_pytest/assertion/rewrite.py:216: in load_module
        py.builtin.exec_(co, mod.__dict__)
    tests/test_basic_connectivity.py:16: in <module>
        import inittest
    tests/inittest.py:20: in <module>
        Khash.set_iv(iv)
    kount/util/khash.py:73: in set_iv
        cls.verify()
    kount/util/khash.py:63: in verify
        raise ValueError(mesg)
    E   ValueError: Configured configurationKey is incorrect.
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    =================================================== 4 error in 0.29 seconds =================================


**Note: run tests with unittest** (displayed info like *logger errors* from raised exceptions in tests):

* with verbosity

::

    ~Kount$ python3 -m unittest discover tests -v
    ...
    test_long request ... validation errors = ['max_length 8991 invalid for S2NM']
    ...

* without verbosity

::

    ~Kount$ python3 -m unittest discover tests
    ...validation errors = ['Regex ^.+@.+\\..+$ invalid for S2EM']
    ....validation errors = ['Regex ^.+@.+\\..+$ invalid for EMAL']
    .validation errors = ['max_length 65 invalid for EMAL']
    .....validation errors = ['Regex ^.+@.+\\..+$ invalid for EMAL']
    .validation errors = ['max_length 8991 invalid for S2NM']
    ValueError - Expecting value: line 1 column 1 (char 0)
    validation errors = ['max_length 56943 invalid for S2NM']
    ValueError - Expecting value: line 1 column 1 (char 0)
    ....validation errors = ['Regex ^.+@.+\\..+$ invalid for EMAL']
    .validation errors = ['max_length 8991 invalid for S2NM']
    ValueError - Expecting value: line 1 column 1 (char 0)
    validation errors = ['max_length 56943 invalid for S2NM']
    ValueError - Expecting value: line 1 column 1 (char 0)
    ...............................validation errors = ['Mode J invalid for MACK', 'Mode J invalid for SESS', 'Mode J invalid for SITE', 'Mode J invalid for PROD_QUANT[0]', 'Mode J invalid for PROD_ITEM[0]', 'Mode J invalid for PROD_PRICE[0]', 'Mode J invalid for PROD_TYPE[0]']
    .............validation errors = ['Mode J invalid for MACK', 'Mode J invalid for SESS', 'Mode J invalid for SITE', 'Mode J invalid for PROD_QUANT[0]', 'Mode J invalid for PROD_ITEM[0]', 'Mode J invalid for PROD_PRICE[0]', 'Mode J invalid for PROD_TYPE[0]']
    ......................
    ----------------------------------------------------------------------
    Ran 85 tests in 71.508s
    OK



**The coverage can be measured with**


::

    ~/Kount$ coverage run -m unittest discover tests
    .....................................................................................
    ----------------------------------------------------------------------
    Ran 85 tests in 67.346s
    ~/Kount$ coverage report --omit=*/local/*,*/.local/*


**TOTAL**  -  **91%**  

or generate **detailed html coverage** in folder ~htmlcov with:

::

    ~/Kount$ coverage  html --omit=*/local/*,*/.local/*


4. Setting up IDE projects

  * Komodo IDE/Edit, Scite, Visual Studio - have automatic python integration

5. Who do I talk to?

    #. Repo owner or admin
    
    #. Other community or team contact
