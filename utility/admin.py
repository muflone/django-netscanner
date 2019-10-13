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

from django.contrib import admin
from django.db.utils import OperationalError

from .models import (AdminListDisplay, AdminListDisplayAdmin,
                     AdminListDisplayLink, AdminListDisplayLinkAdmin)

from utility.misc import get_admin_models, get_class_from_module


admin.site.register(AdminListDisplay, AdminListDisplayAdmin)
admin.site.register(AdminListDisplayLink, AdminListDisplayLinkAdmin)

admin_models = get_admin_models()

# Customize list_display
try:
    # Clear or initialize the model list_display
    for model_name in admin_models:
        admin_models[model_name].list_display = []
    # Add the fields to model list_display
    for item in AdminListDisplay.objects.filter(enabled=True).order_by(
            'model', 'order'):
        # Include only existing models
        if item.model in admin_models:
            admin_models[item.model].list_display.append(item.field)
except OperationalError:
    # If the model AdminListDisplay doesn't yet exist skip the customization
    pass

# Customize list_display_links
try:
    # Clear or initialize the model list_display_links
    for model_name in admin_models:
        admin_models[model_name].list_display_links = []
    # Add the fields to model list_display_links
    for item in AdminListDisplayLink.objects.filter(enabled=True).order_by(
            'model', 'order'):
        admin_models[item.model].list_display_links.append(item.field)
except OperationalError:
    # If the model AdminListDisplayLink doesn't yet exist skip the
    # customization
    pass
