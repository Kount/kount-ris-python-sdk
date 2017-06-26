README Kount Python RIS SDK 
==================================

Contains the Kount Python SDK, tests, and build/package routines.

1.  What is this repository for?

    Contains sources, tests, and resources for the Kount Python SDK
    SDK version: 1.0.0
    Python 2.7.13 and 3.5, 3.6.1 

2. How do I get set up?  

    .. code-block:: python

       pip install kount_ris_sdk

    or
       1. Clone the repository
       2. Dependencies
       
            * requests
        
            # only for python 2.7.13, uncomment them in requirements.txt:
            
            * pathlib
      

      install all dependencies from `requirements.txt <https://github.com/Kount/kount-ris-python-sdk/blob/master/kount/requirements.py>`
      with
    
      .. code-block:: python
    
          pip install -r requirements.txt

3. How to run integration tests in root directory?


    .. code-block:: python

        python3 -m tests.test_api_kount
        python2 -m tests.test_ris_test_suite
        python -m  tests.test_basic_connectivity
    


4. Setting up IDE projects

    Komodo IDE/Edit, Scite, Visual Studio - have automatic python integration

5. Who do I talk to?

    Repo owner or admin
    Other community or team contact

----

This is the README file for the project.

The file should use UTF-8 encoding and be written using `reStructuredText
<http://docutils.sourceforge.net/rst.html>`_. It
will be used to generate the project webpage on PyPI and will be displayed as
the project homepage on common code-hosting services, and should be written for
that purpose.

