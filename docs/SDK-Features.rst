SDK Features
===============

The Kount RIS Python SDK provides means for: 

* building and sending requests to the RIS service 

* client-side data verification 

* sensitive information protection.

Building requests
=================

The SDK contains several object model classes representing different
request types as well as many enumeration-like objects which can be used
as request parameter values.

The ``Client`` class accomplishes client-server-client communication,
secured TLS v1.2 for Python 2.7.13 and 3.6.x.

Older Python versions that do not implement TLSv1.2 will be prohibited
from accessing PyPI.

See below for instructions to check your interpreter's TLS version. To
check your Python interpreter's TLS version:

:: 

    python -c "import requests; print(requests.get('https://www.howsmyssl.com/a/check', verify=False).json()['tls_version'])"


If you see **TLS 1.2**, your interpreter's TLS is up to
date. If you see "TLS 1.0" or an error like "tlsv1 alert protocol
version", then you must upgrade. Mac users should pay special attention.
So far, the system Python shipped with MacOS does not yet support
TLSv1.2 in any MacOS version. Fortunately, it's easy to install a modern
Python alongside the MacOS system Python. Either download Python 3.6
from python.org, or for Python 2.7 with the latest TLS, use Homebrew.
Both methods of installing Python will continue working after June 2018.

The reason Python's TLS implementation is falling behind on macOS is
that Python continues to use OpenSSL, which Apple has stopped updating
on macOS. In the coming year, the Python Packaging Authority team will
investigate porting pip to Apple's own "SecureTransport" library as an
alternative to OpenSSL, which would allow old Python interpreters to use
modern TLS with pip only.

Client-side data verification
=============================

The Kount RIS Python SDK provides means for validation of most of the
request parameters, as well as ensuring presence of required parameters
for each request type.

Sensitive information protection
================================

The SDK utilizes specific hashing methods to encrypt and transmit
sensitive client data like credit card and gift card numbers.

