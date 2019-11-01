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

from .host_snmp_get_info import Command as SNMPGetInfoCommand
from .scanner_arp_request import Command as ARPRequestCommand
from .scanner_hostname import Command as HostnameCommand
from .scanner_icmp_reply import Command as ICMPReplyCommand
from .scanner_netbios_info import Command as NetBIOSInfoCommand
from .scanner_raw_icmp_reply import Command as RawICMPReplyCommand
from .scanner_smb_info import Command as SmbInfoCommand
from .scanner_snmp_find_model import Command as SNMPFindCommand
from .scanner_snmp_request import Command as SNMPRequest
from .scanner_tcp_connect import Command as TCPConnectCommand

discovery_tool_commands = (ARPRequestCommand,
                           HostnameCommand,
                           ICMPReplyCommand,
                           NetBIOSInfoCommand,
                           RawICMPReplyCommand,
                           SmbInfoCommand,
                           SNMPFindCommand,
                           SNMPGetInfoCommand,
                           SNMPRequest,
                           TCPConnectCommand)
