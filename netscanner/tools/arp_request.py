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
                 verbosity: int,
                 timeout: int):
        self.verbosity = verbosity
        self.timeout = timeout

    def execute(self,
                destination: str) -> dict:
        """
        Send an ARP request to the address (requires root access)
        """
        # Print destination for verbosity >= 2
        if self.verbosity >= 2:
            print(destination)
        broadcast = scapy.all.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp = scapy.all.ARP(pdst=destination)
        reply = scapy.all.srp(broadcast / arp,
                              timeout=self.timeout,
                              verbose=False)[0]
        result = reply[0][1].hwsrc.upper() if reply else None
        start_time = reply[0][0].sent_time if reply else 0
        end_time = reply[0][1].time if reply else 0
        duration = round((end_time - start_time) * 1000, 2) if reply else 0
        if duration < 0:
            # Workaround for negative duration
            # https://github.com/secdev/scapy/issues/1952
            duration = 0.00
        return {
            'mac_address': result,
            'status': bool(result),
            'start': start_time,
            'end': end_time,
            'duration': duration,
        }
