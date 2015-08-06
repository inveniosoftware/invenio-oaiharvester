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

from __future__ import absolute_import, print_function, unicode_literals

from invenio.celery import celery

from invenio.modules.workflows.api import start_delayed

from ..api import get_records, list_records
from ..errors import WrongOutputIdentifier
from ..utils import (
    write_to_dir,
    print_to_stdout,
    get_workflow_name,
    get_identifier_names,
    print_total_records,
    print_files_created,
)


@celery.task
def get_specific_records(identifiers, metadata_prefix, url,
                         name, output, workflow, directory):
    """Call the module API, in order to harvest specific records from an OAI repo,
    based on their unique identifiers.

    :param metadata_prefix: The prefix for the metadata return (e.g. 'oai_dc') (required).
    :param identifiers: A list of unique identifiers for records to be harvested.
    :param url: The The url to be used to create the endpoint.
    :param name: The name of the OaiHARVEST object that we want to use to create the endpoint.
    :param output: The type of the output (stdout, workflow, dir/directory).
    :param workflow: The workflow that should process the output.
    :param directory: The directory that we want to send the harvesting results.
    """
    identifiers = get_identifier_names(identifiers)
    schedule_harvest(output, workflow, directory, name,
                     get_records(identifiers, metadata_prefix, url, name))


@celery.task
def list_records_from_dates(metadata_prefix, from_date, until_date, url,
                            name, setSpec, output, workflow, directory):
    """Call the module API, in order to harvest records from an OAI repo,
    based on datestamp and/or set parameters.

    :param metadata_prefix: The prefix for the metadata return (e.g. 'oai_dc') (required).
    :param from_date: The lower bound date for the harvesting (optional).
    :param until_date: The upper bound date for the harvesting (optional).
    :param url: The The url to be used to create the endpoint.
    :param name: The name of the OaiHARVEST object that we want to use to create the endpoint.
    :param setSpec: The 'set' criteria for the harvesting (optional).
    :param output: The type of the output (stdout, workflow, dir/directory).
    :param workflow: The workflow that should process the output.
    :param directory: The directory that we want to send the harvesting results.
    """
    schedule_harvest(
        output, workflow, directory, name,
        list_records(metadata_prefix, from_date, until_date, url, name, setSpec)
    )


def schedule_harvest(output, workflow, directory, name, records):
    """Select the output method, depending on the provided parameters.

    Default is stdout.

    :param output: The type of the output (stdout, workflow, dir/directory).
    :param workflow: The workflow that should process the output.
    :param directory: The directory that we want to send the harvesting results.
    :param name: The name of the OaiHARVEST object.
    :param records: An iterator of harvested records.
    """
    if output == 'stdout':
        total = print_to_stdout(records)
        print_total_records(total)
    elif output == 'dir' or output == 'directory':
        files_created, total = write_to_dir(records, directory)
        print_files_created(files_created)
        print_total_records(total)
    elif output == 'workflow':
        workflow_name = get_workflow_name(workflow, name)
        for record in records:
            start_delayed(workflow_name, [record.raw])
    else:
        raise WrongOutputIdentifier('Output type not recognized.')
