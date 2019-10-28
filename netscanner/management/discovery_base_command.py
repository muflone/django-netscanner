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
import datetime
import json
import multiprocessing

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from netscanner.models import Discovery, DiscoveryResult
from netscanner.utils.consumers import Consumers


class DiscoveryBaseCommand(BaseCommand):
    def __init__(self):
        """
        Discovery base command for all management discovery commands
        Use scanner_tool string to choose the desider scanner to use
        """
        BaseCommand.__init__(self)
        # Automatically save a DiscoveryResult record for each successful
        # discovery result
        self.save_results = True
        # Verbosity level for printing results
        self.verbosity = 0

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        BaseCommand.add_arguments(self, parser)

    def handle(self, *args, **options) -> None:
        discoveries = Discovery.objects.filter(scanner__tool=self.tool_name,
                                               enabled=True)
        for discovery in discoveries:
            # Define options (Command line + Scanner + Discovery)
            discovery_options = {**options}
            # Add Scanner options
            if discovery.scanner.options:
                discovery_options.update(json.loads(discovery.scanner.options))
            # Add Discovery options
            if discovery.options:
                discovery_options.update(json.loads(discovery.options))
            # Exlude Django reserved options
            for reserved_options in ('settings', 'pythonpath',
                                     'traceback', 'no_color', 'force_color'):
                if reserved_options in discovery_options:
                    del discovery_options[reserved_options]
            # Save verbosity level
            self.verbosity = discovery_options['verbosity']
            # Prepare addresses to discover
            tasks = multiprocessing.JoinableQueue()
            for address in discovery.subnetv4.get_ip_list():
                tasks.put(address)
            # Prepare consumers to execute the network discovery
            consumers = Consumers(tasks_queue=tasks)
            # Instance the scanner tool using the discovery options
            tool = self.instance_scanner_tool(discovery=discovery,
                                              options=discovery_options)
            if tool:
                # Print results if verbosity > 0
                if self.verbosity > 0:
                    self.print('Discovery "{DISCOVERY}" - '
                               'workers: {WORKERS}, '
                               'timeout: {TIMEOUT}, '
                               'options: {OPTIONS}'.format(
                                   DISCOVERY=discovery.name,
                                   WORKERS=discovery.workers,
                                   TIMEOUT=discovery.timeout,
                                   OPTIONS=discovery_options))
                consumers.execute(runners=discovery.workers,
                                  action=tool.execute)
                # Process the results in a single operation on the DB side
                with transaction.atomic():
                    # Exclude invalid items from their status
                    results = list(filter(lambda item: item[1]['status'],
                                          consumers.results_as_list()))
                    # Process the results to update the models, if needed
                    self.process_results(discovery=discovery,
                                         options=options,
                                         results=results)
                    # Update last scan discovery
                    discovery = Discovery.objects.get(pk=discovery.pk)
                    discovery.last_scan = timezone.now()
                    discovery.save()

    def instance_scanner_tool(self,
                              discovery: Discovery,
                              options: dict):
        """
        Instance the scanner tool using the discovery options
        :param discovery: Discovery object that launches the tool
        :param options: dictionary containing the options
        :return:
        """
        return None

    def process_results(self,
                        discovery: Discovery,
                        options: dict,
                        results: list) -> None:
        """
        Process the results list
        :param discovery: the Discovery object that launched the scanner
        :param options: dictionary containing the options
        :param results: list of results to process
        :return: None
        """
        serialized_options = json.dumps(options)
        for item in results:
            serializable_values = {}
            address, values = item
            # Save only valid values (if results saving is disabled)
            if values and self.save_results:
                # Serialize values and skip invalid values in JSON
                for (key, value) in values.items():
                    if isinstance(value, datetime.datetime):
                        # Convert datetime to timestamps
                        serializable_values[key] = (
                            int(value.timestamp()))
                    elif isinstance(value, list):
                        # Convert lists to strings
                        serializable_values[key] = ', '.join(value)
                    else:
                        # Raw value
                        serializable_values[key] = value
                # Save the discovery result
                DiscoveryResult.objects.create(
                    discovery=discovery,
                    address=address,
                    options=serialized_options,
                    scan_datetime=timezone.now(),
                    results=(json.dumps(serializable_values)
                             if serializable_values
                             else '')
                )
        # Print results if verbosity > 0
        if self.verbosity > 0:
            self.print('Results:')

    def print(self,
              message: str) -> None:
        """
        Print a message to the console
        :param message:
        :return:
        """
        self.stdout.write(message)
