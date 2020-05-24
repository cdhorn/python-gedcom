# -*- coding: utf-8 -*-

# Python GEDCOM Parser
#
# Copyright (C) 2020 Christopher Horn (cdhorn at embarqmail dot com)
# Copyright (C) 2018 Damon Brodie (damon.brodie at gmail.com)
# Copyright (C) 2018-2019 Nicklas Reincke (contact at reynke.com)
# Copyright (C) 2016 Andreas Oberritter
# Copyright (C) 2012 Madeleine Price Ball
# Copyright (C) 2005 Daniel Zappala (zappala at cs.byu.edu)
# Copyright (C) 2005 Brigham Young University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Further information about the license: http://www.gnu.org/licenses/gpl-2.0.html

"""
GEDCOM element for a `SOURCE_RECORD` source record identified by the
`gedcom.tags.GEDCOM_TAG_SOURCE` tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.change_date import change_date
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.multimedia_link import multimedia_link
from gedcom.subparsers.user_reference_number import user_reference_number
from gedcom.subparsers.source_repository_citation import source_repository_citation

SOURCE_PLURAL_TAGS = {
    tags.GEDCOM_TAG_AUTHOR: 'author',
    tags.GEDCOM_TAG_TITLE: 'title',
    tags.GEDCOM_TAG_PUBLICATION: 'publication',
    tags.GEDCOM_TAG_TEXT: 'text'
}

SOURCE_SINGLE_TAGS = {
    tags.GEDCOM_TAG_ABBREVIATION: 'abbreviation',
    tags.GEDCOM_TAG_REC_ID_NUMBER: 'record_id',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_APID: 'apid'
}


class SourceElement(Element):
    """Element associated with a SOURCE_RECORD"""

    def get_tag(self) -> str:
        return tags.GEDCOM_TAG_SOURCE

    def get_record(self) -> dict:
        """Parse and return the full record in dictionary format.
        """
        record = {
            'key_to_source': self.get_pointer(),
            'data': {
                'events': '',
                'date': '',
                'place': '',
                'agency': '',
                'notes': []
            },
            'author': '',
            'title': '',
            'abbreviation': '',
            'publication': '',
            'text': '',
            'repository': {},
            'references': [],
            'record_id': '',
            'change_date': {},
            'notes': [],
            'media': [],
            'apid': ''
        }
        for child in self.get_child_elements():
            if child.get_tag() in SOURCE_PLURAL_TAGS:
                record[SOURCE_PLURAL_TAGS[child.get_tag()]] = child.get_multi_line_value()
                continue

            if child.get_tag() in SOURCE_SINGLE_TAGS:
                record[SOURCE_SINGLE_TAGS[child.get_tag()]] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_NOTE:
                record['notes'].append(note_structure(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_OBJECT:
                record['media'].append(multimedia_link(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REPOSITORY:
                record['repository'] = source_repository_citation(child)
                continue

            if child.get_tag() == tags.GEDCOM_TAG_DATA:
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_EVENT:
                        record['data']['events'] = gchild.get_value()
                        for ggchild in gchild.get_child_elements():
                            if ggchild.get_tag() == tags.GEDCOM_TAG_DATE:
                                record['data']['date'] = ggchild.get_value()
                                continue

                            if ggchild.get_tag() == tags.GEDCOM_TAG_PLACE:
                                record['data']['place'] = ggchild.get_value()
                        continue

                    if gchild.get_tag() == tags.GEDCOM_TAG_AGENCY:
                        record['data']['agency'] = gchild.get_value()
                        continue

                    if gchild.get_tag() == tags.GEDCOM_TAG_NOTE:
                        record['data']['notes'].append(note_structure(gchild))
                        continue

            if child.get_tag() == tags.GEDCOM_TAG_REFERENCE:
                record['references'].append(user_reference_number(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHANGE:
                record['change_date'] = change_date(child)
                continue

        return record
