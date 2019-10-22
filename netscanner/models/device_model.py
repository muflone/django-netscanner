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
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import pgettext_lazy

from ..forms.change_snmp_configuration import ChangeSNMPConfigurationForm

from utility.models import BaseModel, BaseModelAdmin


class DeviceModel(BaseModel):
    device_type = models.ForeignKey('DeviceType',
                                    on_delete=models.PROTECT,
                                    verbose_name=pgettext_lazy('DeviceModel',
                                                               'device type'))
    brand = models.ForeignKey('Brand',
                              on_delete=models.PROTECT,
                              verbose_name=pgettext_lazy('DeviceModel',
                                                         'brand'))
    name = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('DeviceModel',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('DeviceModel',
                                                              'description'))
    snmp_configuration = models.ForeignKey('SNMPConfiguration',
                                           blank=True,
                                           null=True,
                                           default=None,
                                           on_delete=models.PROTECT,
                                           verbose_name=pgettext_lazy(
                                               'DeviceModel',
                                               'SNMP configuration'))

    class Meta:
        # Define the database table
        db_table = 'netscanner_device_model'
        ordering = ['brand', 'name']
        unique_together = ('brand', 'name')
        verbose_name = pgettext_lazy('DeviceModel', 'Device model')
        verbose_name_plural = pgettext_lazy('DeviceModel', 'Device models')

    def __str__(self):
        return '{BRAND} {NAME}'.format(BRAND=self.brand,
                                       NAME=self.name)


class DeviceModelAdmin(BaseModelAdmin):
    actions = ('action_change_snmp_configuration', )

    def action_change_snmp_configuration(self, request, queryset):
        form = ChangeSNMPConfigurationForm(request.POST)
        if 'action_change_snmp_configuration' in request.POST:
            if form.is_valid():
                # Change SNMP configuration for every selected row
                snmp_configuration = form.cleaned_data['snmp_configuration']
                queryset.update(snmp_configuration=snmp_configuration)
                # Operation successful
                self.message_user(request,
                                  pgettext_lazy(
                                      'Host',
                                      'Changed {COUNT} hosts'.format(
                                          COUNT=queryset.count())))
                return HttpResponseRedirect(request.get_full_path())
        # Render form to confirm changes
        return render(request,
                      'utility/change_attribute/form.html',
                      context={'queryset': queryset,
                               'form': form,
                               'title': pgettext_lazy(
                                   'Host',
                                   'Change SNMP configuration'),
                               'question': pgettext_lazy(
                                   'Host',
                                   'Confirm you want to change the '
                                   'SNMP configuration for the selected '
                                   'hosts?'),
                               'items_name': 'SNMP Configuration',
                               'action': 'action_change_snmp_configuration',
                               'action_description': pgettext_lazy(
                                   'Host',
                                   'Change SNMP configuration'),
                               })
    action_change_snmp_configuration.short_description = pgettext_lazy(
        'Host',
        'Change SNMP configuration')
