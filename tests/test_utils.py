# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015, 2016 CERN.
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

"""Test for utilities used by OAI harvester."""

import os


def test_identifier_extraction(app):
    """Test extracting identifier from OAI XML."""
    from invenio_oaiharvester.utils import (
        identifier_extraction_from_string,
    )
    with app.app_context():
        xml_sample = ("<record><test></test>"
                      "<identifier>identifier1</identifier></record>")
        result = identifier_extraction_from_string(
            xml_sample, oai_namespace=""
        )

        assert result == "identifier1"


def test_identifier_extraction_with_namespace(app):
    """Test extracting identifier from OAI XML."""
    from invenio_oaiharvester.utils import (
        identifier_extraction_from_string,
    )
    with app.app_context():
        xml_sample = ("<OAI-PMH xmlns='http://www.openarchives.org/OAI/2.0/'>"
                      "<record><test></test>"
                      "<identifier>identifier1</identifier></record>"
                      "</OAI-PMH>")
        result = identifier_extraction_from_string(xml_sample)

        assert result == "identifier1"


def test_records_extraction_without_namespace(app):
    """Test extracting records from OAI XML without a namespace."""
    from invenio_oaiharvester.utils import record_extraction_from_string
    with app.app_context():
        raw_xml = open(os.path.join(
            os.path.dirname(__file__),
            "data/sample_arxiv_response_no_namespace.xml"
        )).read()
        result = len(record_extraction_from_string(raw_xml, oai_namespace=""))
        assert result == 1


def test_records_extraction_with_namespace_getrecord(app):
    """Test extracting records from OAI XML with GetRecord."""
    from invenio_oaiharvester.utils import record_extraction_from_string
    with app.app_context():
        raw_xml = open(os.path.join(
            os.path.dirname(__file__),
            "data/sample_arxiv_response_with_namespace.xml"
        )).read()
        assert len(record_extraction_from_string(raw_xml)) == 1


def test_records_extraction_with_namespace_listrecords(app):
    """Test extracting records from OAI XML with ListRecords."""
    from invenio_oaiharvester.utils import record_extraction_from_string
    with app.app_context():
        raw_xml = open(os.path.join(
            os.path.dirname(__file__),
            "data/sample_inspire_response_listrecords.xml"
        )).read()
        assert len(record_extraction_from_string(raw_xml)) == 2


def test_records_extraction_from_file(app):
    """Test extracting records from OAI XML."""
    from invenio_oaiharvester.utils import record_extraction_from_file
    with app.app_context():
        path_tmp = os.path.join(
            os.path.dirname(__file__),
            "data/sample_arxiv_response_with_namespace.xml"
        )
        assert len(record_extraction_from_file(path_tmp)) == 1


def test_identifier_filter():
    """oaiharvest - testing identifier filter."""
    from invenio_oaiharvester.utils import get_identifier_names
    sample = "oai:mysite.com:1234"
    assert get_identifier_names(sample) == ["oai:mysite.com:1234"]

    sample = "oai:mysite.com:1234, oai:example.com:2134"
    expected = ["oai:mysite.com:1234", "oai:example.com:2134"]
    assert get_identifier_names(sample) == expected

    sample = "oai:mysite.com:1234/testing, oai:example.com:record/1234"
    expected = ["oai:mysite.com:1234/testing", "oai:example.com:record/1234"]
    assert get_identifier_names(sample) == expected
