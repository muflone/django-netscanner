# Generated by Django 2.2.5 on 2019-10-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netscanner', '0019_discovery_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='discovery',
            name='timeout',
            field=models.PositiveIntegerField(default=0, verbose_name='timeout'),
        ),
    ]
