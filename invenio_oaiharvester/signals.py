# SPDX-FileCopyrightText: 2016 CERN.
# SPDX-License-Identifier: MIT

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
