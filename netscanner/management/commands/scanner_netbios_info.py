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

from django.utils import timezone

from netscanner.management.discovery_base_command import DiscoveryBaseCommand
from netscanner.models import Discovery, Host
from netscanner.tools.netbios_smb_info import NetBIOSSMBInfo, PROTOCOL_NETBIOS


class Command(DiscoveryBaseCommand):
    help = 'Discover NetBIOS information'
    tool_name = 'netbios_info'

    def instance_scanner_tool(self,
                              discovery: Discovery,
                              options: dict):
        """
        Instance the scanner tool using the discovery options
        :param discovery: Discovery object that launches the tool
        :param options: dictionary containing the options
        :return:
        """
        return NetBIOSSMBInfo(verbosity=options.get('verbosity', 1),
                              timeout=discovery.timeout,
                              protocol=PROTOCOL_NETBIOS,
                              port=options.get('port', 139),
                              port_names=options.get('port_names', 137))

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
        # Process only valid entries
        for item in filter(lambda item: item[1]['status'], results):
            (address, values) = item
            # Print results if verbosity >= 1
            if self.verbosity >= 1:
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
