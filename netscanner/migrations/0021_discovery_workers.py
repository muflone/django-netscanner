# Generated by Django 2.2.5 on 2019-10-21 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netscanner', '0020_discovery_timeout'),
    ]

    operations = [
        migrations.AddField(
            model_name='discovery',
            name='workers',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='workers'),
        ),
    ]