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

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from netscanner.models import SubnetV4, Host


class HostsMapView(TemplateView):
    template_name = 'netscanner/site/hosts_map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Hosts map'
        subnets = SubnetV4.objects.all()
        if 'subnet' in kwargs:
            # Show only the hosts for the selected subnet
            subnet = get_object_or_404(subnets, pk=kwargs['subnet'])
            hosts_dict = dict((address, [])
                              for address in subnet.get_ip_list())
            # Add valid hosts
            for host in Host.objects.filter(
                    subnetv4_id=subnet.pk).order_by('address_numeric'):
                # Add addresses not in the subnet range
                if host.address not in hosts_dict:
                    hosts_dict[host.address] = []
                hosts_dict[host.address].append(host)
            if kwargs.get('show_missing', 0):
                # Show also missing hosts (add placeholder None)
                [hosts_dict[address].append(None)
                 for address in subnet.get_ip_list()
                 if not hosts_dict[address]]
        else:
            # No data for missing subnet
            subnet = None
            hosts_dict = {}
        context['subnets'] = subnets
        context['subnet'] = subnet
        context['hosts'] = hosts_dict
        context['show_missing'] = kwargs.get('show_missing', 0)
        return context
