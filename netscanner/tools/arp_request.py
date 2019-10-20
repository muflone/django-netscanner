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


class ARPRequest(object):
    def __init__(self,
                 timeout: int):
        self.timeout = timeout

    def execute(self,
                destination: str) -> dict:
        """
        Send an ARP request to the address (requires root access)
        """
        broadcast = scapy.all.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp = scapy.all.ARP(pdst=destination)
        reply = scapy.all.srp(broadcast / arp,
                              timeout=self.timeout,
                              verbose=False)[0]
        result = reply[0][1].hwsrc.upper() if reply else None
        return {
            'mac_address': result,
            'status': bool(result)
        }
