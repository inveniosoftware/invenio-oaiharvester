# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111 1307, USA.

"""Generic record processing before inserting into database."""


from invenio.modules.workflows.tasks.logic_tasks import (
    workflow_else,
    workflow_if,
)
from invenio.modules.workflows.tasks.marcxml_tasks import convert_record
from invenio.modules.workflows.tasks.workflows_tasks import log_info

from ..tasks.records import (
    convert_record_to_json,
    create_record,
    quick_match_record
)


class oaiharvest_record(object):

    """Sample workflow for OAI harvesting with oai_dc metadataprefix.

    This workflow assumes the incoming data to be a string representation of
    OAI_DC XML.

    NOTE: This workflow blindly inserts records into the database.
    """

    object_type = "OAI harvest"

    workflow = [
        # Convert OAI_DC XML -> MARCXML
        # FIXME Remove this step when we have one-step OAI_DC -> JSON
        convert_record("oaidc2marcxml.xsl"),
        # Convert MARCXML -> JSON
        convert_record_to_json,
        # Try to match the record with the database
        # FIXME Add more identifiers to match. By default only control_number.
        workflow_if(quick_match_record(), True),
        [
            # Create record in the database using invenio_records
            create_record,
        ],
        workflow_else,
        [
            log_info("Record is already in the database"),
        ],
    ]
