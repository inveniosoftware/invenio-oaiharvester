# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""OAI harvest database models."""

from __future__ import absolute_import, print_function

import datetime

from invenio_db import db


class OAIHarvestConfig(db.Model):
    """Represents a OAIHarvestConfig record."""

    __tablename__ = 'oaiharvester_configs'

    id = db.Column(db.Integer, primary_key=True)
    baseurl = db.Column(db.String(255), nullable=False, server_default='')
    metadataprefix = db.Column(db.String(255), nullable=False,
                               server_default='oai_dc')
    comment = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(255), nullable=False)
    lastrun = db.Column(db.DateTime, default=datetime.datetime(
        year=1900, month=1, day=1
    ), nullable=True)
    setspecs = db.Column(db.Text, nullable=False)

    def save(self):
        """Save object to persistent storage."""
        with db.session.begin_nested():
            db.session.merge(self)

    def update_lastrun(self, new_date=None):
        """Update the 'lastrun' attribute of object to now."""
        self.lastrun = new_date or datetime.datetime.now()


__all__ = ('OAIHarvestConfig',)
