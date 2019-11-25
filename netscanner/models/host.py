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

import socket
import struct

from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe, SafeText
from django.utils.translation import pgettext_lazy

from utility.misc.admin_text_input_filter import AdminTextInputFilter

from .host_custom_field import HostCustomFieldInlineAdmin

from ..forms.change_company import change_field_company_action
from ..forms.change_device_model import change_field_device_model_action
from ..forms.change_domain import change_field_domain_action
from ..forms.change_location import change_field_location_action
from ..forms.change_operating_system import change_field_os_action
from ..forms.change_snmp_configuration import change_field_snmp_config_action
from ..forms.change_snmp_version import change_field_snmp_version_action
from ..forms.change_subnetv4 import change_field_host_subnetv4_action

from utility.misc import ChangeFieldAction, EnableDisableRecords
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
    address_numeric = models.IntegerField(default=0,
                                          verbose_name=pgettext_lazy(
                                              'Host',
                                              'address in numeric form'),
                                          editable=False)
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
    snmp_version = models.ForeignKey('SNMPVersion',
                                     blank=True,
                                     null=True,
                                     default=None,
                                     on_delete=models.PROTECT,
                                     verbose_name=pgettext_lazy(
                                         'Host',
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

    class Meta:
        # Define the database table
        db_table = 'netscanner_hosts'
        ordering = ['location', 'address_numeric']
        unique_together = (('location', 'name', 'address'))
        verbose_name = pgettext_lazy('Host', 'Host')
        verbose_name_plural = pgettext_lazy('Host', 'Hosts')

    def __str__(self):
        return '{NAME} {ADDRESS}'.format(NAME=self.name,
                                         ADDRESS=self.address)

    def save(self, *args, **kwargs):
        # Override address_numeric field during the save
        try:
            self.address_numeric = struct.unpack('!I',
                                                 socket.inet_aton(
                                                     self.address))[0]
        except OSError:
            # Skip invalid IP addresses
            pass
        # Fix MAC Address field
        self.mac_address = (self.mac_address.upper()
                            .replace(':', '')
                            .replace('-', '')
                            .replace(' ', ''))
        # Skip invalid MAC Address
        if all(c == '0' for c in self.mac_address):
            self.mac_address = ''
        super().save()

    def last_seen_date(self):
        """
        Get the last seen date
        """
        return self.last_seen.date() if self.last_seen else None
    last_seen_date.admin_order_field = 'last_seen__date'

    def last_seen_time(self):
        """
        Get the last seen time
        """
        return self.last_seen.time() if self.last_seen else None
    last_seen_time.admin_order_field = 'last_seen__time'

    def ip_address(self):
        """
        Get the address using the numeric ordering
        :return:
        """
        return self.address
    ip_address.admin_order_field = 'address_numeric'

    def brand(self) -> SafeText:
        """
        Brand for DeviceModel
        :param instance: Host object containing the brand
        :return: SafeText object with the HTML text
        """
        return self.device_model.brand if self.device_model else None
    brand.short_description = pgettext_lazy('Host',
                                            'Brand')

    def brand_thumbnail(self) -> SafeText:
        """
        Show Brand image
        :param instance: Host object containing the image
        :return: SafeText object with the HTML text
        """
        if self.device_model:
            if self.device_model.brand.image.name:
                # Brand with image
                url_image = self.device_model.brand.image.url
                return mark_safe('<img class="device_model_image"'
                                 ' src="{image}" '
                                 ' title="{title}" />'.format(
                                    image=url_image,
                                    title=self.device_model.brand))
            else:
                # Missing brand image
                return self.device_model.brand
    brand_thumbnail.short_description = pgettext_lazy('Host',
                                                      'Brand Image')
    brand_thumbnail.admin_order_field = 'device_model__brand'

    def os_thumbnail(self) -> SafeText:
        """
        Show OperatingSystem image
        :param instance: Host object containing the image
        :return: SafeText object with the HTML text
        """
        if self.os:
            if self.os.image.name:
                # Operating system with image
                url_image = self.os.image.url
                return mark_safe('<img class="os_image"'
                                 ' src="{image}" '
                                 ' title="{title}" />'.format(
                                    image=url_image,
                                    title=self.os))
            else:
                # Missing operating system image
                return self.os
    os_thumbnail.short_description = pgettext_lazy('Host',
                                                   'OperatingSystem Image')

    def device_model_thumbnail(self) -> SafeText:
        """
        Show image
        :param instance: Host object containing the image
        :return: SafeText object with the HTML text
        """
        if self.device_model and self.device_model.image.name:
            url_image = self.device_model.image.url
            return mark_safe('<a href="{image}" target="_blank">'
                             '<img class="device_model_image"'
                             ' src="{image}" />'
                             '</a>'.format(image=url_image))
    device_model_thumbnail.short_description = pgettext_lazy('Host',
                                                             'Model image')

    def teamviewer_id(self) -> str:
        """
        Get TeamViewer ID from custom fields
        :return: TeamViewer ID or empty string
        """
        custom_field = self.hostcustomfield_set.filter(
            field__name='TeamViewer ID').first()
        return custom_field.value if custom_field else None


class HostAdmin(BaseModelAdmin):
    class Media:
        # Add custom CSS for images
        css = {
            'all': ('admin/css/device_model.css',)
        }

    list_per_page = 300


class HostProxy(Host):
    class Meta:
        proxy = True
        verbose_name = pgettext_lazy('Host', 'Host (extended)')
        verbose_name_plural = pgettext_lazy('Host', 'Hosts (extended)')


class HostProxyAdmin(BaseModelAdmin):
    class Media:
        # Add custom CSS for images
        css = {
            'all': ('admin/css/device_model.css',)
        }

    actions = ('action_enable',
               'action_disable',
               'action_change_company',
               'action_change_device_model',
               'action_change_domain',
               'action_change_location',
               'action_change_operating_system',
               'action_change_snmp_version',
               'action_change_snmp_configuration',
               'action_change_subnetv4')
    inlines = [HostCustomFieldInlineAdmin]
    list_per_page = 300

    def action_enable(self, request, queryset):
        enable_disable = EnableDisableRecords(
            request=request,
            queryset=queryset,
            model_admin=self,
            action_name='action_enable',
            enabled_count_message=pgettext_lazy('Host',
                                                'Enabled {COUNT} hosts'),
            item_name='Host',
            title=pgettext_lazy('Host', 'Enable hosts'),
            description=pgettext_lazy('Host', 'Enable'),
            question=pgettext_lazy('Host',
                                   'Confirm you want to enable the selected '
                                   'hosts?'))
        return enable_disable.enable()
    action_enable.short_description = pgettext_lazy('Host',
                                                    'Enable')

    def action_disable(self, request, queryset):
        enable_disable = EnableDisableRecords(
            request=request,
            queryset=queryset,
            model_admin=self,
            action_name='action_disable',
            enabled_count_message=pgettext_lazy('Host',
                                                'Disabled {COUNT} hosts'),
            item_name='Host',
            title=pgettext_lazy('Host', 'Disable hosts'),
            description=pgettext_lazy('Host', 'Disable'),
            question=pgettext_lazy('Host',
                                   'Confirm you want to disable the selected '
                                   'hosts?'))
        return enable_disable.disable()
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

    def action_change_snmp_version(self, request, queryset):
        """
        Change SNMP Version
        """
        return self.do_action_change(request, queryset,
                                     action=change_field_snmp_version_action,
                                     action_name='change_snmp_version')
    action_change_snmp_version.short_description = (
        change_field_snmp_version_action.title)

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


class HostAdminNameInputFilter(AdminTextInputFilter):
    """
    Filter SNMPValues by name
    """
    parameter_name = 'name'
    title = pgettext_lazy('Host', 'Name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__icontains=self.value())


class HostAdminAddressInputFilter(AdminTextInputFilter):
    """
    Filter SNMPValues by address
    """
    parameter_name = 'address'
    title = pgettext_lazy('Host', 'Address')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(address__icontains=self.value())


class HostAdminMACAddressInputFilter(AdminTextInputFilter):
    """
    Filter SNMPValues by MAC address
    """
    parameter_name = 'mac_address'
    title = pgettext_lazy('Host', 'MAC Address')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(mac_address__icontains=self.value())
