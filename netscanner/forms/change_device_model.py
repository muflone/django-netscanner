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

from ..models.device_model import DeviceModel

from utility.misc import ChangeFieldAction


class ChangeDeviceModelForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    changed_data = forms.ModelChoiceField(
        queryset=DeviceModel.objects,
        required=False,
        label=pgettext_lazy('Host',
                            'Device model'))


change_field_device_model_action = ChangeFieldAction(
    item='Device Model',
    field_name='device_model',
    title=pgettext_lazy('Host', 'Change Device model'),
    question=pgettext_lazy('Host',
                           'Confirm you want to change the '
                           'device model for the selected hosts?'),
    form=ChangeDeviceModelForm)
