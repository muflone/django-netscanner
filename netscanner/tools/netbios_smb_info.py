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

# Based on inbtscan (https://github.com/iiilin/inbtscan)

import socket
import datetime

NetBIOS_ITEM_TYPE = {
    b'\x01\x00': 'netbios_computer_name',
    b'\x02\x00': 'netbios_domain_name',
    b'\x03\x00': 'dns_computer_name',
    b'\x04\x00': 'dns_domain_name',
}

PROTOCOL_NETBIOS = 0
PROTOCOL_SMB = 1


class NetBIOSSMBInfo(object):
    def __init__(self,
                 verbosity: int,
                 timeout: int,
                 protocol: int,
                 port: int,
                 port_names: int):
        self.verbosity = verbosity
        self.timeout = timeout
        self.protocol = protocol
        # Port used for NetBIOS and SMB data
        self.port = port
        # Port used for NetBIOS names only
        self.port_names = port_names

    def execute(self,
                destination: str) -> dict:
        """
        Inspect NetBIOS and SMB info
        """
        results = {}
        # Print destination for verbosity >= 2
        if self.verbosity >= 2:
            print(destination)
        if self.protocol == PROTOCOL_NETBIOS:
            nbns_result = self._get_netbios_names(destination)
            if not nbns_result or not nbns_result['unique_names']:
                return {'status': False}
            results['names'] = nbns_result['unique_names']
            results['group'] = nbns_result['group']

        sock = socket.socket(family=socket.AF_INET,
                             type=socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        try:
            sock.connect((destination, self.port))
            if self.protocol == PROTOCOL_NETBIOS:
                payload = (b'\x81\x00\x00D ' +
                           self._netbios_encode_name(results['names'][0]) +
                           b'\x00 EOENEBFACACACACACACACACACACACACA\x00')
                sock.send(payload)
                sock.recv(1024)

            payload = (b'\x00\x00\x00\x85\xff\x53\x4d\x42\x72\x00\x00\x00\x00'
                       b'\x18\x53\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                       b'\x00\x00\x00\x00\xff\xfe\x00\x00\x00\x00\x00\x62\x00'
                       b'\x02\x50\x43\x20\x4e\x45\x54\x57\x4f\x52\x4b\x20\x50'
                       b'\x52\x4f\x47\x52\x41\x4d\x20\x31\x2e\x30\x00\x02\x4c'
                       b'\x41\x4e\x4d\x41\x4e\x31\x2e\x30\x00\x02\x57\x69\x6e'
                       b'\x64\x6f\x77\x73\x20\x66\x6f\x72\x20\x57\x6f\x72\x6b'
                       b'\x67\x72\x6f\x75\x70\x73\x20\x33\x2e\x31\x61\x00\x02'
                       b'\x4c\x4d\x31\x2e\x32\x58\x30\x30\x32\x00\x02\x4c\x41'
                       b'\x4e\x4d\x41\x4e\x32\x2e\x31\x00\x02\x4e\x54\x20\x4c'
                       b'\x4d\x20\x30\x2e\x31\x32\x00')
            sock.send(payload)
            sock.recv(1024)

            payload = (b'\x00\x00\x01\x0a\xff\x53\x4d\x42\x73\x00\x00\x00\x00'
                       b'\x18\x07\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                       b'\x00\x00\x00\x00\xff\xfe\x00\x00\x40\x00\x0c\xff\x00'
                       b'\x0a\x01\x04\x41\x32\x00\x00\x00\x00\x00\x00\x00\x4a'
                       b'\x00\x00\x00\x00\x00\xd4\x00\x00\xa0\xcf\x00\x60\x48'
                       b'\x06\x06\x2b\x06\x01\x05\x05\x02\xa0\x3e\x30\x3c\xa0'
                       b'\x0e\x30\x0c\x06\x0a\x2b\x06\x01\x04\x01\x82\x37\x02'
                       b'\x02\x0a\xa2\x2a\x04\x28\x4e\x54\x4c\x4d\x53\x53\x50'
                       b'\x00\x01\x00\x00\x00\x07\x82\x08\xa2\x00\x00\x00\x00'
                       b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05'
                       b'\x02\xce\x0e\x00\x00\x00\x0f\x00\x57\x00\x69\x00\x6e'
                       b'\x00\x64\x00\x6f\x00\x77\x00\x73\x00\x20\x00\x53\x00'
                       b'\x65\x00\x72\x00\x76\x00\x65\x00\x72\x00\x20\x00\x32'
                       b'\x00\x30\x00\x30\x00\x33\x00\x20\x00\x33\x00\x37\x00'
                       b'\x39\x00\x30\x00\x20\x00\x53\x00\x65\x00\x72\x00\x76'
                       b'\x00\x69\x00\x63\x00\x65\x00\x20\x00\x50\x00\x61\x00'
                       b'\x63\x00\x6b\x00\x20\x00\x32\x00\x00\x00\x00\x00\x57'
                       b'\x00\x69\x00\x6e\x00\x64\x00\x6f\x00\x77\x00\x73\x00'
                       b'\x20\x00\x53\x00\x65\x00\x72\x00\x76\x00\x65\x00\x72'
                       b'\x00\x20\x00\x32\x00\x30\x00\x30\x00\x33\x00\x20\x00'
                       b'\x35\x00\x2e\x00\x32\x00\x00\x00\x00\x00')
            sock.send(payload)
            ret = sock.recv(1024)
            sock.close()
            if len(ret) > 47:
                # Process response
                length = ord(ret[43:44]) + ord(ret[44:45]) * 256
                # Versions
                os_version = ret[47 + length:]
                versions = (os_version
                            .replace(b'\x00\x00', b'|')
                            .replace(b'\x00', b'')
                            .decode('UTF-8', errors='ignore').split('|'))
                results['version'] = [item for item in versions if item]
                start = ret.find(b'NTLMSSP')
                length = (ord(ret[start + 40:start + 41]) +
                          ord(ret[start + 41:start + 42]) * 256)
                offset = ord(ret[start + 44:start + 45])
                results['major'] = ord(ret[start + 48:start + 49])
                results['minor'] = ord(ret[start + 49:start + 50])
                results['build'] = (ord(ret[start + 50:start + 51]) +
                                    256 * ord(ret[start + 51:start + 52]))
                results['ntlm_revision'] = ord(ret[start + 55:start + 56])
                # Process results
                index = start + offset
                while index < start + offset + length:
                    item_type = ret[index:index + 2]
                    item_length = (ord(ret[index + 2:index + 3]) +
                                   ord(ret[index + 3:index + 4]) * 256)
                    item_content = (ret[index + 4: index + 4 + item_length]
                                    .replace(b'\x00', b''))
                    if item_type == b'\x07\x00':
                        # Timestamp
                        timestamp = int.from_bytes(bytes=item_content,
                                                   byteorder='little')
                        EPOCH_AS_FILETIME = 116444736000000000
                        timestamp = datetime.datetime.fromtimestamp(
                            (timestamp - EPOCH_AS_FILETIME) / 10000000)
                        results['timestamp'] = timestamp
                    elif item_type in NetBIOS_ITEM_TYPE:
                        # Other data
                        value = item_content.decode(errors='ignore')
                        results[NetBIOS_ITEM_TYPE[item_type]] = value
                    elif item_type == b'\x00\x00':
                        # End of the data
                        break
                    index += 4 + item_length
        except socket.error:
            # Skip exceptions
            pass
        # Add status
        results['status'] = bool(results)
        # Add timestamp
        results['timestamp'] = datetime.datetime.now().timestamp()
        return results

    def _get_netbios_names(self,
                           destination: str) -> dict:
        """
        Get a dictionary object containing the workgroup and a list of
        unique computer names

        :param destination: address to connect to to get information
        :return: dictionary object with workgroup and computer unique names
        """
        try:
            sock = socket.socket(family=socket.AF_INET,
                                 type=socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            payload = (b'ff\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00 '
                       b'CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00\x00!\x00\x01')
            sock.sendto(payload, (destination, self.port_names))
            rep = sock.recv(2000)
            if isinstance(rep, str):
                rep = bytes(rep)

            unique_names = []
            group = ''
            # Number of answers
            num = ord(rep[56:57].decode())
            # Answer start
            data = rep[57:]
            for answer in range(num):
                answer_start = 18 * answer
                name = data[answer_start:answer_start + 15].decode().strip()
                flag_bit = bytes(data[answer_start + 15:answer_start + 16])
                if flag_bit == b'\x00':
                    name_flags = data[answer_start + 16:answer_start + 18]
                    if ord(name_flags[0:1]) >= 128:
                        group = name
                    else:
                        unique_names.append(name)
            return {'group': group,
                    'unique_names': unique_names}
        except socket.error:
            return {}

    def _netbios_encode_name(self,
                             name: str) -> bytes:
        """
        Encode a NetBIOS computer name
        :param name: computer name to encode
        :return: byte string with the encoded computer name
        """
        src = name.ljust(16, "\x20")
        names = []
        for c in src:
            char_ord = ord(c)
            high_4_bits = char_ord >> 4
            low_4_bits = char_ord & 0x0f
            names.append(high_4_bits)
            names.append(low_4_bits)

        result = b''
        for name in names:
            result += chr(0x41 + name).encode()
        return result
