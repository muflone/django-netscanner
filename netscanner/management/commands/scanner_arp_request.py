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
import multiprocessing

from django.core.management.base import BaseCommand
from django.utils import timezone

from netscanner.models import Discovery, Host
from netscanner.tools.arp_request import ARPRequest
from netscanner.utils.consumers import Consumers


class Command(BaseCommand):
    help = 'Discover network hosts using ARP requests'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--workers',
                            action='store',
                            type=int,
                            default=10)
        parser.add_argument('--timeout',
                            action='store',
                            type=int,
                            default=1)

    def handle(self, *args, **options):
        discoveries = Discovery.objects.filter(scanner__tool='arp_request')

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
            for reserved_options in ('verbosity', 'settings', 'pythonpath',
                                     'traceback', 'no_color', 'force_color'):
                if reserved_options in discovery_options:
                    del discovery_options[reserved_options]
            # Prepare addresses to discover
            tasks = multiprocessing.JoinableQueue()
            for address in discovery.subnetv4.get_ip_list():
                tasks.put(address)
            # Prepare consumers to execute the network discovery
            consumers = Consumers(tasks_queue=tasks)
            tool = ARPRequest(discovery_options['timeout'])
            consumers.execute(runners=discovery_options['workers'],
                              action=tool.execute)
            # Process results
            for item in consumers.results_as_list():
                if item and item[1]:
                    # Update MAC Address
                    address = item[0]
                    self.stdout.write(item[0])
                    hosts = Host.objects.filter(address=address)
                    if hosts:
                        # Update existing hosts
                        for host in hosts:
                            # Update only if not excluded from discovery
                            if not host.no_discovery:
                                host.mac_address = item[1].replace(':', '')
                                host.last_seen = timezone.now()
                                host.save()
                    else:
                        # Insert new host
                        host = Host.objects.create()
                        host.name = address
                        host.address = address
                        host.subnetv4 = discovery.subnetv4
                        host.mac_address = item[1].replace(':', '')
                        host.last_seen = timezone.now()
                        host.save()
            # Update last scan discovery
            discovery.last_scan = timezone.now()
            discovery.save()
