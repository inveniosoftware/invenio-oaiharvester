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

"""CLI tool to harvest records from an OAI-PMH repository.

The output can be directed to files in a directory, passed into a "workflow"
or printed to stdout (default).
"""

from __future__ import absolute_import, print_function, unicode_literals

from invenio.ext.script import Manager

from .errors import IdentifiersOrDates
from .tasks import get_specific_records, list_records_from_dates

manager = Manager(description=__doc__)


@manager.option('-m', '--metadataprefix', dest='metadata_prefix', default=None,
                help="The prefix for the metadata return (e.g. 'oai_dc')")
@manager.option('-n', '--name', dest='name', default=None,
                help="The name of the OaiHARVEST object that we want to use to create the endpoint.")
@manager.option('-s', '--setSpec', dest='setSpec', default=None,
                help="The 'set' criteria for the harvesting (optional).")
@manager.option('-i', '--identifiers', dest='identifiers', default=None,
                help="A list of unique identifiers for records to be harvested.")
@manager.option('-f', '--from', dest='from_date', default=None,
                help="The lower bound date for the harvesting (optional).")
@manager.option('-t', '--to', dest='until_date', default=None,
                help="The upper bound date for the harvesting (optional).")
@manager.option('-u', '--url', dest='url', default=None,
                help="The upper bound date for the harvesting (optional).")
@manager.option('-o', '--output', dest='output', default='stdout',
                help="The type of the output (stdout, workflow, dir/directory).")
@manager.option('-w', '--workflow', dest='workflow', default=None,
                help="The workflow that should process the output.")
@manager.option('-d', '--dir', dest='directory', default='records_harvested',
                help="The directory that we want to send the harvesting results.")
def get(metadata_prefix, name, setSpec, identifiers, from_date,
        until_date, url, output, workflow, directory):
    """Harvest records from an OAI repository immediately, without scheduling."""
    begin_harvesting_action(metadata_prefix, name, setSpec, identifiers, from_date,
                            until_date, url, output, workflow, directory, is_queue=False)


@manager.option('-m', '--metadataprefix', dest='metadata_prefix', default=None,
                help="The prefix for the metadata return (e.g. 'oai_dc')")
@manager.option('-n', '--name', dest='name', default=None,
                help="The name of the OaiHARVEST object that we want to use to create the endpoint.")
@manager.option('-s', '--setSpec', dest='setSpec', default=None,
                help="The 'set' criteria for the harvesting (optional).")
@manager.option('-i', '--identifiers', dest='identifiers', default=None,
                help="A list of unique identifiers for records to be harvested.")
@manager.option('-f', '--from', dest='from_date', default=None,
                help="The lower bound date for the harvesting (optional).")
@manager.option('-t', '--to', dest='until_date', default=None,
                help="The upper bound date for the harvesting (optional).")
@manager.option('-u', '--url', dest='url', default=None,
                help="The upper bound date for the harvesting (optional).")
@manager.option('-o', '--output', dest='output', default='stdout',
                help="The type of the output (stdout, workflow, dir/directory).")
@manager.option('-w', '--workflow', dest='workflow', default=None,
                help="The workflow that should process the output.")
@manager.option('-d', '--dir', dest='directory', default='records_harvested',
                help="The directory that we want to send the harvesting results.")
def queue(metadata_prefix, name, setSpec, identifiers, from_date,
          until_date, url, output, workflow, directory):
    """Schedule a run to harvest records from an OAI repository."""
    begin_harvesting_action(metadata_prefix, name, setSpec, identifiers, from_date,
                            until_date, url, output, workflow, directory, is_queue=True)


def begin_harvesting_action(metadata_prefix, name, setSpec, identifiers, from_date,
                            until_date, url, output, workflow, directory, is_queue=False):
    """Select the right method for harvesting according to the parameters.

    Then run it immediately or queue it with Celery.

    :param metadata_prefix: The prefix for the metadata return (e.g. 'oai_dc').
    :param name: The name of the OaiHARVEST object that we want to use to create the endpoint.
    :param setSpec: The 'set' criteria for the harvesting (optional).
    :param identifiers: A list of unique identifiers for records to be harvested.
    :param from_date: The lower bound date for the harvesting (optional).
    :param until_date: The upper bound date for the harvesting (optional).
    :param url: The The url to be used to create the endpoint.
    :param output: The type of the output (stdout, workflow, dir/directory).
    :param workflow: The workflow that should process the output.
    :param directory: The directory that we want to send the harvesting results.
    :param is_queue: Boolean to check whether the harvest should be queued or run immediately.
    """
    if identifiers is None:
        # If no identifiers are provided, a harvest is scheduled:
        # - url / name is used for the endpoint
        # - from_date / lastrun is used for the dates (until_date optionally if from_date is used)
        params = (metadata_prefix, from_date, until_date, url,
                  name, setSpec, output, workflow, directory)
        if is_queue:
            job = list_records_from_dates.delay(*params)
            print("Scheduled job {0}".format(job.id))
        else:
            list_records_from_dates(*params)
    else:
        if (from_date is not None) or (until_date is not None):
            raise IdentifiersOrDates("Identifiers cannot be used in combination with dates.")

        # If identifiers are provided, we schedule an immediate run using them.
        params = (identifiers, metadata_prefix, url,
                  name, output, workflow, directory)
        if is_queue:
            job = get_specific_records.delay(*params)
            print("Scheduled job {0}".format(job.id))
        else:
            get_specific_records(*params)


def main():
    """Run manager."""
    from invenio.base.factory import create_app
    app = create_app()
    manager.app = app
    manager.run()

if __name__ == '__main__':
    main()
