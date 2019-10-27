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

import scapy.all


class RawICMPReply(object):
    def __init__(self,
                 verbosity: int,
                 timeout: int):
        self.verbosity = verbosity
        self.timeout = timeout

    def execute(self,
                destination: str) -> dict:
        """
        Ping an IP address using Raw socket (requires root access)
        """
        # Print destination for verbosity > 1
        if self.verbosity > 1:
            print(destination)
        scapy.all.conf.L3socket = scapy.all.L3RawSocket
        ip_request = scapy.all.IP(dst=destination)
        ping = scapy.all.ICMP()
        reply = scapy.all.sr1(ip_request / ping,
                              timeout=self.timeout,
                              verbose=False)
        result = reply[0][1].code == 0 if reply else False
        return {
            'reply': result,
            'status': bool(result)
        }
