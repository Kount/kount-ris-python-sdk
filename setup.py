#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# This file is part of the Kount python sdk project
# https://github.com/Kount/kount-ris-python-sdk/)
# Copyright (C) 2025 Kount an Equifax Company All Rights Reserved.
"""
import os
from codecs import open
from setuptools import setup, find_packages

# GitLab env value will now dynamically set the version (gallilama)
if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

AUTHOR = 'Kount'
EMAIL = 'sdkadmin@kount.com'
PROJECT = 'kount_ris_sdk'
PROJECT_MODULE = 'kount'
VERSION = version
PROJECT_URL = 'https://github.com/Kount/kount-ris-python-sdk'
DESC = 'Kount Python RIS SDK'
LONG_DESC = ''
LICENSE = 'Kount'
KEYWORDS = ('kount', 'sdk', 'ris')

# Version can be set dynamically by GitLab, but other things in the
# SDK appear to be using the value in version.py.
# Developers SHOULD STILL UPDATE the value in version.py for other needs.

this_path = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(this_path, 'README.md'), encoding='utf-8') as f:
    LONG_DESC = f.read()

REQUIRES = (
    'requests>=2.32.3',
)

EXTRAS = {
    'test': (
        'pytest >= 8.3.4',
        'pytest-cov >= 6.0.0',
        'pytest-profiling >= 1.8.1',
        'pytest-html >= 4.1.1',
        'pytest-metadata >= 3.1.1',
    ),
    'dev': (
        'flake8 >= 2.5.0',
        'pytest >= 8.3.4',
        'pytest-cov >= 6.0.0',
        'pytest-profiling >= 1.8.1',
        'pylint >= 3.3.4',
        'pytest-html >= 4.1.1',
        'pytest-metadata >= 3.1.1',
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
]

if __name__ == '__main__':
    setup(
        name=PROJECT,
        version=VERSION,
        description=DESC,
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
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
