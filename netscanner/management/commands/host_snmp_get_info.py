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

from netscanner.management.host_base_command import HostBaseCommand
from netscanner.models import Discovery
from netscanner.tools.snmp_get_info import SNMPGetInfo


class Command(HostBaseCommand):
    help = 'Get SNMP information about existing hosts with model set'
    tool_name = 'snmp_get_info'

    def instance_scanner_tool(self,
                              discovery: Discovery,
                              options: dict):
        """
        Instance the scanner tool using the discovery options
        :param discovery: Discovery object that launches the tool
        :param options: dictionary containing the options
        :return:
        """
        return SNMPGetInfo(verbosity=options.get('verbosity', 1),
                           timeout=discovery.timeout,
                           port=options.get('port', 161),
                           retries=options.get('retries', 0))

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
            (host, values) = item
            # Print results if verbosity >= 1
            if self.verbosity >= 1:
                self.print('%-18s %s' % (host.address, values))
            # Update only if not excluded from discovery
            if not host.no_discovery:
                # Update last seen time
                host.last_seen = timezone.now()
                # Update host fields
                for key, value in values.items():
                    if (key.startswith('host.') and
                            # Existing attribute
                            hasattr(host, key[5:]) and
                            # Empty attribute value
                            not getattr(host, key[5:])):
                        setattr(host, key[5:], value)
                host.save()
