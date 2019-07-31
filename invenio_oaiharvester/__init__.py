# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

r"""Invenio module for OAI-PMH metadata harvesting between repositories.

Harvesting is simple
====================

.. code-block:: shell

    youroverlay oaiharvester harvest -u http://export.arxiv.org/oai2 \
        -i oai:arXiv.org:1507.07286 > my_record.xml


This will harvest the repository for a specific record and print the records to
stdout - which in this case will save it to a file called ``my_record.xml``.

If you want to have your harvested records saved in a directory automatically,
its easy:

.. code-block:: shell

    youroverlay oaiharvester harvest -u http://export.arxiv.org/oai2 \
        -i oai:arXiv.org:1507.07286 -d /tmp


Note the directory ``-d`` parameter that specifies a directory to save
harvested XML files.


Integration with your application
=================================

If you want to integrate ``invenio-oaiharvester`` into your application,
you could hook into the signals sent by the harvester after a completed
harvest.

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

    youroverlay oaiharvester get -n somerepo -i oai:example.org:1234

Here we are using the `-n, --name` parameter to specify which configured
OAI-PMH source to query, using the ``name`` property.
"""

from __future__ import absolute_import, print_function

from .api import get_records, list_records
from .ext import InvenioOAIHarvester
from .version import __version__

__all__ = ('__version__',
           'InvenioOAIHarvester',
           'get_records',
           'list_records')
