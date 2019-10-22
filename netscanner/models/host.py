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

from ..forms.confirm_action import ConfirmActionForm
from ..forms.change_company import ChangeCompanyForm
from ..forms.change_device_model import ChangeDeviceModelForm
from ..forms.change_domain import ChangeDomainForm
from ..forms.change_location import ChangeLocationForm
from ..forms.change_snmp_configuration import ChangeSNMPConfigurationForm
from ..forms.change_subnetv4 import ChangeSubnetV4Form

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

    def action_change_company(self, request, queryset):
        form = ChangeCompanyForm(request.POST)
        if 'action_change_company' in request.POST:
            if form.is_valid():
                # Change Company for every selected row
                company = form.cleaned_data['company']
                queryset.update(company=company)
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
                                   'Change Company'),
                               'question': pgettext_lazy(
                                   'Host',
                                   'Confirm you want to change the '
                                   'company for the selected hosts?'),
                               'items_name': 'Company',
                               'action': 'action_change_company',
                               'action_description': pgettext_lazy(
                                   'Host',
                                   'Change Company'),
                               })
    action_change_company.short_description = pgettext_lazy(
        'Host',
        'Change Company')

    def action_change_device_model(self, request, queryset):
        form = ChangeDeviceModelForm(request.POST)
        if 'action_change_device_model' in request.POST:
            if form.is_valid():
                # Change Device model for every selected row
                device_model = form.cleaned_data['device_model']
                queryset.update(device_model=device_model)
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
                                   'Change Device model'),
                               'question': pgettext_lazy(
                                   'Host',
                                   'Confirm you want to change the '
                                   'device model for the selected hosts?'),
                               'items_name': 'Device model',
                               'action': 'action_change_device_model',
                               'action_description': pgettext_lazy(
                                   'Host',
                                   'Change Device model'),
                               })
    action_change_device_model.short_description = pgettext_lazy(
        'Host',
        'Change Device model')

    def action_change_domain(self, request, queryset):
        form = ChangeDomainForm(request.POST)
        if 'action_change_domain' in request.POST:
            if form.is_valid():
                # Change Domain for every selected row
                domain = form.cleaned_data['domain']
                queryset.update(domain=domain)
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
                                   'Change Domain'),
                               'question': pgettext_lazy(
                                   'Host',
                                   'Confirm you want to change the '
                                   'domain for the selected hosts?'),
                               'items_name': 'Domain',
                               'action': 'action_change_domain',
                               'action_description': pgettext_lazy(
                                   'Host',
                                   'Change Domain'),
                               })
    action_change_domain.short_description = pgettext_lazy(
        'Host',
        'Change Domain')

    def action_change_location(self, request, queryset):
        form = ChangeLocationForm(request.POST)
        if 'action_change_location' in request.POST:
            if form.is_valid():
                # Change Location for every selected row
                location = form.cleaned_data['location']
                queryset.update(location=location)
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
                                   'Change Location'),
                               'question': pgettext_lazy(
                                   'Host',
                                   'Confirm you want to change the '
                                   'location for the selected hosts?'),
                               'items_name': 'Location',
                               'action': 'action_change_location',
                               'action_description': pgettext_lazy(
                                   'Host',
                                   'Change Location'),
                               })
    action_change_location.short_description = pgettext_lazy('Host',
                                                             'Change Location')

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

    def action_change_subnetv4(self, request, queryset):
        form = ChangeSubnetV4Form(request.POST)
        if 'action_change_subnetv4' in request.POST:
            if form.is_valid():
                # Change SNMP configuration for every selected row
                subnetv4 = form.cleaned_data['subnetv4']
                queryset.update(subnetv4=subnetv4)
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
                                   'Change Subnet V4'),
                               'question': pgettext_lazy(
                                   'Host',
                                   'Confirm you want to change the '
                                   'Subnet V4 for the selected hosts?'),
                               'items_name': 'SNMP Configuration',
                               'action': 'action_change_subnetv4',
                               'action_description': pgettext_lazy(
                                   'Host',
                                   'Change Subnet V4'),
                               })
    action_change_subnetv4.short_description = pgettext_lazy(
        'Host',
        'Change Subnet V4')
