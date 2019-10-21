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

from ..forms import ConfirmActionForm

from utility.models import BaseModel, BaseModelAdmin


class Discovery(BaseModel):
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name=pgettext_lazy('Discovery',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('Discovery',
                                                              'description'))
    subnetv4 = models.ForeignKey('SubnetV4',
                                 on_delete=models.PROTECT,
                                 verbose_name=pgettext_lazy('Discovery',
                                                            'subnet v4'))
    enabled = models.BooleanField(default=True,
                                  verbose_name=pgettext_lazy('Discovery',
                                                             'enabled'))
    scanner = models.ForeignKey('Scanner',
                                on_delete=models.PROTECT,
                                verbose_name=pgettext_lazy('Discover',
                                                           'scanner'))
    timeout = models.PositiveIntegerField(default=0,
                                          verbose_name=pgettext_lazy(
                                              'Discover',
                                              'timeout'))
    workers = models.PositiveSmallIntegerField(default=1,
                                               verbose_name=pgettext_lazy(
                                                   'Discover',
                                                   'workers'))
    options = models.TextField(blank=True,
                               verbose_name=pgettext_lazy('Discover',
                                                          'options'))
    interval = models.PositiveIntegerField(default=60,
                                           verbose_name=pgettext_lazy(
                                               'Discovery',
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
    actions = ('action_enable', 'action_disable')

    def action_enable(self, request, queryset):
        form = ConfirmActionForm(request.POST)
        if 'action_enable' in request.POST:
            if form.is_valid():
                # Enable every selected row
                queryset.update(enabled=True)
                # Operation successful
                self.message_user(request,
                                  pgettext_lazy(
                                      'Discovery',
                                      'Enabled {COUNT} discoveries'.format(
                                          COUNT=queryset.count())))
                return HttpResponseRedirect(request.get_full_path())
        # Render form to confirm changes
        return render(request,
                      'utility/change_attribute/form.html',
                      context={'queryset': queryset,
                               'form': form,
                               'title': pgettext_lazy(
                                   'Discovery',
                                   'Enable discoveries'),
                               'question': pgettext_lazy(
                                   'Discovery',
                                   'Confirm you want to enable the selected '
                                   'discoveries?'),
                               'items_name': 'Discovery',
                               'action': 'action_enable',
                               'action_description': pgettext_lazy(
                                   'Discovery',
                                   'Enable'),
                               })
    action_enable.short_description = pgettext_lazy('Discovery',
                                                    'Enable')

    def action_disable(self, request, queryset):
        form = ConfirmActionForm(request.POST)
        if 'action_disable' in request.POST:
            if form.is_valid():
                # Disable every selected row
                queryset.update(enabled=False)
                # Operation successful
                self.message_user(request,
                                  pgettext_lazy(
                                      'Discovery',
                                      'Disabled {COUNT} discoveries'.format(
                                          COUNT=queryset.count())))
                return HttpResponseRedirect(request.get_full_path())
        # Render form to confirm changes
        return render(request,
                      'utility/change_attribute/form.html',
                      context={'queryset': queryset,
                               'form': form,
                               'title': pgettext_lazy(
                                   'Discovery',
                                   'Disable discoveries'),
                               'question': pgettext_lazy(
                                   'Discovery',
                                   'Confirm you want to disable the selected '
                                   'discoveries?'),
                               'items_name': 'Discovery',
                               'action': 'action_disable',
                               'action_description': pgettext_lazy(
                                   'Discovery',
                                   'Disable'),
                               })
    action_disable.short_description = pgettext_lazy('Discovery',
                                                     'Disable')
