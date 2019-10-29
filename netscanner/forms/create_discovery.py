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

from django import forms
from django.utils.translation import pgettext_lazy

from ..models.scanner import Scanner
from ..models.subnet_v4 import SubnetV4


class CreateDiscoveryForm(forms.Form):
    """
    Form for the Discoveries mass creation
    """
    naming_style = forms.ChoiceField(choices=(
        ('subnet_scanner', pgettext_lazy('Discovery', 'Subnet - Scanner')),
        ('scanner_subnet', pgettext_lazy('Discovery', 'Scanner - Subnet'))))
    scanner = forms.ModelChoiceField(required=True,
                                     queryset=Scanner.objects.all())
    subnetv4 = forms.ModelMultipleChoiceField(required=True,
                                              queryset=SubnetV4.objects.all())
    enabled = forms.BooleanField(required=False,
                                 initial=True)
    timeout = forms.IntegerField(required=True,
                                 min_value=0,
                                 initial=5)
    workers = forms.IntegerField(required=True,
                                 min_value=1,
                                 initial=10)
    description = forms.CharField(required=False,
                                  widget=forms.Textarea)
    options = forms.CharField(required=False,
                              widget=forms.Textarea)
    interval = forms.IntegerField(required=True,
                                  min_value=1,
                                  initial=60)
