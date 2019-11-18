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

from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render

from netscanner.forms.confirm_action import ConfirmActionForm

from ..models import BaseModelAdmin


class EnableDisableRecords(object):
    def __init__(self,
                 request: HttpRequest = None,
                 queryset: QuerySet = None,
                 model_admin: BaseModelAdmin = None,
                 action_name: str = None,
                 enabled_count_message: str = None,
                 item_name: str = None,
                 title: str = None,
                 description: str = None,
                 question: str = None):
        self.request = request
        self.queryset = queryset
        self.model_admin = model_admin
        self.action_name = action_name
        self.enabled_count_message = enabled_count_message
        self.item_name = item_name
        self.title = title
        self.description = description
        self.question = question

    def _enable_disable_records(self,
                                status: bool) -> HttpResponse:
        """
        Enable or disable the records in the queryset
        :param status: True to enable the records, else False
        :return: Response object with the form or the results
        """
        form = ConfirmActionForm(self.request.POST)
        if self.action_name in self.request.POST:
            if form.is_valid():
                # Enable every selected row
                self.queryset.update(enabled=status)
                # Operation successful
                self.model_admin.message_user(
                    self.request,
                    self.enabled_count_message.format(
                        COUNT=self.queryset.count()))
                return HttpResponseRedirect(self.request.get_full_path())
        # Render form to confirm changes
        return render(self.request,
                      'utility/change_attribute/form.html',
                      context={'queryset': self.queryset,
                               'form': form,
                               'title': self.title,
                               'question': self.question,
                               'items_name': self.item_name,
                               'action': self.action_name,
                               'action_description': self.description
                               })

    def enable(self) -> HttpResponse:
        """
        Enable all the selected records
        :return: Response object with the form or the results
        """
        return self._enable_disable_records(status=True)

    def disable(self) -> HttpResponse:
        """
        Disable all the selected records
        :return: Response object with the form or the results
        """
        return self._enable_disable_records(status=False)
