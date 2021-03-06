# Generated by Django 2.2.5 on 2019-10-15 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netscanner', '0005_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainMain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Domain main',
                'verbose_name_plural': 'Domains main',
                'db_table': 'netscanner_domain_main',
                'ordering': ['name'],
            },
        ),
    ]
