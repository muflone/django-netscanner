# Generated by Django 2.2.5 on 2019-10-19 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netscanner', '0017_device_model_ordering'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscoveryResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('options', models.TextField(blank=True, verbose_name='options')),
                ('scan_datetime', models.DateTimeField(verbose_name='scan date and time')),
                ('results', models.TextField(blank=True, verbose_name='results')),
                ('discovery', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='netscanner.Discovery', verbose_name='discovery')),
            ],
            options={
                'verbose_name': 'Discovery result',
                'verbose_name_plural': 'Discovery results',
                'db_table': 'netscanner_discovery_result',
                'ordering': ['scan_datetime'],
            },
        ),
    ]
