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

import socket


class TCPConnect(object):
    def __init__(self,
                 verbosity: int,
                 timeout: int,
                 portnr: int):
        self.verbosity = verbosity
        self.timeout = timeout
        self.portnr = portnr

    def execute(self,
                destination: str) -> dict:
        """
        Connect to an IP address using socket TCP connection
        """
        # Print destination for verbosity > 1
        if self.verbosity > 1:
            print(destination)
        sock = socket.socket(family=socket.AF_INET,
                             type=socket.SOCK_STREAM,
                             proto=socket.IPPROTO_TCP)
        try:
            sock.settimeout(self.timeout)
            sock.connect((destination, self.portnr))
            sock.close()
            result = True
        except (ConnectionRefusedError,
                OSError,
                socket.timeout):
            result = False
        return {
            'connected': result,
            'status': result
        }
