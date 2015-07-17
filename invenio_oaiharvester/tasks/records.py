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

import StringIO


def convert_record_to_json(obj, eng):
    """Convert one record from MARCXML to JSON."""
    from invenio.base.globals import cfg
    source = StringIO.StringIO(obj.data)
    for record in cfg["RECORD_PROCESSORS"]["marcxml"](source):
        # Should only be one.
        obj.data = record
        break
    source.close()


def create_record(obj, eng):
    """Create record with Record API."""
    from invenio_records.api import create_record
    create_record(obj.data)


def check_record(obj, eng):
    """Check if there is a valid record in the data.

    If not, skip this object.
    """
    try:
        assert obj.data
        assert obj.data != '<?xml version="1.0"?>\n<collection/>\n'
    except AssertionError as e:
        obj.log.info("No data found in record. Skipping: {0}".format(str(e)))
        eng.continueNextToken()
