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

"""OAI harvest utils."""

from __future__ import absolute_import, print_function, unicode_literals

import os
import re
import sys
from datetime import datetime

from lxml import etree

from invenio_base.globals import cfg
from invenio_utils.shell import run_shell_command

REGEXP_OAI_ID = re.compile("<identifier.*?>(.*?)<\/identifier>", re.DOTALL)


def record_extraction_from_file(path, oai_namespace="http://www.openarchives.org/OAI/2.0/"):
    """Given a harvested file return a list of every record incl. headers.

    :param path: is the path of the file harvested
    :type path: str

    :param oai_namespace: optionally provide the OAI-PMH namespace
    :type oai_namespace: str

    :return: return a list of XML records as string
    :rtype: str
    """
    list_of_records = []
    with open(path) as xml_file:
        list_of_records = record_extraction_from_string(xml_file.read(), oai_namespace)
    return list_of_records


def record_extraction_from_string(xml_string, oai_namespace="http://www.openarchives.org/OAI/2.0/"):
    """Given a OAI-PMH XML return a list of every record incl. headers.

    :param xml_string: OAI-PMH XML
    :type xml_string: str

    :param oai_namespace: optionally provide the OAI-PMH namespace
    :type oai_namespace: str

    :return: return a list of XML records as string
    :rtype: str
    """
    if oai_namespace:
        nsmap = {
            None: oai_namespace
        }
    else:
        nsmap = cfg.get("OAIHARVESTER_DEFAULT_NAMESPACE_MAP")
    namespace_prefix = "{{{0}}}".format(oai_namespace)
    root = etree.fromstring(xml_string)
    headers = []
    headers.extend(root.findall(".//{0}responseDate".format(namespace_prefix), nsmap))
    headers.extend(root.findall(".//{0}request".format(namespace_prefix), nsmap))

    records = root.findall(".//{0}record".format(namespace_prefix), nsmap)

    list_of_records = []
    for record in records:
        wrapper = etree.Element("OAI-PMH", nsmap=nsmap)
        for header in headers:
            wrapper.append(header)
        wrapper.append(record)
        list_of_records.append(etree.tostring(wrapper))
    return list_of_records


def identifier_extraction_from_string(xml_string, oai_namespace="http://www.openarchives.org/OAI/2.0/"):
    """Given a OAI-PMH XML string return the OAI identifier.

    :param xml_string: OAI-PMH XML
    :type xml_string: str

    :param oai_namespace: optionally provide the OAI-PMH namespace
    :type oai_namespace: str

    :return: OAI identifier
    :rtype: str
    """
    if oai_namespace:
        nsmap = {
            None: oai_namespace
        }
    else:
        nsmap = cfg.get("OAIHARVESTER_DEFAULT_NAMESPACE_MAP")
    namespace_prefix = "{{{0}}}".format(oai_namespace)
    root = etree.fromstring(xml_string)
    node = root.find(".//{0}identifier".format(namespace_prefix), nsmap)
    if node is not None:
        return node.text


def collect_identifiers(harvested_file_list):
    """Collect all OAI PMH identifiers from each file in the list.

    Then adds them to a list of identifiers per file.

    :param harvested_file_list: list of filepaths to harvested files

    :return list of lists, containing each files' identifier list
    """
    result = []
    for harvested_file in harvested_file_list:
        try:
            fd_active = open(harvested_file)
        except IOError as e:
            raise e
        data = fd_active.read()
        fd_active.close()
        result.append(REGEXP_OAI_ID.findall(data))
    return result


