# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""OAI harvest config."""

from __future__ import absolute_import, print_function

OAIHARVESTER_DEFAULT_NAMESPACE_MAP = {
    "OAI-PMH": "http://www.openarchives.org/OAI/2.0/",
}
"""The default namespace used when handling OAI-PMH results."""

OAIHARVESTER_WORKDIR = None
"""Path to directory for oaiharvester related files, default: instance_path."""
