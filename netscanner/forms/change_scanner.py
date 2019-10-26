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

from utility.misc import ChangeFieldAction


class ChangeScannerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    changed_data = forms.ModelChoiceField(
        queryset=Scanner.objects,
        required=False,
        label=pgettext_lazy('Discovery',
                            'Scanner'))


change_field_scanner_action = ChangeFieldAction(
    item='Scanner',
    field_name='scanner',
    title=pgettext_lazy('Discovery', 'Change Scanner'),
    question=pgettext_lazy('Discovery',
                           'Confirm you want to change the '
                           'scanner for the selected discoveries?'),
    form=ChangeScannerForm)
