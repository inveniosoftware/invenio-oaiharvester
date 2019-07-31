# -*- coding: utf-8; -*-
#
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""OAI harvester signals."""

from blinker import Namespace

_signals = Namespace()

oaiharvest_finished = _signals.signal('oaiharvest-finished')
"""
This signal is sent when a harvest has completed.

Example subscriber

.. code-block:: python

    def listener(sender, records, *args, **kwargs):
        for record in records:
            pass
"""
