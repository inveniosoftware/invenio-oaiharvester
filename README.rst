..
    This file is part of Invenio.
    Copyright (C) 2015, 2016 CERN.

    Invenio is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, CERN does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.

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
* Documentation: https://invenio-oaiharvester.readthedocs.org.

*This is an experimental development preview release.*

Features
========

This module allows you to easily harvest OAI-PMH repositories, thanks to the `Sickle`_ module, and via signals
you can hook the output into your application, or simply to files.

You keep configurations of your OAI-PMH sources via SQLAlchemy models and run or schedule immediate harvesting jobs
via command-line or regularly via `Celery beat`_.

.. _Celery beat: http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html
.. _Sickle: http://sickle.readthedocs.org/en/latest/

Harvesting is simple
====================

.. code-block:: shell

    inveniomanage oaiharvester get -u http://export.arxiv.org/oai2 -i oai:arXiv.org:1507.07286 > my_record.xml


This will harvest the repository for a specific record and print the records to stdout - which in this case will save it to a file called ``my_record.xml``.

If you want to have your harvested records saved in a directory automatically, its easy:

.. code-block:: shell

    inveniomanage oaiharvester get -u http://export.arxiv.org/oai2 -i oai:arXiv.org:1507.07286 -d /tmp


Note the directory ``-d`` parameter that specifies a directory to save harvested XML files.


Integration with your application
=================================

If you want to integrate ``invenio-oaiharvester`` into your application, you should hook into
the signals sent by the harvester upon completed harvesting.

See ``invenio_oaiharvester.signals:oaiharvest_finished``.

Check also the defined Celery tasks under ``invenio_oaiharvester.tasks``.


Managing OAI-PMH sources
========================

If you want to store configuration for an OAI repository, you can use the
SQLAlchemy model ``invenio_oaiharvester.models:OAIHarvestConfig``.

This is useful if you regularly need to query a server.

Here you can add information about the server URL, metadataPrefix to use etc.
This information is also available when scheduling and running tasks:

.. code-block:: shell

    inveniomanage oaiharvester get -n somerepo -i oai:example.org:1234

Here we are using the `-n, --name` parameter to specify which configured
OAI-PMH source to query, using the ``name`` property.


API
===

If you need to schedule or run harvests via Python, you can use our API:

.. code-block:: python

    from invenio_oaiharvester.api import get_records

    request, records = get_records(identifiers=["oai:arXiv.org:1207.7214"],
                                   url="http://export.arxiv.org/oai2")
    for record in records:
        print rec.raw
