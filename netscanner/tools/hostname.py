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


class Hostname(object):
    def __init__(self,
                 verbosity: int):
        self.verbosity = verbosity

    def execute(self,
                destination: str) -> dict:
        """
        Resolve the address hostname
        """
        # Print destination for verbosity >= 2
        if self.verbosity >= 2:
            print(destination)
        result = socket.getfqdn(destination)
        return {
            'fqdn': result,
            'status': bool(result) and result != destination,
        }
