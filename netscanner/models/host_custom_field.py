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

from django.contrib import admin
from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class HostCustomField(BaseModel):
    host = models.ForeignKey('Host',
                             blank=False,
                             null=True,
                             on_delete=models.PROTECT,
                             verbose_name=pgettext_lazy('HostCustomField',
                                                        'host'))
    field = models.ForeignKey('CustomField',
                              blank=False,
                              null=True,
                              on_delete=models.PROTECT,
                              verbose_name=pgettext_lazy('HostCustomField',
                                                         'field'))
    value = models.CharField(max_length=255,
                             verbose_name=pgettext_lazy('HostCustomField',
                                                        'value'))

    class Meta:
        # Define the database table
        db_table = 'netscanner_host_custom_fields'
        ordering = ['host', 'field']
        unique_together = (('host', 'field'))
        verbose_name = pgettext_lazy('HostCustomField', 'Host Custom field')
        verbose_name_plural = pgettext_lazy('HostCustomField',
                                            'Hosts Custom fields')

    def __str__(self):
        return '{HOST} {FIELD}'.format(HOST=self.host,
                                       FIELD=self.field)


class HostCustomFieldAdmin(BaseModelAdmin):
    pass


class HostCustomFieldInlineAdmin(admin.TabularInline):
    """
    Proxy Admin Inline to show children rows for HostCustomField
    """
    model = HostCustomField
    fields = ('field', 'value')
