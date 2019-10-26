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


class SNMPConfiguration(BaseModel):
    device_model = models.ForeignKey('DeviceModel',
                                     blank=True,
                                     null=True,
                                     default=None,
                                     on_delete=models.PROTECT,
                                     verbose_name=pgettext_lazy(
                                         'SNMPConfiguration',
                                         'Device model'))
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name=pgettext_lazy('SNMPConfiguration',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy(
                                       'SNMPConfiguration',
                                       'description'))
    values = models.ManyToManyField(
        'SNMPValue',
        db_table='netscanner_snmp_configuration_values',
        blank=True,
        verbose_name=pgettext_lazy('SNMPConfiguration',
                                   'SNMP values'))
    autodetect = models.ForeignKey('SNMPValue',
                                   blank=True,
                                   null=True,
                                   default=None,
                                   on_delete=models.PROTECT,
                                   related_name=(
                                       'snmp_configuration_autodetect'),
                                   verbose_name=pgettext_lazy(
                                       'SNMPConfiguration',
                                       'Autodetect value'))
    format = models.CharField(max_length=255,
                              blank=True,
                              verbose_name=pgettext_lazy('SNMPConfiguration',
                                                         'Format string'))
    lstrip = models.BooleanField(default=False,
                                 verbose_name=pgettext_lazy(
                                     'SNMPConfiguration',
                                     'Strip spaces on the left'))
    rstrip = models.BooleanField(default=False,
                                 verbose_name=pgettext_lazy(
                                     'SNMPConfiguration',
                                     'Strip spaces on the right'))
    value = models.CharField(max_length=255,
                             default='',
                             verbose_name=pgettext_lazy('SNMPConfiguration',
                                                        'Resulting value'))

    class Meta:
        # Define the database table
        db_table = 'netscanner_snmp_configuration'
        ordering = ['device_model', 'name']
        verbose_name = pgettext_lazy('SNMPConfiguration', 'SNMP Configuration')
        verbose_name_plural = pgettext_lazy('SNMPConfiguration',
                                            'SNMP Configurations')

    def __str__(self):
        return '{NAME}'.format(NAME=self.name)


class SNMPConfigurationAdmin(BaseModelAdmin):
    pass
