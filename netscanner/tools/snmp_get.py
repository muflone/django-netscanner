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

from ..models import Host, SNMPValue


class SNMPGet(object):
    def __init__(self,
                 timeout: int,
                 port: int):
        self.timeout = timeout
        self.port = port

    def execute(self,
                host: Host) -> dict:
        """
        Resolve the address hostname
        """
        snmp_configuration = (host.snmp_configuration or
                              host.device_model.snmp_configuration)
        result = {}
        if snmp_configuration:
            snmp_version = {'v1': 1,
                            'v2c': 2}.get(host.snmp_version, 2)
            session = easysnmp.session.Session(hostname=host.address,
                                               remote_port=self.port,
                                               version=snmp_version,
                                               community=(
                                                   host.snmp_community or
                                                   'public'),
                                               timeout=self.timeout or 30)
            for snmp_value in snmp_configuration.values.all():
                result[str(snmp_value)] = self.format_snmp_value(
                    snmp_value,
                    session.get(snmp_value.oid))
        result['status'] = bool(result)
        return result

    def format_snmp_value(self,
                          value_configuration: SNMPValue,
                          value: easysnmp.variables.SNMPVariable):
        """
        Format SNMPVariable value using the SNMPValue configuration
        :param value_configuration: SNMPValue object containing configuration
        :param value: SNMPVariable object with value
        :return: interpreted value
        """
        result = None
        if value:
            if value_configuration.format == 'int':
                # Integer value
                result = int(value.value)
            elif value_configuration.format == 'timeticks':
                # Timeticks
                milliseconds = int(value.value) * 10
                result = (datetime.datetime.now() -
                          datetime.timedelta(milliseconds=milliseconds)
                          ).replace(microsecond=0)
            elif value_configuration.format == 'mac address':
                # MAC Address
                result = ':'.join(['%0.2x' % ord(_) for _ in value.value])
            else:
                result = value.value
        return result
