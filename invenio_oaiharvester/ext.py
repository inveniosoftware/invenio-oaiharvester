# SPDX-FileCopyrightText: 2016 CERN.
# SPDX-License-Identifier: MIT

"""Invenio module for OAI-PMH metadata harvesting between repositories."""

from __future__ import absolute_import, print_function

from . import config
from .cli import oaiharvester as oaiharvester_cmd


class InvenioOAIHarvester(object):
    """Invenio-OAIHarvester extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.cli.add_command(oaiharvester_cmd)
        app.extensions['invenio-oaiharvester'] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith('OAIHARVESTER_'):
                app.config.setdefault(k, getattr(config, k))
