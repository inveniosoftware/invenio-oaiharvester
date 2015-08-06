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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Test for workflow tasks used by OAI harvester."""

from invenio.modules.workflows.testsuite.test_workflows import \
    WorkflowTasksTestCase
from invenio.testsuite import make_test_suite, run_test_suite


class OAIHarvesterTasks(WorkflowTasksTestCase):

    """Class to test the harvesting related workflow tasks."""

    def setUp(self):
        """Setup tests."""
        self.create_registries()

    def tearDown(self):
        """Clean up created objects."""
        from invenio.modules.workflows.models import Workflow
        Workflow.get(Workflow.module_name == "unit_tests").first().delete()
        self.cleanup_registries()


TEST_SUITE = make_test_suite(OAIHarvesterTasks)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE)
