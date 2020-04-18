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
from django.db import models
from django.utils.translation import pgettext_lazy

from netscanner.management.discovery_base_command import DiscoveryBaseCommand
from netscanner.models import Discovery

from . import discovery_tool_commands


class Command(BaseCommand):
    help = 'Custom Discovery'

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        BaseCommand.add_arguments(self, parser)
        parser.add_argument('--discovery',
                            action='store',
                            type=str,
                            required=True,
                            help=pgettext_lazy(
                                'Scanner Custom',
                                'Discovery to execute'))
        parser.add_argument('--disabled',
                            action='store_true',
                            default=False,
                            help=pgettext_lazy(
                                'Scanner Custom',
                                'Launch also disabled discoveries'))
        parser.add_argument('--failing',
                            action='store_true',
                            default=False,
                            help=pgettext_lazy(
                                'Scanner Custom',
                                'Save results also for failing hosts'))
        parser.add_argument('--destinations',
                            action='store',
                            type=str,
                            required=False,
                            help=pgettext_lazy(
                                'Scanner Custom',
                                'Execute the discovery only to the selected '
                                'destinations'))

    def handle(self, *args, **options) -> None:
        management_command = DiscoveryBaseCommand()
        # Set verbosity level
        management_command.verbosity = options['verbosity']
        # Get Discovery
        try:
            discovery = Discovery.objects.get(name=options['discovery'])
        except models.ObjectDoesNotExist:
            # Not existing Discovery
            discovery = None
            if management_command.verbosity >= 1:
                management_command.print('No discovery named "{NAME}"'.format(
                    NAME=options['discovery']))
        if discovery:
            destinations = (options['destinations'].split(' ')
                            if options['destinations']
                            else None)
            # Execute only enabled discoveries or any if disabled is passed
            if discovery.enabled or options['disabled']:
                # Find the tool for the requested discovery
                for command in discovery_tool_commands:
                    if command.tool_name == discovery.scanner.tool:
                        # Execute discovery for the requested tool
                        command().do_discovery(
                            discovery=discovery,
                            options=management_command.get_options(
                                general_options={**options},
                                scanner_options=discovery.scanner.options,
                                discovery_options=discovery.options),
                            destinations=destinations)
                        break
            else:
                # Disabled discovery
                if management_command.verbosity >= 1:
                    management_command.print(
                        'The discovery "{NAME}" is disabled'.format(
                            NAME=discovery.name))
