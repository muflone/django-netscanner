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
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import pgettext_lazy

from ..forms.confirm_action import ConfirmActionForm
from ..forms.change_company import change_field_company_action
from ..forms.change_device_model import change_field_device_model_action
from ..forms.change_domain import change_field_domain_action
from ..forms.change_location import change_field_location_action
from ..forms.change_operating_system import change_field_os_action
from ..forms.change_snmp_configuration import change_field_snmp_config_action
from ..forms.change_subnetv4 import change_field_host_subnetv4_action

from utility.misc import ChangeFieldAction
from utility.models import BaseModel, BaseModelAdmin


class Host(BaseModel):
    location = models.ForeignKey('Location',
                                 blank=True,
                                 null=True,
                                 default=None,
                                 on_delete=models.PROTECT,
                                 verbose_name=pgettext_lazy('Host',
                                                            'location'))
    area = models.CharField(max_length=255,
                            blank=True,
                            verbose_name=pgettext_lazy('Host',
                                                       'area'))
    position = models.CharField(max_length=255,
                                blank=True,
                                verbose_name=pgettext_lazy('Host',
                                                           'position'))
    name = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('Host',
                                                       'name'))
    address = models.CharField(max_length=255,
                               verbose_name=pgettext_lazy('Host',
                                                          'address'))
    mac_address = models.CharField(max_length=12,
                                   blank=True,
                                   verbose_name=pgettext_lazy('Host',
                                                              'MAC address'))
    subnetv4 = models.ForeignKey('SubnetV4',
                                 blank=True,
                                 null=True,
                                 default=None,
                                 on_delete=models.PROTECT,
                                 verbose_name=pgettext_lazy('Host',
                                                            'subnet v4'))
    hostname = models.CharField(max_length=255,
                                blank=True,
                                verbose_name=pgettext_lazy('Host',
                                                           'hostname'))
    domain = models.ForeignKey('Domain',
                               blank=True,
                               null=True,
                               default=None,
                               on_delete=models.PROTECT,
                               verbose_name=pgettext_lazy('Host',
                                                          'network domain'))
    device_model = models.ForeignKey('DeviceModel',
                                     blank=True,
                                     null=True,
                                     default=None,
                                     on_delete=models.PROTECT,
                                     verbose_name=pgettext_lazy('Host',
                                                                'device model')
                                     )
    serial = models.CharField(max_length=255,
                              blank=True,
                              verbose_name=pgettext_lazy('Host',
                                                         'serial number'))
    enabled = models.BooleanField(default=True,
                                  verbose_name=pgettext_lazy('Host',
                                                             'enabled'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('Host',
                                                              'description'))
    company = models.ForeignKey('Company',
                                blank=True,
                                null=True,
                                default=None,
                                on_delete=models.PROTECT,
                                verbose_name=pgettext_lazy('Host',
                                                           'company'))
    os = models.ForeignKey('OperatingSystem',
                           blank=True,
                           null=True,
                           default=None,
                           on_delete=models.PROTECT,
                           verbose_name=pgettext_lazy('Host',
                                                      'operating system'))
    no_discovery = models.BooleanField(default=False,
                                       verbose_name=pgettext_lazy(
                                           'Host',
                                           'do not update on discoveries'))
    last_seen = models.DateTimeField(blank=True,
                                     null=True,
                                     default=None,
                                     verbose_name=pgettext_lazy('Host',
                                                                'last seen'))
    verified = models.BooleanField(default=False,
                                   verbose_name=pgettext_lazy('Host',
                                                              'verified'))
    verification = models.DateField(blank=True,
                                    null=True,
                                    default=None,
                                    verbose_name=pgettext_lazy('Host',
                                                               'verification'))
    snmp_version = models.CharField(max_length=5,
                                    blank=True,
                                    choices=(('off', pgettext_lazy('Host',
                                                                   'Off')),
                                             ('v1', '1'),
                                             ('v2c', '2C')),
                                    verbose_name=pgettext_lazy('Host',
                                                               'SNMP version'))
    snmp_community = models.CharField(max_length=255,
                                      blank=True,
                                      verbose_name=pgettext_lazy(
                                          'Host',
                                          'SNMP community string'))
    snmp_configuration = models.ForeignKey('SNMPConfiguration',
                                           blank=True,
                                           null=True,
                                           default=None,
                                           on_delete=models.PROTECT,
                                           verbose_name=pgettext_lazy(
                                               'Host',
                                               'SNMP configuration'))
    custom_fields = models.ManyToManyField('CustomField',
                                           db_table='netscanner_host_custom',
                                           blank=True,
                                           verbose_name=pgettext_lazy(
                                               'Host',
                                               'custom fields'))

    class Meta:
        # Define the database table
        db_table = 'netscanner_hosts'
        ordering = ['location', 'name', 'address']
        unique_together = (('location', 'name', 'address'))
        verbose_name = pgettext_lazy('Host', 'Host')
        verbose_name_plural = pgettext_lazy('Host', 'Hosts')

    def __str__(self):
        return '{NAME} {ADDRESS}'.format(NAME=self.name,
                                         ADDRESS=self.address)


class HostAdmin(BaseModelAdmin):
    actions = ('action_enable',
               'action_disable',
               'action_change_company',
               'action_change_device_model',
               'action_change_domain',
               'action_change_location',
               'action_change_operating_system',
               'action_change_snmp_configuration',
               'action_change_subnetv4')

    def action_enable(self, request, queryset):
        form = ConfirmActionForm(request.POST)
        if 'action_enable' in request.POST:
            if form.is_valid():
                # Enable every selected row
                queryset.update(enabled=True)
                # Operation successful
                self.message_user(request,
                                  pgettext_lazy(
                                      'Host',
                                      'Enabled {COUNT} hosts'.format(
                                          COUNT=queryset.count())))
                return HttpResponseRedirect(request.get_full_path())
        # Render form to confirm changes
        return render(request,
                      'utility/change_attribute/form.html',
                      context={'queryset': queryset,
                               'form': form,
                               'title': pgettext_lazy(
                                   'Host',
                                   'Enable hosts'),
                               'question': pgettext_lazy(
                                   'Host',
                                   'Confirm you want to enable the selected '
                                   'hosts?'),
                               'items_name': 'Host',
                               'action': 'action_enable',
                               'action_description': pgettext_lazy(
                                   'Host',
                                   'Enable'),
                               })
    action_enable.short_description = pgettext_lazy('Host',
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
                                      'Host',
                                      'Disabled {COUNT} hosts'.format(
                                          COUNT=queryset.count())))
                return HttpResponseRedirect(request.get_full_path())
        # Render form to confirm changes
        return render(request,
                      'utility/change_attribute/form.html',
                      context={'queryset': queryset,
                               'form': form,
                               'title': pgettext_lazy(
                                   'Host',
                                   'Disable hosts'),
                               'question': pgettext_lazy(
                                   'Host',
                                   'Confirm you want to disable the selected '
                                   'hosts?'),
                               'items_name': 'Host',
                               'action': 'action_disable',
                               'action_description': pgettext_lazy(
                                   'Host',
                                   'Disable'),
                               })
    action_disable.short_description = pgettext_lazy('Host',
                                                     'Disable')

    def do_action_change(self, request, queryset,
                         action: ChangeFieldAction,
                         action_name: str) -> HttpResponse:
        """
        Execute a change action on a group of selected records
        :param request: Request object from the page
        :param queryset: queryset with the data to edit
        :param action: ChangeFieldAction object containing the messages
        :param action_name: called action name
        :return: HttpResponse or HttpResponseRedirect object
        """
        form = action.form(request.POST)
        if 'action_%s' % action_name in request.POST:
            if form.is_valid():
                # Change Field for every selected row
                fields = {action.field_name: form.cleaned_data['changed_data']}
                queryset.update(**fields)
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
                               'title': action.title,
                               'question': action.question,
                               'items_name': action.item,
                               'action': 'action_%s' % action_name,
                               'action_description': action.title,
                               })

    def action_change_company(self, request, queryset):
        """
        Change Company
        """
        return self.do_action_change(request, queryset,
                                     action=change_field_company_action,
                                     action_name='change_company')
    action_change_company.short_description = (
        change_field_company_action.title)

    def action_change_device_model(self, request, queryset):
        """
        Change Device model
        """
        return self.do_action_change(request, queryset,
                                     action=change_field_device_model_action,
                                     action_name='change_device_model')
    action_change_device_model.short_description = (
        change_field_device_model_action.title)

    def action_change_domain(self, request, queryset):
        """
        Change Domain
        """
        return self.do_action_change(request, queryset,
                                     action=change_field_domain_action,
                                     action_name='change_domain')
    action_change_domain.short_description = (
        change_field_domain_action.title)

    def action_change_location(self, request, queryset):
        """
        Change Location
        """
        return self.do_action_change(request, queryset,
                                     action=change_field_location_action,
                                     action_name='change_location')
    action_change_location.short_description = (
        change_field_location_action.title)

    def action_change_operating_system(self, request, queryset):
        """
        Change Operating System
        """
        return self.do_action_change(request, queryset,
                                     action=change_field_os_action,
                                     action_name='change_operating_system')
    action_change_operating_system.short_description = (
        change_field_os_action.title)

    def action_change_snmp_configuration(self, request, queryset):
        """
        Change SNMP Configuration
        """
        return self.do_action_change(request, queryset,
                                     action=change_field_snmp_config_action,
                                     action_name='change_snmp_configuration')
    action_change_snmp_configuration.short_description = (
        change_field_snmp_config_action.title)

    def action_change_subnetv4(self, request, queryset):
        """
        Change Subnet v4
        """
        return self.do_action_change(request, queryset,
                                     action=change_field_host_subnetv4_action,
                                     action_name='change_subnetv4')
    action_change_subnetv4.short_description = (
        change_field_host_subnetv4_action.title)
