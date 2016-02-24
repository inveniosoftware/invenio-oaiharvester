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

"""CLI tool to harvest records from an OAI-PMH repository."""

from __future__ import absolute_import, print_function, unicode_literals

from invenio_ext.script import Manager

from .errors import IdentifiersOrDates
from .tasks import get_specific_records, list_records_from_dates
from .utils import (
    write_to_dir,
    print_to_stdout,
    print_total_records,
    print_files_created,
)

manager = Manager(description=__doc__)


@manager.option('-m', '--metadataprefix', dest='metadata_prefix', default=None,
                help="The prefix for the metadata return (e.g. 'oai_dc')")
@manager.option('-n', '--name', dest='name', default=None,
                help="The name of the OaiHARVEST object that we want to use to create the endpoint.")
@manager.option('-s', '--setspecs', dest='setspecs', default=None,
                help="The 'set' criteria for the harvesting (optional).")
@manager.option('-i', '--identifiers', dest='identifiers', default=None,
                help="A list of unique identifiers for records to be harvested.")
@manager.option('-f', '--from', dest='from_date', default=None,
                help="The lower bound date for the harvesting (optional).")
@manager.option('-t', '--to', dest='until_date', default=None,
                help="The upper bound date for the harvesting (optional).")
@manager.option('-u', '--url', dest='url', default=None,
                help="The upper bound date for the harvesting (optional).")
@manager.option('-d', '--dir', dest='directory', default=None,
                help="The directory that we want to send the harvesting results.")
@manager.option('-a', '--args', dest='arguments', default=[], action="append",
                help="Arguments to harvesting task, in the form `-a arg1=val1`.")
@manager.option('-q', '--quiet', dest='quiet', action="store_true", default=False,
                help="Surpress output.")
@manager.option('-k', '--enqueue', dest='enqueue', action="store_true", default=False,
                help="Enqueue harvesting and return immediately.")
@manager.option('-p', '--no-signals', dest='signals', action="store_false", default=True,
                help="No signals sent with OAI-PMH harvesting results.")
def harvest(metadata_prefix, name, setspecs, identifiers, from_date,
            until_date, url, directory, arguments, quiet, enqueue, signals):
    """Harvest records from an OAI repository."""
    arguments = dict(x.split('=', 1) for x in arguments)
    if identifiers is None:
        # If no identifiers are provided, a harvest is scheduled:
        # - url / name is used for the endpoint
        # - from_date / lastrun is used for the dates (until_date optionally if from_date is used)
        params = (metadata_prefix, from_date, until_date, url,
                  name, setspecs, signals)
        if enqueue:
            job = list_records_from_dates.delay(*params, **arguments)
            print("Scheduled job {0}".format(job.id))
        else:
            records = list_records_from_dates(*params, **arguments)
    else:
        if (from_date is not None) or (until_date is not None):
            raise IdentifiersOrDates("Identifiers cannot be used in combination with dates.")

        # If identifiers are provided, we schedule an immediate run using them.
        params = (identifiers, metadata_prefix, url,
                  name, signals)
        if enqueue:
            job = get_specific_records.delay(*params, **arguments)
            print("Scheduled job {0}".format(job.id))
        else:
            records = get_specific_records(*params, **arguments)
    if directory:
        files_created, total = write_to_dir(records, directory)
        print_files_created(files_created)
        print_total_records(total)
    elif not quiet:
        total = print_to_stdout(records)
        print_total_records(total)


def main():
    """Run manager."""
    from invenio_base.factory import create_app
    app = create_app()
    manager.app = app
    manager.run()

if __name__ == '__main__':
    main()
