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

from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class Discovery(BaseModel):
    name = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('Discovery',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('Discovery',
                                                              'description'))
    subnetv4 = models.ForeignKey('SubnetV4',
                                 on_delete=models.PROTECT,
                                 verbose_name=pgettext_lazy('Discovery',
                                                            'subnet v4'))
    enabled = models.BooleanField(verbose_name=pgettext_lazy('Discovery',
                                                             'enabled'))
    scanner = models.ForeignKey('Scanner',
                                on_delete=models.PROTECT,
                                verbose_name=pgettext_lazy('Discover',
                                                           'scanner'))
    options = models.TextField(blank=True,
                               verbose_name=pgettext_lazy('Discover',
                                                          'options'))
    interval = models.PositiveIntegerField(
        verbose_name=pgettext_lazy('Discovery',
                                   'scan interval'))
    last_scan = models.DateTimeField(blank=True,
                                     null=True,
                                     default=None,
                                     verbose_name=pgettext_lazy('Discovery',
                                                                'last scan'))

    class Meta:
        # Define the database table
        db_table = 'netscanner_discovery'
        ordering = ['name']
        verbose_name = pgettext_lazy('Discovery', 'Discovery')
        verbose_name_plural = pgettext_lazy('Discovery', 'Discoveries')

    def __str__(self):
        return '{NAME}'.format(NAME=self.name)


class DiscoveryAdmin(BaseModelAdmin):
    pass
