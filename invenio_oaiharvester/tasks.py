# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Celery tasks used by Invenio-OAIHarvester."""

from __future__ import absolute_import, print_function

from celery import shared_task

from .api import get_records, list_records
from .signals import oaiharvest_finished
from .utils import get_identifier_names


@shared_task
def get_specific_records(identifiers, metadata_prefix=None, url=None,
                         name=None, signals=True, encoding=None,
                         **kwargs):
    """Harvest specific records from an OAI repo via OAI-PMH identifiers.

    :param metadata_prefix: The prefix for the metadata return (e.g. 'oai_dc')
    :param identifiers: list of unique identifiers for records to be harvested.
    :param url: The The url to be used to create the endpoint.
    :param name: The name of the OAIHarvestConfig to use instead of passing
                 specific parameters.
    :param signals: If signals should be emitted about results.
    :param encoding: Override the encoding returned by the server. ISO-8859-1
                     if it is not provided by the server.
    """
    identifiers = get_identifier_names(identifiers)
    request, records = get_records(identifiers, metadata_prefix, url, name,
                                   encoding)
    if signals:
        oaiharvest_finished.send(request, records=records, name=name, **kwargs)


@shared_task
def list_records_from_dates(metadata_prefix=None, from_date=None,
                            until_date=None, url=None,
                            name=None, setspecs=None, signals=True,
                            encoding=None, **kwargs):
    """Harvest multiple records from an OAI repo.

    :param metadata_prefix: The prefix for the metadata return (e.g. 'oai_dc')
    :param from_date: The lower bound date for the harvesting (optional).
    :param until_date: The upper bound date for the harvesting (optional).
    :param url: The The url to be used to create the endpoint.
    :param name: The name of the OAIHarvestConfig to use instead of passing
                 specific parameters.
    :param setspecs: The 'set' criteria for the harvesting (optional).
    :param signals: If signals should be emitted about results.
    :param encoding: Override the encoding returned by the server. ISO-8859-1
                     if it is not provided by the server.
    """
    request, records = list_records(
        metadata_prefix,
        from_date,
        until_date,
        url,
        name,
        setspecs,
        encoding
    )
    if signals:
        oaiharvest_finished.send(request, records=records, name=name, **kwargs)
