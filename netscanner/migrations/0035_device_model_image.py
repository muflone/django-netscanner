# Generated by Django 2.2.5 on 2019-11-02 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netscanner', '0034_host_snmp_version_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicemodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='models/', verbose_name='image'),
        ),
    ]
