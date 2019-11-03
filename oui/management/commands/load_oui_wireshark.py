##
#     Project: Django NetScanner
# Description: A Django application to make network scans
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2019 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import argparse

from django.core.management.base import BaseCommand
from django.utils.translation import pgettext

from oui.models import Oui


class Command(BaseCommand):
    """
    The Wireshark manuf file has the following format:
    00:12:34    Vendor    Vendor name
    00:12:34:56:78:90/36    Vendor Vendor name
    Each field is separated by a tab character

    https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf;hb=HEAD
    """
    help = 'Load OUI from Wireshark manuf file'

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        BaseCommand.add_arguments(self, parser)
        parser.add_argument('--filename',
                            action='store',
                            type=str,
                            required=True,
                            help=pgettext('Load OUI Wireshark',
                                          'filename'))
        parser.add_argument('--count',
                            action='store',
                            type=int,
                            required=False,
                            default=1000,
                            help=pgettext('Load OUI Wireshark',
                                          'items count to insert per batch'))

    def handle(self, *args, **options) -> None:
        # Load existing prefixes
        existing_prefixes = {prefix[0]
                             for prefix
                             in Oui.objects.all().values_list('prefix')}
        try:
            # List of prepared Oui to insert later using bulk_create
            list_oui = []
            file_oui = open(options['filename'], 'r')
            for line in file_oui:
                # Strip comments
                if '#' in line:
                    line = line[:line.find('#')]
                # Remove spaces and newlines
                line = line.strip()
                if '\t' in line:
                    prefix, vendor = line.split('\t', 1)
                    prefix = prefix.replace(':', '').replace('-', '').upper()
                    # Use full vendor if present (3rd field)
                    if '\t' in vendor:
                        vendor = vendor.split('\t', 1)[1]
                    # Check for duplicated prefix
                    if prefix == '000000':
                        # Skip invalid initial line with 00:00:00
                        pass
                    elif prefix not in existing_prefixes:
                        # Valid prefix, add to queue
                        list_oui.append(Oui(prefix=prefix,
                                            organization=vendor,
                                            address=''))
                        existing_prefixes.add(prefix)
                    else:
                        # Skip duplicated prefixes
                        print('Existing prefix "{PREFIX}", skipping'.format(
                            PREFIX=prefix))
                elif line:
                    # Invalid line, no tab character
                    print('Invalid line in file: {LINE}'.format(LINE=line))
                # Commit data to Model
                if len(list_oui) >= options['count']:
                    Oui.objects.bulk_create(list_oui)
                    list_oui = []
            # Commit last block of changes
            Oui.objects.bulk_create(list_oui)
            # Close input file
            file_oui.close()
        except FileNotFoundError:
            # Invalid filename
            print('File "{FILENAME}" not found'.format(
                FILENAME=options['filename']))
