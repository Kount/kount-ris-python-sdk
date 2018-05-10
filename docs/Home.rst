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

3. How to run integration tests against the installed sdk library.

    First, you need to obtain configuration key from Kount.

    Download the source code from https://github.com/Kount/kount-ris-python-sdk

    Go to the root directory of the project and execute:

::

    pip install .[test]

    pytest tests --conf-key={KEY}
    # or set shell environment
    export CONF_KEY={KEY}
    pytest tests

Running specific test:

::

    pytest tests/test_file.py

For more verbosity and code coverage run the following:
::

        pytest -s -v --cov=kount tests/

4. Setting up IDE projects

  * Komodo IDE/Edit, Scite, Visual Studio - have automatic python integration

5. Who do I talk to?

    #. Repo owner or admin
    
    #. Other community or team contact
