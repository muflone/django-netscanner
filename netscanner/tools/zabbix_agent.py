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
import socket
import struct


class ZabbixAgent(object):
    def __init__(self,
                 verbosity: int,
                 timeout: int,
                 port: int,
                 items: list):
        self.verbosity = verbosity
        self.timeout = timeout
        self.port = port
        self.items = items

    def execute(self,
                destination: str) -> dict:
        """
        Scan a destination for Zabbix Agent values
        """
        results = {}
        # Print destination for verbosity >= 2
        if self.verbosity >= 2:
            print(destination)
        for item in self.items:
            if self.verbosity >= 3:
                print(destination, item)
            try:
                # Connect to the server
                sock = socket.socket(family=socket.AF_INET,
                                     type=socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                sock.connect((destination, self.port))
                # Send data
                # [HEADER ZBXD][LENGTH 4 bytes][DATA]
                data = 'ZBXD\1{LENGTH}{DATA}'.format(
                    LENGTH=struct.pack('<Q', len(item)).decode('utf-8'),
                    DATA=item)
                sock.send(data.encode('utf-8'))
                value = sock.recv(4096).decode('utf-8')
                # Get results
                # [HEADER ZBXD][LENGTH 4 bytes][RESERVED 4 bytes][DATA]
                # https://www.zabbix.com/documentation/4.0/manual/appendix/protocols/header_datalen
                if value.startswith('ZBXD'):
                    # Check for unsupported value
                    if not value[13:].startswith('ZBX_NOTSUPPORTED'):
                        results[item] = value[13:]
                sock.close()
            except (ConnectionRefusedError,
                    OSError,
                    socket.timeout):
                # If an error was raised for the ping operation, cancel scan
                if item == 'agent.ping':
                    break
        # Add status
        results['status'] = bool(results)
        # Add timestamp
        results['timestamp'] = datetime.datetime.now().timestamp()
        return results
