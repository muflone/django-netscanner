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

from django.utils import timezone

from netscanner.management.management_base_command import ManagementBaseCommand
from netscanner.models import Discovery, Host
from netscanner.tools.icmp_reply import ICMPReply


class Command(ManagementBaseCommand):
    help = 'Discover network hosts using ICMP reply requests'
    tool_name = 'icmp_reply'

    def __init__(self):
        super().__init__()

    def add_arguments(self, parser: argparse.ArgumentParser):
        super().add_arguments(parser)
        parser.add_argument('--workers',
                            action='store',
                            type=int,
                            default=10)

    def instance_scanner_tool(self,
                              discovery: Discovery,
                              options: dict):
        """
        Instance the scanner tool using the discovery options
        :param discovery: Discovery object that launches the tool
        :param options: dictionary containing the options
        :return:
        """
        return ICMPReply(timeout=discovery.timeout)

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
        super().process_results(discovery, options, results)
        for item in results:
            (address, values) = item
            self.print('%-18s %s' % (address, values))
            # Update last seen time
            hosts = Host.objects.filter(address=address)
            if hosts:
                # Update existing hosts
                for host in hosts:
                    # Update only if not excluded from discovery
                    if not host.no_discovery:
                        host.last_seen = timezone.now()
                        host.save()
            else:
                # Insert new host
                host = Host.objects.create()
                host.name = address
                host.address = address
                host.subnetv4 = discovery.subnetv4
                host.last_seen = timezone.now()
                host.save()
