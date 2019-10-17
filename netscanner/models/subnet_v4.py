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

import ipaddress

from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class SubnetV4(BaseModel):
    name = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('SubnetV4',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('SubnetV4',
                                                              'description'))
    subnet_ip = models.GenericIPAddressField(
        protocol='IPv4',
        verbose_name=pgettext_lazy('SubnetV4', 'Subnet IP'))
    cidr = models.PositiveSmallIntegerField(
        verbose_name=pgettext_lazy('SubnetV4', 'CIDR'))
    starting_ip = models.GenericIPAddressField(
        protocol='IPv4',
        verbose_name=pgettext_lazy('SubnetV4', 'Starting IP'))
    ending_ip = models.GenericIPAddressField(
        protocol='IPv4',
        verbose_name=pgettext_lazy('SubnetV4', 'Ending IP'))
    gateway_ip = models.GenericIPAddressField(
        protocol='IPv4',
        verbose_name=pgettext_lazy('SubnetV4', 'Gateway IP'))
    broadcast_ip = models.GenericIPAddressField(
        protocol='IPv4',
        verbose_name=pgettext_lazy('SubnetV4', 'Broadcast IP'))

    class Meta:
        # Define the database table
        db_table = 'netscanner_subnet_v4'
        ordering = ['name']
        verbose_name = pgettext_lazy('SubnetV4', 'Subnet version 4')
        verbose_name_plural = pgettext_lazy('SubnetV4', 'Subnets version 4')

    def __str__(self):
        return '{NAME}'.format(NAME=self.name)

    def get_ip_list(self) -> list:
        """
        Get the whole IP list for a network/CIDR
        """
        ip_network = ipaddress.ip_network('{}/{}'.format(self.subnet_ip,
                                                         self.cidr))
        return list(map(str, ip_network.hosts()))


class SubnetV4Admin(BaseModelAdmin):
    pass
