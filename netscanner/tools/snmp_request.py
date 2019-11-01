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

import easysnmp

from .snmp_get_info import SNMPGetInfo


class SNMPRequest(object):
    def __init__(self,
                 verbosity: int,
                 timeout: int,
                 port: int,
                 version: str,
                 community: str,
                 retries: int,
                 values: list):
        self.verbosity = verbosity
        self.timeout = timeout
        self.port = port
        self.snmp_version = version
        self.snmp_community = community
        self.retries = retries
        self.values = values

    def execute(self,
                destination: str) -> dict:
        """
        Scan a destination for SNMP values
        """
        results = {}
        # Print destination for verbosity >= 2
        if self.verbosity >= 2:
            print(destination)
        snmp_version = {'v1': 1,
                        'v2c': 2}.get(self.snmp_version, 2)
        session = easysnmp.session.Session(hostname=destination,
                                           remote_port=self.port,
                                           version=snmp_version,
                                           community=self.snmp_community,
                                           timeout=self.timeout,
                                           retries=self.retries)
        for value in self.values:
            if self.verbosity >= 3:
                print(destination, value.name, value.oid)
            try:
                results[value.name] = SNMPGetInfo.format_snmp_value(
                    value=session.get(value.oid),
                    format=value.format,
                    lstrip=value.lstrip,
                    rstrip=value.rstrip)
            except SystemError:
                # Handle SystemError bug under Python >= 3.7
                # https://github.com/kamakazikamikaze/easysnmp/issues/108
                pass
        # Add status
        results['status'] = bool(results)
        return results
