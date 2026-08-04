# SPDX-FileCopyrightText: 2014, 2015, 2016 CERN.
# SPDX-License-Identifier: MIT

"""OAI harvest config."""

from __future__ import absolute_import, print_function

OAIHARVESTER_DEFAULT_NAMESPACE_MAP = {
    "OAI-PMH": "http://www.openarchives.org/OAI/2.0/",
}
"""The default namespace used when handling OAI-PMH results."""

OAIHARVESTER_WORKDIR = None
"""Path to directory for oaiharvester related files, default: instance_path."""
