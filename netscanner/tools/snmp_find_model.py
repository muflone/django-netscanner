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

from ..models import Host, SNMPConfiguration


class SNMPFindModel(object):
    def __init__(self,
                 verbosity: int,
                 timeout: int,
                 port: int,
                 version: str,
                 community: str,
                 retries: int,
                 skip_existing: bool,
                 configurations: list,
                 initial_configuration: SNMPConfiguration):
        self.verbosity = verbosity
        self.timeout = timeout
        self.port = port
        self.snmp_version = version
        self.snmp_community = community
        self.retries = retries
        self.skip_existing = skip_existing
        self.configurations = configurations
        self.initial_configuration = initial_configuration

    def execute(self,
                destination: str) -> dict:
        """
        Scan an IP address for SNMP values
        """
        result = {'status': False}
        # Print destination for verbosity >= 2
        if self.verbosity >= 2:
            print(destination)
        # Get existing hosts
        hosts = Host.objects.filter(address=destination)
        # Skip hosts with SNMP disabled
        if hosts.filter(snmp_version='off'):
            if self.verbosity >= 3:
                print('Host {DESTINATION} has SNMP disabled, skipping'.format(
                    DESTINATION=destination))
            return result
        # If requested, skip any existing hosts with the device model set
        if self.skip_existing and hosts.exclude(device_model__isnull=True):
            if self.verbosity >= 3:
                print('Host {DESTINATION} has DeviceModel, skipping'.format(
                    DESTINATION=destination))
            return result

        snmp_version = {'v1': 1,
                        'v2c': 2}.get(self.snmp_version, 2)
        session = easysnmp.session.Session(hostname=destination,
                                           remote_port=self.port,
                                           version=snmp_version,
                                           community=self.snmp_community,
                                           timeout=self.timeout,
                                           retries=self.retries)
        # First test an initial configuration before trying all configurations.
        # A reduced group of SNMP values will try to avoid to loop over
        # all the configuration models, resulting in a quicker scan.
        # If no values are probed from the initial configuration, no scan
        # will be done using the models configurations.
        if self.initial_configuration:
            value = None
            for snmp_value in self.initial_configuration.values.all():
                if self.verbosity >= 4:
                    print(destination,
                          'Initial configuration',
                          snmp_value.name,
                          snmp_value.oid)
                try:
                    value = SNMPGetInfo.format_snmp_value(
                        value=session.get(snmp_value.oid),
                        format=snmp_value.format,
                        lstrip=snmp_value.lstrip,
                        rstrip=snmp_value.rstrip)
                    if value is not None:
                        break
                except SystemError:
                    # Handle SystemError bug under Python >= 3.7
                    # https://github.com/kamakazikamikaze/easysnmp/issues/108
                    pass
            # If not a single value was found from the request, abort the scan
            if value is None:
                if self.verbosity >= 3:
                    print('Host {DESTINATION} does not respond to the SNMP'
                          'initial configuration, skipping'.format(
                              DESTINATION=destination))
                return result
        # Try every model for the best matching
        for configuration in self.configurations:
            try:
                value = SNMPGetInfo.format_snmp_value(
                    value=session.get(configuration.autodetect.oid),
                    format=configuration.format,
                    lstrip=configuration.lstrip,
                    rstrip=configuration.rstrip)
            except SystemError:
                # Handle SystemError bug under Python >= 3.7
                # https://github.com/kamakazikamikaze/easysnmp/issues/108
                value = None
            # Replace '${ }' with spaces in autodetection value
            # Django-admin automatically removes trailing whitespaces
            autodetect_value = configuration.value.replace('${ }', ' ')
            if self.verbosity >= 3:
                print('destination="{}"'.format(destination),
                      'requested value="{}"'.format(autodetect_value),
                      'oid="{}"'.format(configuration.autodetect.oid),
                      'value="{}"'.format(value))
            # Check if the value is the autodetection value
            if value and value == autodetect_value:
                # Save status and model
                result['status'] = True
                result['model_name'] = configuration.device_model.name
                result['model_id'] = configuration.device_model.id
                break
        # Add some information to the results
        if result['status']:
            result['version'] = self.snmp_version
        return result
