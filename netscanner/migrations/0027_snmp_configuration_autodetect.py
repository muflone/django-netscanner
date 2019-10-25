# Generated by Django 2.2.5 on 2019-10-25 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netscanner', '0026_host_snmp_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='snmpconfiguration',
            name='autodetect',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='snmp_configuration_autodetect', to='netscanner.SNMPValue', verbose_name='Autodetect'),
        ),
        migrations.AddField(
            model_name='snmpconfiguration',
            name='autodetect_value',
            field=models.CharField(blank=True, max_length=255, verbose_name='Autodetect value'),
        ),
    ]
