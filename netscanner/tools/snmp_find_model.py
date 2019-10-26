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

from .snmp_get import SNMPGet

from ..models import Host


class SNMPFindModel(object):
    def __init__(self,
                 timeout: int,
                 port: int,
                 version: str,
                 community: str,
                 retries: int,
                 skip_existing: bool,
                 models: list):
        self.timeout = timeout
        self.port = port
        self.snmp_version = version
        self.snmp_community = community
        self.retries = retries
        self.skip_existing = skip_existing
        self.models = models

    def execute(self,
                destination: str) -> dict:
        """
        Scan an IP address for SNMP values
        """
        result = {'status': False}
        # If requested, skip any existing hosts with the device model set
        if self.skip_existing and Host.objects.filter(
                address=destination).exclude(
                device_model__isnull=True):
            return result

        snmp_version = {'v1': 1,
                        'v2c': 2}.get(self.snmp_version, 2)
        session = easysnmp.session.Session(hostname=destination,
                                           remote_port=self.port,
                                           version=snmp_version,
                                           community=self.snmp_community,
                                           timeout=self.timeout,
                                           retries=self.retries)
        # Try every model for the best matching
        for model in self.models:
            try:
                value = SNMPGet.format_snmp_value(
                    value_configuration=model.snmp_configuration.autodetect,
                    value=session.get(model.snmp_configuration.autodetect.oid)
                )
            except SystemError:
                # Handle SystemError bug under Python >= 3.7
                # https://github.com/kamakazikamikaze/easysnmp/issues/108
                value = None
            # Check if the value is the autodetection value
            if value and value == model.snmp_configuration.autodetect_value:
                # Get the first valid value
                result['status'] = True
                result['model_name'] = model.name
                result['model_id'] = model.id
                break
        # Add some information to the results
        if result['status']:
            result['version'] = self.snmp_version
        return result
