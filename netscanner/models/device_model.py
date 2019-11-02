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

from django.db import models
from django.utils.safestring import mark_safe, SafeText
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class DeviceModel(BaseModel):
    device_type = models.ForeignKey('DeviceType',
                                    on_delete=models.PROTECT,
                                    verbose_name=pgettext_lazy('DeviceModel',
                                                               'device type'))
    brand = models.ForeignKey('Brand',
                              on_delete=models.PROTECT,
                              verbose_name=pgettext_lazy('DeviceModel',
                                                         'brand'))
    name = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('DeviceModel',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('DeviceModel',
                                                              'description'))
    image = models.ImageField(null=True,
                              blank=True,
                              upload_to='models/',
                              verbose_name=pgettext_lazy('DeviceModel',
                                                         'image'))

    class Meta:
        # Define the database table
        db_table = 'netscanner_device_model'
        ordering = ['brand', 'name']
        unique_together = ('brand', 'name')
        verbose_name = pgettext_lazy('DeviceModel', 'Device model')
        verbose_name_plural = pgettext_lazy('DeviceModel', 'Device models')

    def __str__(self):
        return '{BRAND} {NAME}'.format(BRAND=self.brand,
                                       NAME=self.name)


class DeviceModelAdmin(BaseModelAdmin):
    class Media:
        # Add custom CSS for images
        css = {
            'all': ('admin/css/device_model.css',)
        }

    def brand_thumbnail(self,
                        instance: DeviceModel) -> SafeText:
        """
        Show Brand image
        :param instance: DeviceModel object containing the image
        :return: SafeText object with the HTML text
        """
        if instance.brand.image.name:
            url_image = instance.brand.image.url
            return mark_safe('<a href="{image}" target="_blank">'
                             '<img class="device_model_image"'
                             ' src="{image}" />'
                             '</a>'.format(image=url_image))
    brand_thumbnail.short_description = pgettext_lazy('DeviceModel',
                                                      'Brand Image')

    def image_thumbnail(self,
                        instance: DeviceModel) -> SafeText:
        """
        Show image
        :param instance: DeviceModel object containing the image
        :return: SafeText object with the HTML text
        """
        if instance.image.name:
            url_image = instance.image.url
            return mark_safe('<a href="{image}" target="_blank">'
                             '<img class="device_model_image"'
                             ' src="{image}" />'
                             '</a>'.format(image=url_image))
    image_thumbnail.short_description = pgettext_lazy('DeviceModel', 'Image')
