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
from invenio.testsuite import InvenioTestCase, make_test_suite, run_test_suite
from invenio_oaiharvester.api import get_records
import httpretty


class OaiHarvesterTests(InvenioTestCase):

    def test_get_from_identifiers(self):
        test_record = {
            'license': ['http://arxiv.org/licenses/nonexclusive-distrib/1.0/'],
            'forenames': ['J. E.', 'Rachel Kuzio', 'Sharon X.'],
            'abstract': ['  We introduce the MUSCEL Program (MUltiwavelength observations of the\n'
                         'Structure, Chemistry and Evolution of LSB galaxies), a project aimed at\n'
                         'determining the star-formation histories of low surface brightness galaxies.\n'
                         'MUSCEL utilizes ground-based optical spectra and space-based UV and IR\n'
                         'photometry to fully constrain the star-formation histories of our targets with\n'
                         'the aim of shedding light on the processes that led low surface brightness\n'
                         'galaxies down a different evolutionary path from that followed by high surface\n'
                         'brightness galaxies, such as our Milky Way. Here we present the\n'
                         'spatially-resolved optical spectra of UGC 628, observed with the VIRUS-P IFU at\n'
                         'the 2.7-m Harlen J. Smith Telescope at the McDonald Observatory, and utilize\n'
                         'emission-line diagnostics to determine the rate and distribution of star\n'
                         'formation as well as the gas-phase metallicity and metallicity gradient. We\n'
                         'find highly clustered star formation throughout UGC 628, excluding the core\n'
                         'regions, and a log(O/H) metallicity around -4.2, with more metal rich regions\n'
                         'near the edges of the galactic disk. Based on the emission-line diagnostics\n'
                         'alone, the current mode of star formation, slow and concentrated in the outer\n'
                         'disk, appears to have dominated for quite some time, although there are clear\n'
                         'signs of a much older stellar population formed in a more standard inside-out\n'
                         'fashion.\n'],
            'author': [None, None, None],
            'comments': ['13 pages, 7 figures'],
            'created': ['2015-07-10'],
            'keyname': ['Young', 'de Naray', 'Wang'],
            'authors': [None],
            'title': ['The Distribution of Star Formation and Metals in the Low Surface\n  Brightness Galaxy UGC 628'],
            'id': ['1507.03011'],
            'categories': ['astro-ph.GA']}

        httpretty.enable()
        httpretty.register_uri(httpretty.GET, 'http://export.arxiv.org/oai2', body=test_record)

        records = get_records('oai:arXiv.org:1507.03011', url='http://export.arxiv.org/oai2')

        self.assertEqual(httpretty.last_request().body, test_record)

TEST_SUITE = make_test_suite(OaiHarvesterTests)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE)