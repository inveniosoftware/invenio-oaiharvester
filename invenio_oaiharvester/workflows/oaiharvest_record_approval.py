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

"""Generic record processing with approval step before inserting."""

from __future__ import absolute_import, print_function, unicode_literals

from flask import render_template

from invenio.modules.workflows.tasks.logic_tasks import (
    workflow_else,
    workflow_if,
)
from invenio.modules.workflows.tasks.marcxml_tasks import (
    approve_record,
    convert_record,
    was_approved
)
from invenio.modules.workflows.tasks.workflows_tasks import log_info

from invenio_records.api import Record

import six

from ..tasks.records import (
    convert_record_to_json,
    create_record,
    quick_match_record
)


class oaiharvest_record_approval(object):

    """Sample workflow for OAI harvesting with oai_dc metadataprefix.

    This workflow assumes the incoming data to be a string representation of
    OAI_DC XML.

    NOTE: This workflow makes use of Holding Pen for record approval.
    """

    object_type = "OAI harvest"
    mapping = {
        "title": "title_statement.title",
        "subject": "subject_added_entry_topical_term.topical_term_or_geographic_name_entry_element",
        "abstract": "summary.summary",
        "ids": "system_control_number.system_control_number"
    }

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
            # Halt this record to be approved in the Holding Pen
            approve_record,
            # Check user action taken
            workflow_if(was_approved),
            [
                # Create record in the database using invenio_records
                create_record,
            ],
            workflow_else,
            [
                log_info("Record has been rejected")
            ]
        ],
        workflow_else,
        [
            log_info("Record is already in the database"),
        ],
    ]

    @staticmethod
    def get_title(bwo, **kwargs):
        """Return the value to put in the title column of HoldingPen."""
        if isinstance(bwo.data, six.string_types):
            # Probably XML, nothing to do here
            return "No title extracted"
        record = Record(bwo.data)
        return record[oaiharvest_record_approval.mapping["title"]][0]

    @staticmethod
    def get_description(bwo, **kwargs):
        """Return the value to put in the description column of HoldingPen."""
        if isinstance(bwo.data, six.string_types):
            # Probably XML, nothing to do here
            return "Unformatted: <pre>{0}</pre>".format(bwo.data[:100])
        record = Record(bwo.data)

        abstract = record[oaiharvest_record_approval.mapping["abstract"]][0][0]
        categories = record[oaiharvest_record_approval.mapping["subject"]][0]
        identifiers = record[oaiharvest_record_approval.mapping["ids"]][0]

        return render_template(
            'oaiharvester/holdingpen/oai_record.html',
            object=bwo,
            categories=categories,
            abstract=abstract,
            identifiers=identifiers
        )

    @staticmethod
    def get_additional(bwo, **kwargs):
        """Return the value to put in the additional column of HoldingPen."""
        return ""

    @staticmethod
    def formatter(obj, **kwargs):
        """Format the object."""
        return "<pre>{0}</pre>".format(obj.data)

    @staticmethod
    def get_sort_data(obj, **kwargs):
        """Return a dictionary of key values useful for sorting in Holding Pen."""
        return {}
