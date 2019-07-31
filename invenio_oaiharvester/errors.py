# -*- coding: utf-8; -*-
#
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""OAI harvester errors."""

from __future__ import absolute_import, print_function


class InvenioOAIHarvesterError(Exception):
    """Base exception for invenio-oaiharvester."""


class InvenioOAIRequestError(InvenioOAIHarvesterError):
    """Error with the OAI-PMH request."""


class NameOrUrlMissing(InvenioOAIHarvesterError):
    """Name or url for harvesting missing."""


class WrongDateCombination(InvenioOAIHarvesterError):
    """'Until' date is larger that 'from' date."""


class IdentifiersOrDates(InvenioOAIHarvesterError):
    """Identifiers cannot be used in combination with dates."""


class InvenioOAIHarvesterConfigNotFound(InvenioOAIHarvesterError):
    """No InvenioOAIHarvesterConfig was found."""
