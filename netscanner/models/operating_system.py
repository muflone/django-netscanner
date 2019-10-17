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


class OperatingSystem(BaseModel):
    brand = models.ForeignKey('Brand',
                              on_delete=models.PROTECT,
                              verbose_name=pgettext_lazy('OperatingSystem',
                                                         'brand'))
    name = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('OperatingSystem',
                                                       'name'))
    version = models.CharField(max_length=255,
                               verbose_name=pgettext_lazy('OperatingSystem',
                                                          'version'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy(
                                       'OperatingSystem',
                                       'description'))

    class Meta:
        # Define the database table
        db_table = 'netscanner_operating_system'
        ordering = ['brand', 'name', 'version']
        unique_together = ('brand', 'name', 'version')
        verbose_name = pgettext_lazy('OperatingSystem', 'Operating System')
        verbose_name_plural = pgettext_lazy('OperatingSystem',
                                            'Operating Systems')

    def __str__(self):
        return '{BRAND} {NAME} {VERSION}'.format(BRAND=self.brand.description,
                                                 NAME=self.name,
                                                 VERSION=self.version)


class OperatingSystemAdmin(BaseModelAdmin):
    pass
