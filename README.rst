..
    This file is part of Invenio.
    Copyright (C) 2015-2019 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


======================
 Invenio-OAIHarvester
======================

.. image:: https://img.shields.io/travis/inveniosoftware/invenio-oaiharvester.svg
        :target: https://travis-ci.org/inveniosoftware/invenio-oaiharvester

.. image:: https://img.shields.io/coveralls/inveniosoftware/invenio-oaiharvester.svg
        :target: https://coveralls.io/r/inveniosoftware/invenio-oaiharvester

.. image:: https://img.shields.io/pypi/v/invenio-oaiharvester.svg
        :target: https://pypi.org/pypi/invenio-oaiharvester


Invenio module for OAI-PMH metadata harvesting between repositories.

* Free software: MIT license
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
