# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module for OAI-PMH metadata harvesting between repositories."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.35',
    'coverage>=4.3.4',
    'isort==4.2.2',
    'mock>=2.0.0',
    'pydocstyle>=1.1.1',
    'pytest-cache>=1.0',
    'pytest-cov>=2.4.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
    'responses>=0.8.0',
    'celery>=3.1.25,<4.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.3,<1.6',
    ],
    'postgresql': [
        'invenio-db[postgresql]>=1.0.0',
    ],
    'mysql': [
        'invenio-db[mysql]>=1.0.0',
    ],
    'sqlite': [
        'invenio-db>=1.0.0',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name in ('mysql', 'postgresql', 'sqlite'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.6.2',
]

install_requires = [
    'Flask>=0.12',
    'flask-celeryext>=0.2.2',
    'blinker>=1.4',
    'sickle>=0.6.1',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_oaiharvester', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-oaiharvester',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio TODO',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-oaiharvester',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_oaiharvester = invenio_oaiharvester:InvenioOAIHarvester',
        ],
        'invenio_celery.tasks': [
            'invenio_oaiharvester = invenio_oaiharvester.tasks',
        ],
        'invenio_db.models': [
            'invenio_oaiharvester = invenio_oaiharvester.models',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
    ],
)
