..
    This file is part of Invenio.
    Copyright (C) 2015 CERN.

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

This module allows you to easily harvest OAI-PMH repositories, thanks to the `Sickle`_ module, and feed the
output into your ingestion workflows, or simply to files. You can configure
your OAI-PMH sources via a web-interface and run or schedule immediate harvesting jobs
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

    inveniomanage oaiharvester get -u http://export.arxiv.org/oai2 -i oai:arXiv.org:1507.07286 -o dir


Note the  output ``-o`` parameter that specifies how to output the harvested records. The three options are:

   * Sent to a workflow (E.g. `-o workflow`)
   * Saved files in a folder (E.g. `-o dir`)
   * Printed to stdout (default)


Harvesting with workflows
=========================

.. code-block:: shell

    inveniomanage oaiharvester get -u http://export.arxiv.org/oai2 -i oai:arXiv.org:1507.07286 -o workflow

When you send an harvested record to a workflow you can process the harvested
files however you'd like and then even upload it automatically into your own repository.

This module already provides some


Managing OAI-PMH sources
========================

If you want to store configuration for an OAI repository, you can use the
administration interface available via the admin panel. This is useful if you regularly need to query a server.

Here you can add information about the server URL, metadataPrefix to use etc. This information is also available when scheduling and running tasks:


.. code-block:: shell

    inveniomanage oaiharvester get -n somerepo -i oai:example.org:1234

Here we are using the `-n, --name` parameter to specify which stored OAI-PMH source to query, by name.


API
===

If you need to schedule or run harvests via Python, you can use our API:

.. code-block:: python

    from invenio_oaiharvester.api import get_records
    for rec in get_records(identifiers=["oai:arXiv.org:1207.7214"],
                           url="http://export.arxiv.org/oai2"):
        print rec.raw
