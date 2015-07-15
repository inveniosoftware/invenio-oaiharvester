# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2011, 2012, 2013, 2014, 2015 CERN.
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

"""OAI harvest database models."""

from invenio.ext.sqlalchemy import db
from invenio.ext.sqlalchemy.utils import session_manager

def get_default_arguments():
    """Return default values for arguments."""
    arguments_default = {'c_stylesheet': '',
                         'r_kb-rep-no-file': '',
                         'r_format': '',
                         'u_name': '',
                         'a_rt-queue': '',
                         'r_kb-journal-file': '',
                         'u_priority': '',
                         'a_stylesheet': '',
                         't_doctype': '',
                         'f_filter-file': '',
                         'p_extraction-source': []}
    return arguments_default


class OaiHARVEST(db.Model):

    """Represents a OaiHARVEST record."""

    __tablename__ = 'oaiHARVEST'

    id = db.Column(db.MediumInteger(9, unsigned=True), nullable=False,
                   primary_key=True, autoincrement=True)
    baseurl = db.Column(db.String(255), nullable=False, server_default='')
    metadataprefix = db.Column(db.String(255), nullable=False,
                               server_default='oai_dc')
    arguments = db.Column(db.MarshalBinary(default_value=get_default_arguments(),
                                           force_type=dict), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(255), nullable=False)
    lastrun = db.Column(db.DateTime, nullable=True)
    postprocess = db.Column(db.String(20), nullable=False,
                            server_default='h')
    workflows = db.Column(db.String(255),
                          nullable=False,
                          server_default='')
    setspecs = db.Column(db.Text, nullable=False)

    def to_dict(self):
        """Get model as dict."""
        dict_representation = self.__dict__
        del dict_representation["_sa_instance_state"]
        return dict_representation

    @classmethod
    def get(cls, *criteria, **filters):
        """Wrapper for filter and filter_by functions of SQLAlchemy.

        .. code-block:: python

            OaiHARVEST.get(OaiHARVEST.id == 1)
            OaiHARVEST.get(id=1)
        """
        return cls.query.filter(*criteria).filter_by(**filters)

    @session_manager
    def save(self):
        """Save object to persistent storage."""
        db.session.add(self)


__all__ = ('OaiHARVEST',)
