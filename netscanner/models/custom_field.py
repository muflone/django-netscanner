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


class CustomField(BaseModel):
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name=pgettext_lazy('CustomField',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('CustomField',
                                                              'description'))

    class Meta:
        # Define the database table
        db_table = 'netscanner_custom_fields'
        ordering = ['name']
        verbose_name = pgettext_lazy('CustomField', 'Custom field')
        verbose_name_plural = pgettext_lazy('CustomField', 'Custom fields')

    def __str__(self):
        return '{NAME}'.format(NAME=self.name)


class CustomFieldAdmin(BaseModelAdmin):
    pass