def find_matching_files(basedir, filetypes):
    """Try to find all files matching given filetypes.

    By looking at all the files and filenames in the given directory,
    including subdirectories.

    :param basedir: full path to base directory to search in
    :type basedir: string

    :param filetypes: list of filetypes, extensions
    :type filetypes: list

    :return: exitcode and any error messages as: (exitcode, err_msg)
    :rtype: tuple
    """
    files_list = []
    for dirpath, dummy0, filenames in os.walk(basedir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            dummy1, cmd_out, dummy2 = run_shell_command(
                'file %s', (full_path,)
            )
            for filetype in filetypes:
                if cmd_out.lower().find(filetype) > -1:
                    files_list.append(full_path)
                elif filename.split('.')[-1].lower() == filetype:
                    files_list.append(full_path)
    return files_list


def get_identifier_names(identifiers):
    """Return list of identifiers from a comma-separated string."""
    if identifiers is not None:
        return [s.strip() for s in identifiers.split(',')]
    return []


def update_lastrun(oaiharvest_object):
    """Update the 'lastrun' attribute of the OaiHARVEST object.

    :param oaiharvest_object: An OaiHARVEST object from the database.
    """
    oaiharvest_object.lastrun = datetime.now()
    oaiharvest_object.save()


def get_workflow_name(workflow, name):
    """Return the name of the workflow depending on whether a name was provided or not.

    :param workflow: The workflow name.
    :param name: The name of the oaiHARVEST object.
    """
    if workflow is not None:
        return workflow
    elif name is not None:
        obj = get_oaiharvest_object(name)
        return obj.workflows
    else:
        from invenio_oaiharvester.errors import WorkflowNotFound
        raise WorkflowNotFound("Workflow not found. Try '-o workflow -w <workflow name> or provide a name (-n <name>).")


def get_oaiharvest_object(name):
    """Query and returns an OaiHARVEST object based on its name.

    :param name: The name of the OaiHARVEST object.
    :return: The OaiHARVEST object.
    """
    from invenio_oaiharvester.models import OaiHARVEST
    return OaiHARVEST.query.filter_by(name=name).first()


def check_or_create_dir(output_dir):
    """Check whether the directory exists, and creates it if not.

    :param output_dir: The directory where the output should be sent.
    """
    default = cfg['OAIHARVESTER_STORAGEDIR']
    path = os.path.join(default, output_dir)

    if not os.path.exists(path):
        os.makedirs(path)

    return path


def create_file_name(output_dir):
    """Create a random file name.

    :param output_dir: The directory where the file should be created.
    """
    from tempfile import NamedTemporaryFile
    prefix = 'oaiharvest_' + datetime.now().strftime('%Y-%m-%d') + '_'

    try:
        temp = NamedTemporaryFile(prefix=prefix, suffix='.xml', dir=output_dir, mode='w+')
        file_name = temp.name[:]
    finally:
        temp.close()
    return file_name


def write_to_dir(records, output_dir, max_records=1000):
    """Check if the output directory exists, and creates it if it does not.

    :param records: An iterator of harvested records.
    :param output_dir: The directory where the output should be sent.
    :param max_records: The max number of records to be written in a single file.
    """
    output_path = check_or_create_dir(output_dir)

    files_created = [create_file_name(output_path)]
    total = 0  # total number of records processed
    f = open(files_created[0], 'w+')

    for record in records:
        total += 1
        if total % max_records == 0:
            # we need a new file to write to
            f.close()
            files_created.append(create_file_name(output_path))
            f = open(files_created[-1], 'w+')

        f.write(record.raw)

    f.close()
    return files_created, total


def print_to_stdout(records):
    """Print the raw information of the records to the stdout.

    :param records: An iterator of harvested records.
    """
    total = 0
    for record in records:
        total += 1
        print(record.raw)
    return total


def print_files_created(files_created):
    """Print the paths to all files created.

    :param files_created: list of strings containing file paths
    """
    print('-------------------', file=sys.stderr)
    print('Harvested {0} files'.format(len(files_created)), file=sys.stderr)
    print('-------------------', file=sys.stderr)
    for path in files_created:
        print(path, file=sys.stderr)
    print()


def print_total_records(total):
    """Print the total number of harvested records.

    :param total: The total number of harvested records.
    """
    print('------------------------------', file=sys.stderr)
    print('Number of records harvested {0}'.format(total), file=sys.stderr)
    print('------------------------------', file=sys.stderr)
