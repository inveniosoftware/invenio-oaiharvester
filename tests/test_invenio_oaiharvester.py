# SPDX-FileCopyrightText: 2016 CERN.
# SPDX-License-Identifier: MIT

"""Module tests."""

from __future__ import absolute_import, print_function

from flask import Flask

from invenio_oaiharvester import InvenioOAIHarvester


def test_version():
    """Test version import."""
    from invenio_oaiharvester import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = InvenioOAIHarvester(app)
    assert 'invenio-oaiharvester' in app.extensions

    app = Flask('testapp')
    ext = InvenioOAIHarvester()
    assert 'invenio-oaiharvester' not in app.extensions
    ext.init_app(app)
    assert 'invenio-oaiharvester' in app.extensions
