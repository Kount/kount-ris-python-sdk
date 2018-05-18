#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.
"""
from __future__ import absolute_import

import os
from codecs import open
from setuptools import setup, find_packages

AUTHOR = 'Kount'
EMAIL = 'sdkadmin@kount.com'
PROJECT = 'kount_ris_sdk'
PROJECT_MODULE = 'kount'
VERSION = '<unknown>'
PROJECT_URL = 'https://github.com/Kount/kount-ris-python-sdk'
DESC = 'Kount Python RIS SDK'
LONG_DESC = ''
LICENSE = 'Kount'
KEYWORDS = ('kount', 'sdk', 'ris')

main_ns = {}
this_path = os.path.abspath(os.path.dirname(__file__))
version_file = os.path.join(this_path, 'src/{0}/version.py'.format(
    PROJECT_MODULE))
with open(version_file) as ver_file:
    exec(ver_file.read(), main_ns)
    VERSION = main_ns['VERSION']

# Get the long description from the README file
with open(os.path.join(this_path, 'README.md'), encoding='utf-8') as f:
    LONG_DESC = f.read()

REQUIRES = (
    'requests>=2.11.1',
    'mom>=0.1.3;python_version<"3.0"'
)

EXTRAS = {
    'test': (
        'pytest >= 2.8.4',
        'pytest-cov >= 2.4.0',
        'pytest-profiling >= 1.1.1',
        'pytest-html >= 1.14.2',
        'pytest-metadata >= 1.5.0',
    ),
    'dev': (
        'flake8 >= 2.5.0',
        'pytest >= 2.8.4',
        'pytest-cov >= 2.4.0',
        'pytest-profiling >= 1.1.1',
        'pylint >= 1.7.2',
        'pytest-html >= 1.14.2',
        'pytest-metadata >= 1.5.0',
    ),
}

# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Python Modules",
    'License :: Other/Proprietary License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]

if __name__ == '__main__':
    setup(
        name=PROJECT,
        version=VERSION,
        description=DESC,
        long_description=LONG_DESC,
        url=PROJECT_URL,
        author=AUTHOR,
        author_email=EMAIL,
        license=LICENSE,
        classifiers=CLASSIFIERS,
        platforms=('any',),
        keywords=KEYWORDS,
        packages=find_packages('src'),
        package_dir={'': 'src'},
        install_requires=REQUIRES,
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        extras_require=EXTRAS,
        package_data={'kount': ['resources/validate.xml']},
        # data_file=['kount/resources/validate.xml']
    )
