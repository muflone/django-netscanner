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


class ChangeFieldAction(object):
    def __init__(self,
                 item: str,
                 field_name: str,
                 title: str,
                 question: str,
                 form: forms.Form):
        """
        ChangeFieldAction to map a change field Action

        :param item: Object (model) name to change
        :param field_name: Field name to change
        :param title: Title of the requesting page
        :param question: Question to confirm the change
        :param form: Form object containing the information
        """
        self.item = item
        self.field_name = field_name
        self.title = title
        self.question = question
        self.form = form
