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
from django.views.generic import TemplateView

from netscanner.models import SubnetV4, Host


class HostsMapView(TemplateView):
    template_name = 'netscanner/site/hosts_map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Hosts map'
        subnet = SubnetV4.objects.get(name='Giammoro')
        hosts_dict = dict((address, None)
                          for address in subnet.get_ip_list())
        hosts_dict.update(dict((host.address, host)
                               for host
                               in Host.objects.filter(subnetv4_id=subnet.pk)))
        context['subnet'] = subnet
        context['hosts'] = hosts_dict
        return context
