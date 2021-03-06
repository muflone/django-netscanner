# Generated by Django 2.2.5 on 2019-11-02 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netscanner', '0032_brand_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='SNMPVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('version', models.PositiveSmallIntegerField(verbose_name='version')),
            ],
            options={
                'verbose_name': 'SNMP Version',
                'verbose_name_plural': 'SNMP Versions',
                'db_table': 'netscanner_snmp_version',
                'ordering': ['name'],
            },
        ),
    ]
