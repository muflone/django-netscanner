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
from django.views.generic.list import ListView

from netscanner.forms.hosts_map import HostsMapForm
from netscanner.models import SubnetV4, Host


class HostsMapView(ListView, FormMixin):
    template_name = 'netscanner/site/hosts_map.html'
    form_class = HostsMapForm
    model = SubnetV4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hosts_dict = {}
        if self.request.POST and self.form.is_valid():
            form_data = self.form.cleaned_data
            subnet = form_data['subnet']
            if subnet:
                # Show only the hosts for the selected subnet
                hosts_dict = dict((address, [])
                                  for address in subnet.get_ip_list())
                # Add valid hosts
                for host in Host.objects.filter(
                        subnetv4_id=subnet.pk).order_by('address_numeric'):
                    # Add addresses not in the subnet range
                    if host.address not in hosts_dict:
                        hosts_dict[host.address] = []
                    hosts_dict[host.address].append(host)
                if form_data.get('show_missing', 0):
                    # Show also missing hosts (add placeholder None)
                    [hosts_dict[address].append(None)
                        for address in subnet.get_ip_list()
                        if not hosts_dict[address]]
        context['page_title'] = 'Hosts map'
        context['hosts'] = hosts_dict
        return context

    def post(self, request, *args, **kwargs):
        # From ProcessFormMixin
        self.form = self.get_form(self.get_form_class())
        # From BaseListView
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list,
                                        form=self.form)
        return self.render_to_response(context)
