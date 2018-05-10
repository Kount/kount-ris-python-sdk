README Kount Python RIS SDK 
==================================

Contains the Kount Python SDK, tests, and build/package routines.

1.  What is this repository for?

    Contains sources, tests, and resources for the Kount Python SDK
    SDK version: 3.0
    Python 2.7.13 and 3.5, 3.6.1 

2. How do I get set up?  

    .. code-block:: python

       pip install kount_ris_sdk

3. How to run integration tests against the installed sdk library.

    First, you need to obtain configuration key from Kount.

    Download the source code from https://github.com/Kount/kount-ris-python-sdk

    Go to the root directory of the project and execute:
    .. code-block:: python

        pip install .[test]

        pytest tests --conf-key={KEY}

        or

        export CONF_KEY={KEY}
        pytest tests

    Running specific test:

    .. code-block:: python
        pytest tests/test_file.py


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

