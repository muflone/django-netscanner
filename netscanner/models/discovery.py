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

from django.contrib import messages
from django.db import models, IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.translation import pgettext_lazy

from ..forms.change_subnetv4 import change_field_discovery_subnetv4_action
from ..forms.change_scanner import change_field_scanner_action
from ..forms.create_discovery import CreateDiscoveryForm

from utility.misc import ChangeFieldAction, EnableDisableRecords
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
    actions = ('action_enable',
               'action_disable',
               'action_change_scanner',
               'action_change_subnetv4')
    change_list_template = 'netscanner/discovery_create/change_list.html'

    def get_urls(self):
        """
        Additional URLs for the DiscoveryAdmin model
        """
        urls = [
            path('create/', self.create),
        ] + super().get_urls()
        return urls

    def action_enable(self, request, queryset):
        enable_disable = EnableDisableRecords(
            request=request,
            queryset=queryset,
            model_admin=self,
            action_name='action_enable',
            enabled_count_message=pgettext_lazy('Discovery',
                                                'Enabled {COUNT} discoveries'),
            item_name='Discovery',
            title=pgettext_lazy('Discovery', 'Enable discoveries'),
            description=pgettext_lazy('Discovery', 'Enable'),
            question=pgettext_lazy('Discovery',
                                   'Confirm you want to enable the selected '
                                   'discoveries?'))
        return enable_disable.enable()
    action_enable.short_description = pgettext_lazy('Discovery',
                                                    'Enable')

    def action_disable(self, request, queryset):
        enable_disable = EnableDisableRecords(
            request=request,
            queryset=queryset,
            model_admin=self,
            action_name='action_disable',
            enabled_count_message=pgettext_lazy(
                'Discovery',
                'Disabled {COUNT} discoveries'),
            item_name='Discovery',
            title=pgettext_lazy('Discovery', 'Disable discoveries'),
            description=pgettext_lazy('Discovery', 'Disable'),
            question=pgettext_lazy('Discovery',
                                   'Confirm you want to disable the selected '
                                   'discoveries?'))
        return enable_disable.disable()
    action_disable.short_description = pgettext_lazy('Discovery',
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
                                      'Discovery',
                                      'Changed {COUNT} discoveries'.format(
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

    def action_change_scanner(self, request, queryset):
        """
        Change Scanner
        """
        return self.do_action_change(
            request,
            queryset,
            action=change_field_scanner_action,
            action_name='change_scanner')
    action_change_scanner.short_description = (
        change_field_scanner_action.title)

    def action_change_subnetv4(self, request, queryset):
        """
        Change Subnet v4
        """
        return self.do_action_change(
            request,
            queryset,
            action=change_field_discovery_subnetv4_action,
            action_name='change_subnetv4')
    action_change_subnetv4.short_description = (
        change_field_discovery_subnetv4_action.title)

    def create(self, request):
        """
        Discoveries mass creation for each SubnetV4
        """
        if request.method == 'POST':
            form = CreateDiscoveryForm(request.POST)
            if form.is_valid():
                # Process the request by creating many Discovery objects
                counter = 0
                scanner = form.cleaned_data['scanner']
                # Create a new Discovery object for each selected subnet
                for subnet in form.cleaned_data['subnetv4']:
                    # Define name between two styles
                    naming_style = form.cleaned_data['naming_style']
                    name = ('{SUBNET} - {SCANNER}'
                            if naming_style == 'subnet_scanner'
                            else '{SCANNER} - {SUBNET}').format(
                        SUBNET=subnet.name,
                        SCANNER=scanner.name)
                    try:
                        # Create a new Discovery
                        Discovery.objects.create(
                            name=name,
                            description=form.cleaned_data['description'],
                            subnetv4_id=subnet.pk,
                            enabled=form.cleaned_data['enabled'],
                            scanner_id=scanner.pk,
                            timeout=form.cleaned_data['timeout'],
                            workers=form.cleaned_data['workers'],
                            options=form.cleaned_data['options'],
                            interval=form.cleaned_data['interval'])
                        counter += 1
                    except IntegrityError:
                        # Discovery already exists
                        self.message_user(
                            request=request,
                            message=pgettext_lazy(
                                'Discovery',
                                'The discovery {NAME} already exists'.format(
                                    NAME=name)),
                            level=messages.ERROR)
                # Operation completed
                if counter > 0:
                    # Discoveries created successfully
                    message = pgettext_lazy('Discovery',
                                            '{COUNT} discoveries were '
                                            'created'.format(COUNT=counter))
                    message_level = messages.INFO
                else:
                    # No discoveries created
                    message = pgettext_lazy('Discovery',
                                            'No discoveries were created')
                    message_level = messages.WARNING
                # Show results to the user
                self.message_user(request=request,
                                  message=message,
                                  level=message_level)
                # Return to the calling page
                return redirect('..')
        # Show the requesting form
        return render(request,
                      'netscanner/discovery_create/form.html',
                      {'form': CreateDiscoveryForm(),
                       'action': 'create',
                       'action_description': 'Create new discoveries',
                       })
