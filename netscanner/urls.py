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

from django.urls import path

from netscanner.views.find_oui_by_mac_address import FindOUIByMACAddressView
from netscanner.views.find_oui_by_organization import FindOUIByOrganizationView
from netscanner.views.hosts_map import HostsMapView


urlpatterns = [path(route='hosts_map/',
                    view=HostsMapView.as_view(),
                    name='hosts_map'),
               path(route='find_oui_by_mac/',
                    view=FindOUIByMACAddressView.as_view(),
                    name='find_oui_by_mac'),
               path(route='find_oui_by_organization/',
                    view=FindOUIByOrganizationView.as_view(),
                    name='find_oui_by_organization')
               ]
