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

"""Tasks used in OAI harvesting for invenio records manipulation."""

from __future__ import absolute_import, print_function, unicode_literals

import StringIO
from functools import wraps

import six
from werkzeug.utils import import_string


def convert_record_to_json(obj, eng):
    """Convert one record from MARCXML to JSON."""
    from invenio.base.globals import cfg
    source = StringIO.StringIO(obj.data)

    processor = cfg["RECORD_PROCESSORS"]["marcxml"]
    if isinstance(processor, six.string_types):
        processor = import_string(processor)

    for record in processor(source):
        # Should only be one.
        obj.data = record
        break
    source.close()


def create_record(obj, eng):
    """Create record with Record API."""
    from invenio_records.api import create_record
    create_record(obj.data)


def quick_match_record(keys_to_check=None, collection=None):
    """Try to quickly match the record with the database.

    You can pass a list of tuples containing the key to retrieve and field.

    E.g. [("control_number",  "control_number"), ..]

    would make a search for record["control_number"] using field
    "control_number".

    :param keys_to_check: list of tuples [(record_key, search_field), ..]
    :param collection: collection to search in. None by default.

    :return: True if matches found, False otherwise
    """
    @wraps(quick_match_record)
    def _quick_match_record(obj, eng):
        keys = keys_to_check  # needed due to outer scope issues
        if not keys:
            # At least try the recid
            keys = [("control_number", "control_number")]

        from invenio_records.api import Record
        from invenio_search.api import Query

        try:
            record = Record(obj.data.dumps())
        except AttributeError:
            record = Record(obj.data)

        for key, field in keys:
            values = record[key] if key in record else None
            if values:
                if not isinstance(values, list):
                    values = [values]
                for val in values:
                    if field:
                        query_string = '{0}:"{1}"'.format(field, val)
                    else:
                        query_string = '"{0}"'.format(val)

                    query = Query(query_string)
                    result = query.search(collection=collection)
                    if len(result) > 0:
                        return True
        return False
    return _quick_match_record
