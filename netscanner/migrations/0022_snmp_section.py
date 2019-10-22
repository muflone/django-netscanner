# Generated by Django 2.2.5 on 2019-10-22 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netscanner', '0021_discovery_workers'),
    ]

    operations = [
        migrations.CreateModel(
            name='SNMPSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'SNMP Section',
                'verbose_name_plural': 'SNMP Sections',
                'db_table': 'netscanner_snmp_section',
                'ordering': ['name'],
            },
        ),
    ]
