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
import json
import time

from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone
from django.utils.translation import pgettext_lazy

from netscanner.management.discovery_base_command import DiscoveryBaseCommand
from netscanner.models import Discovery

from . import discovery_tool_commands


class Command(BaseCommand):
    help = 'Discovery sequence'

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        BaseCommand.add_arguments(self, parser)
        parser.add_argument('--discovery',
                            action='store',
                            type=str,
                            required=True,
                            help=pgettext_lazy(
                                'Scanner Sequence',
                                'Discovery to execute'))
        parser.add_argument('--disabled',
                            action='store_true',
                            default=False,
                            help=pgettext_lazy(
                                'Scanner Sequence',
                                'Launch also disabled discoveries'))
        parser.add_argument('--destinations',
                            action='store',
                            type=str,
                            required=False,
                            help=pgettext_lazy(
                                'Scanner Sequence',
                                'Execute the discovery only to the selected '
                                'destinations'))

    def handle(self, *args, **options) -> None:
        management_command = DiscoveryBaseCommand()
        # Set verbosity level
        management_command.verbosity = options['verbosity']
        # Get Discovery
        try:
            sequence = Discovery.objects.get(name=options['discovery'])
        except models.ObjectDoesNotExist:
            # Not existing Discovery
            sequence = None
            if management_command.verbosity >= 1:
                management_command.print('No discovery named "{NAME}"'.format(
                    NAME=options['discovery']))
        if sequence:
            destinations = (options['destinations'].split(' ')
                            if options['destinations']
                            else None)
            operations = json.loads(sequence.options)
            # Execute only enabled discoveries or any if disabled is passed
            if sequence.enabled or options['disabled']:
                # Find the tool for the requested discovery
                for operation in operations:
                    discovery = Discovery.objects.get(
                        name=operation['discovery'])
                    for command in discovery_tool_commands:
                        if command.tool_name == discovery.scanner.tool:
                            if management_command.verbosity >= 1:
                                management_command.print(
                                    'Executing discovery {DISCOVERY}'.format(
                                        DISCOVERY=discovery.name))
                            # Execute discovery for the requested tool
                            command().do_discovery(
                                discovery=discovery,
                                options=management_command.get_options(
                                    general_options={**options},
                                    scanner_options=discovery.scanner.options,
                                    discovery_options=discovery.options),
                                destinations=destinations)
                            # Sleep after the discovery
                            if operation['wait'] > 0:
                                if management_command.verbosity >= 1:
                                    management_command.print(
                                        'Sleeping for {WAIT} seconds '
                                        'after discovery {DISCOVERY}'.format(
                                            WAIT=operation['wait'],
                                            DISCOVERY=discovery.name))
                                time.sleep(operation['wait'])
                            break
                # Update last scan discovery
                sequence = Discovery.objects.get(name=options['discovery'])
                sequence.last_scan = timezone.now()
                sequence.save()
            else:
                # Disabled discovery
                if management_command.verbosity >= 1:
                    management_command.print(
                        'The discovery "{NAME}" is disabled'.format(
                            NAME=sequence.name))
