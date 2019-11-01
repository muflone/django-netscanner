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

import json

from django.contrib import messages
from django.db import models, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import pgettext_lazy

from ..forms.confirm_action import ConfirmActionForm

from utility.models import BaseModel, BaseModelAdmin


class DiscoveryResult(BaseModel):
    discovery = models.ForeignKey('Discovery',
                                  on_delete=models.PROTECT,
                                  verbose_name=pgettext_lazy('DiscoveryResult',
                                                             'discovery'))
    address = models.CharField(max_length=255,
                               verbose_name=pgettext_lazy('DiscoveryResult',
                                                          'address'))
    options = models.TextField(blank=True,
                               verbose_name=pgettext_lazy('DiscoveryResult',
                                                          'options'))
    scan_datetime = models.DateTimeField(
        verbose_name=pgettext_lazy('Discovery',
                                   'scan date and time'))
    results = models.TextField(blank=True,
                               verbose_name=pgettext_lazy('DiscoveryResult',
                                                          'results'))

    class Meta:
        # Define the database table
        db_table = 'netscanner_discovery_result'
        ordering = ['-scan_datetime']
        verbose_name = pgettext_lazy('DiscoveryResult', 'Discovery result')
        verbose_name_plural = pgettext_lazy('DiscoveryResult',
                                            'Discovery results')

    def __str__(self):
        return '{ID}'.format(ID=self.id)

    def scan_date(self):
        """
        Get the scan date
        """
        return self.scan_datetime.date()
    scan_date.admin_order_field = 'scan_datetime__date'

    def scan_time(self):
        """
        Get the scan time
        """
        return self.scan_datetime.time()
    scan_time.admin_order_field = 'scan_datetime__time'

class DiscoveryResultAdmin(BaseModelAdmin):
    actions = ('action_apply_to_hosts', )

    def action_apply_to_hosts(self, request, queryset):
        from ..management.commands import discovery_tool_commands

        form = ConfirmActionForm(request.POST)
        if 'action_apply_to_hosts' in request.POST:
            if form.is_valid():
                # Prepare every available tool
                tools = {}
                for command in discovery_tool_commands:
                    tools[command.tool_name] = command()
                    # Disable the DiscoveryResults automatic generation
                    tools[command.tool_name].no_log_results = True
                # Process the results in a single operation on the DB side
                with transaction.atomic():
                    # Process each row in the results set
                    for result in queryset:
                        if result.discovery.scanner.tool in tools:
                            # Process each result using the tool
                            command = tools[result.discovery.scanner.tool]
                            command.process_results(
                                discovery=result.discovery,
                                options=None,
                                results=[(result.address,
                                         json.loads(result.results))])
                        else:
                            # Unknown tool
                            self.message_user(
                                request=request,
                                message=pgettext_lazy(
                                    'DiscoveryResultAdmin',
                                    'Unrecognized Scanner tool'),
                                level=messages.ERROR)
                            break
                    else:
                        # Operation successful
                        self.message_user(
                            request,
                            pgettext_lazy(
                                'DiscoveryResult',
                                'Applied results to {COUNT} hosts'.format(
                                    COUNT=queryset.count())))
                return HttpResponseRedirect(request.get_full_path())
        # Render form to confirm changes
        return render(request,
                      'utility/change_attribute/form.html',
                      context={'queryset': queryset,
                               'form': form,
                               'title': pgettext_lazy(
                                   'DiscoveryResult',
                                   'Apply the results to the hosts'),
                               'question': pgettext_lazy(
                                   'DiscoveryResult',
                                   'Confirm you want to apply the results '
                                   'to the hosts?'),
                               'items_name': 'DiscoveryResult',
                               'action': 'action_apply_to_hosts',
                               'action_description': pgettext_lazy(
                                   'DiscoveryResult',
                                   'Apply to hosts'),
                               })
    action_apply_to_hosts.short_description = pgettext_lazy('DiscoveryResult',
                                                            'Apply to hosts')
