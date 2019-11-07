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

import datetime

import easysnmp

from netscanner.models import SNMPConfiguration
from ..models import Host


class SNMPGetInfo(object):
    def __init__(self,
                 verbosity: int,
                 timeout: int,
                 port: int,
                 retries: int):
        self.verbosity = verbosity
        self.timeout = timeout
        self.port = port
        self.retries = retries

    def execute(self,
                host: Host) -> dict:
        """
        Get the values using SNMP
        """
        # Print destination for verbosity >= 2
        if self.verbosity >= 2:
            print(host.address)
        if host.snmp_configuration:
            # Check host SNMP Configuration
            snmp_configurations = (host.snmp_configuration, )
        else:
            # Check model SNMP Configurations
            snmp_configurations = SNMPConfiguration.objects.filter(
                device_model__id=host.device_model.pk)
        result = {}
        if snmp_configurations:
            snmp_version = host.snmp_version
            session = easysnmp.session.Session(hostname=host.address,
                                               remote_port=self.port,
                                               version=snmp_version.version,
                                               community=(
                                                   host.snmp_community or
                                                   'public'),
                                               timeout=self.timeout or 30,
                                               retries=self.retries)
            # Cycle all SNMP Configurations
            for snmp_configuration in snmp_configurations:
                # Cycle all configured SNMP values and save values
                values = snmp_configuration.snmpconfigurationvalue_set.all()
                for snmp_configuration_value in values:
                    snmp_value = snmp_configuration_value.snmp_value
                    try:
                        result_name = '{SECTION} - {BRAND} - {NAME}'.format(
                            SECTION=snmp_value.section,
                            BRAND=snmp_value.brand,
                            NAME=snmp_value.name)
                        if self.verbosity >= 3:
                            print('destination="{}"'.format(host.address),
                                  'oid="{}"'.format(snmp_value.oid))
                        result_value = session.get(snmp_value.oid)
                        # Save values
                        result[result_name] = self.format_snmp_value(
                                value=result_value,
                                format=snmp_value.format,
                                lstrip=snmp_value.lstrip,
                                rstrip=snmp_value.rstrip)
                        if self.verbosity >= 3:
                            print('\r')
                            print('destination="{}"'.format(host.address),
                                  'requested value="{}"'.format(
                                      snmp_value.name),
                                  'oid="{}"'.format(snmp_value.oid),
                                  'value="{}"'.format(result[result_name]))
                        # SNMPConfigurationValue has field to set
                        if snmp_configuration_value.field:
                            result[snmp_configuration_value.field] = (
                                result[result_name])
                    except SystemError:
                        # Handle SystemError bug under Python >= 3.7
                        # https://github.com/kamakazikamikaze/easysnmp/issues/108
                        pass
        result['status'] = bool(result)
        return result

    @staticmethod
    def format_snmp_value(value: easysnmp.variables.SNMPVariable,
                          format: str,
                          lstrip: bool,
                          rstrip: bool) -> str:
        """
        Format SNMPVariable value using the SNMPValue configuration
        :param value: SNMPVariable object with value
        :param format: string format
        :param lstrip: boolean value to strip spaces on the left side
        :param rstrip: boolean value to strip spaces on the right side
        :return: interpreted value
        """
        result = None
        if value:
            if format == 'int':
                # Integer value
                result = int(value.value)
            elif format == 'timeticks':
                # Timeticks
                milliseconds = int(value.value) * 10
                result = (datetime.datetime.now() -
                          datetime.timedelta(milliseconds=milliseconds)
                          ).replace(microsecond=0)
            elif (format.startswith('[') and format.endswith(']')):
                # Slice string
                format_parts = list(map(int, format[1:-1].split(':')))
                if len(format_parts) == 1:
                    # Start only
                    result = value.value[format_parts[0]]
                elif len(format_parts) == 2:
                    # Start:End
                    result = value.value[format_parts[0]:
                                         format_parts[1]]
                elif len(format_parts) == 3:
                    # Start:End:Count
                    result = value.value[format_parts[0]:
                                         format_parts[1]:
                                         format_parts[2]]
                else:
                    # Whole string
                    result = value.value
                return result
            elif format == 'mac address':
                # MAC Address
                result = ''.join(['%0.2x' % ord(_)
                                  for _ in value.value]).upper()
            elif format.startswith('remove:'):
                # Remove symbols (space separated list)
                result = value.value
                format_parts = format[7:].split(' ')
                for symbol in format_parts:
                    result = result.replace(symbol, '')
            else:
                result = value.value
            # Strip spaces from the left side
            if isinstance(result, str) and lstrip:
                result = result.lstrip()
            # Strip spaces from the right side
            if isinstance(result, str) and rstrip:
                result = result.rstrip()
        return result
