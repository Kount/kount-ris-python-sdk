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
secured TLS v1.3

See below for instructions to check your interpreter's TLS version. To
check your Python interpreter's TLS version:

:: 

    python -c "import requests; print(requests.get('https://www.howsmyssl.com/a/check', verify=False).json()['tls_version'])"

Client-side data verification
=============================

The Kount RIS Python SDK provides means for validation of most of the
request parameters, as well as ensuring presence of required parameters
for each request type.

Sensitive information protection
================================

The SDK utilizes specific hashing methods to encrypt and transmit
sensitive client data like credit card and gift card numbers.

