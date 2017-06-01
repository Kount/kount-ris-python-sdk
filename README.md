# Kount Python RIS SDK #

Contains the Kount Python SDK, tests, and build/package routines.

## What is this repository for?

    Contains sources, tests, and resources for the Kount Python SDK
    SDK version: 1.0.0
    Python 2.7.13 and 3.5, 3.6.1 

How do I get set up?  

`pip install kount_ris_sdk`  

or
   1. Clone the repository
   2. Dependencies
        * requests
        * simplejson

How to build the SDK and run integration tests in root directory?


    pytest tests
    python3 -m tests.test_api_kount
    python2 -m tests.test_ris_test_suite
    python -m  tests.test_basic_connectivity


### Setting up IDE projects
* Komodo IDE/Edit, Scite, Visual Studio - have automatic python integration

### Who do I talk to?

    Repo owner or admin
    Other community or team contact

A project that exists as an aid to the `Python Packaging User Guide [pip - link](<https://kount_ris_sdk.python.org>)

