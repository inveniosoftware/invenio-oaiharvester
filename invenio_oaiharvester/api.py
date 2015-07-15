# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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
from sickle import Sickle
from .errors import NameOrUrlMissing, WrongDateCombination
from .utils import get_oaiharvest_object


def list_records(metadata_prefix='arXiv', from_date=None, until_date=None, url=None, name=None, setSpec=None):
    """
    Harvest records from an OAI repo, based on datestamp and/or set parameters.
    :param metadata_prefix: The prefix for the metadata return (e.g. 'arXiv') (required).
    :param from_date: The lower bound date for the harvesting (optional).
    :param until_date: The upper bound date for the harvesting (optional).
    :param url: The The url to be used to create the endpoint.
    :param name: The name of the OaiHARVEST object that we want to use to create the endpoint.
    :param setSpec: The 'set' criteria for the harvesting (optional).
    :return: An iterator of harvested records.
    """
    if url:
        request = get_from_url(url)
    elif name:
        request, metadata_prefix, lastrun = get_from_oai_name(name)
    else:
        raise NameOrUrlMissing("Name/url missing. Retry using the parameters -n <name> or -u <url>.")

    # By convention, when we have a url we have no lastrun, and when we use
    # the name we can either have from_date (if provided) or lastrun.
    dates = {
        'from': lastrun if from_date is None else from_date,
        'until': until_date
    }

    # Sanity check
    if (dates['until'] is not None) and (dates['from'] > dates['until']):
        raise WrongDateCombination("'Until' date larger than 'from' date.")

    return request.ListRecords(metadataPrefix=metadata_prefix, set=setSpec, **dates)


def get_records(identifiers, metadata_prefix='arXiv', url=None, name=None):
    """
    Harvest specific records from an OAI repo, based on their unique identifiers.
    :param metadata_prefix: The prefix for the metadata return (e.g. 'arXiv') (required).
    :param identifiers: A list of unique identifiers for records to be harvested.
    :param url: The The url to be used to create the endpoint.
    :param name: The name of the OaiHARVEST object that we want to use to create the endpoint.
    :return: An iterator of harvested records.
    """
    if url:
        request = get_from_url(url)
    elif name:
        request, metadata_prefix, _ = get_from_oai_name(name)
    else:
        raise NameOrUrlMissing("Name/url missing. Retry using the parameters -n <name> or -u <url>.")

    for identifier in identifiers:
        arguments = {'identifier': identifier, 'metadataPrefix': metadata_prefix}
        yield request.GetRecord(**arguments)


def get_from_url(url):
    return Sickle(url)


def get_from_oai_name(name):
    obj = get_oaiharvest_object(name)

    req = Sickle(obj.baseurl)
    metadata_prefix = obj.metadataprefix
    lastrun = obj.lastrun
    return req, metadata_prefix, lastrun

