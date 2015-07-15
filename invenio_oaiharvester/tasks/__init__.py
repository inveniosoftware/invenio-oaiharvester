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

from invenio.celery import celery

from invenio.modules.workflows.api import start

from ..api import get_records, list_records
from ..utils import write_to_dir, print_to_stdout, get_workflow_name, get_identifier_names


@celery.task
def get_specific_records(identifiers, metadata_prefix, url, name, output_dir, workflow):
    """
    Call the module api, in order to harvest specific records from an OAI repo,
    based on their unique identifiers.
    :param metadata_prefix: The prefix for the metadata return (e.g. 'arXiv') (required).
    :param identifiers: A list of unique identifiers for records to be harvested.
    :param url: The The url to be used to create the endpoint.
    :param name: The name of the OaiHARVEST object that we want to use to create the endpoint.
    :param output_dir: The directory where the output should be sent.
    :param workflow: The workflow that should process the output.
    """
    identifiers = get_identifier_names(identifiers)
    schedule_harvest(workflow, output_dir,
                     get_records(identifiers, metadata_prefix, url, name), name)


@celery.task
def list_records_from_dates(metadata_prefix, from_date, until_date, url, name, setSpec, output_dir, workflow):
    """
    Call the module api, in order to harvest records from an OAI repo,
    based on datestamp and/or set parameters.
    :param metadata_prefix: The prefix for the metadata return (e.g. 'arXiv') (required).
    :param from_date: The lower bound date for the harvesting (optional).
    :param until_date: The upper bound date for the harvesting (optional).
    :param url: The The url to be used to create the endpoint.
    :param name: The name of the OaiHARVEST object that we want to use to create the endpoint.
    :param setSpec: The 'set' criteria for the harvesting (optional).
    :param output_dir: The directory where the output should be sent.
    :param workflow: The workflow that should process the output.
    """
    schedule_harvest(workflow, output_dir,
                     list_records(metadata_prefix, from_date, until_date, url, name, setSpec), name)


def schedule_harvest(workflow, output_dir, records, name):
    """
    Selects the output method, depending on the provided parameters. Default is stdout.
    :param workflow: The workflow that should process the output.
    :param output_dir: The directory where the output should be sent.
    :param records: An iterator of harvested records.
    :param name: The name of the OaiHARVEST object.
    """
    if workflow:
        # record_list = []
        # for record in records:
        # record_list.append(record.raw)
        #
        # start(get_workflow_name(workflow, name), record_list)
        pass
    elif output_dir:
        write_to_dir(records, output_dir, max_records=1000)
    else:
        print_to_stdout(records)
