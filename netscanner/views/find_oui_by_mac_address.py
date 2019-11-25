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

from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView

from netscanner.forms.find_oui_by_mac_address import FindOUIByMACAddressForm

from oui.models import Oui


class FindOUIByMACAddressView(TemplateView, FormMixin):
    template_name = 'netscanner/site/find_oui_by_mac_address.html'
    form_class = FindOUIByMACAddressForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oui_list = []
        if self.request.POST and self.form.is_valid():
            form_data = self.form.cleaned_data
            mac_address = form_data['mac_address']
            if mac_address:
                # Show only the matching OUIs
                oui_list = Oui.objects.filter(prefix__startswith=mac_address)
        context['page_title'] = 'Find OUI by MAC Address'
        context['oui_list'] = oui_list
        return context

    def post(self, request, *args, **kwargs):
        # From ProcessFormMixin
        self.form = self.get_form(self.get_form_class())
        context = self.get_context_data(form=self.form)
        return self.render_to_response(context)
