..
    SPDX-FileCopyrightText: 2015, 2016 CERN.
    SPDX-License-Identifier: MIT

======================
 Invenio-OAIHarvester
======================

.. image:: https://img.shields.io/travis/inveniosoftware/invenio-oaiharvester.svg
        :target: https://travis-ci.org/inveniosoftware/invenio-oaiharvester

.. image:: https://img.shields.io/coveralls/inveniosoftware/invenio-oaiharvester.svg
        :target: https://coveralls.io/r/inveniosoftware/invenio-oaiharvester

.. image:: https://img.shields.io/github/tag/inveniosoftware/invenio-oaiharvester.svg
        :target: https://github.com/inveniosoftware/invenio-oaiharvester/releases

.. image:: https://img.shields.io/pypi/dm/invenio-oaiharvester.svg
        :target: https://pypi.python.org/pypi/invenio-oaiharvester

.. image:: https://img.shields.io/github/license/inveniosoftware/invenio-oaiharvester.svg
        :target: https://github.com/inveniosoftware/invenio-oaiharvester/blob/master/LICENSE


Invenio module for OAI-PMH metadata harvesting between repositories.

* Free software: GPLv2 license
* Documentation: https://invenio-oaiharvester.readthedocs.io/

*This is an experimental development preview release.*

About
=====

This module allows you to easily harvest OAI-PMH repositories, thanks to the `Sickle`_ module, and via signals
you can hook the output into your application, or simply to files.

You keep configurations of your OAI-PMH sources via SQLAlchemy models and run or schedule immediate harvesting jobs
via command-line or regularly via `Celery beat`_.

.. _Celery beat: http://celery.readthedocs.io/en/latest/userguide/periodic-tasks.html
.. _Sickle: http://sickle.readthedocs.io/en/latest/
