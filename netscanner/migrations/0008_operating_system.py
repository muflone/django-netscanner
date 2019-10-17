# Generated by Django 2.2.5 on 2019-10-15 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netscanner', '0007_domain'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('version', models.CharField(max_length=255, verbose_name='version')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='netscanner.Brand', verbose_name='brand')),
            ],
            options={
                'verbose_name': 'Operating System',
                'verbose_name_plural': 'Operating Systems',
                'db_table': 'netscanner_operating_system',
                'ordering': ['brand', 'name', 'version'],
                'unique_together': {('brand', 'name', 'version')},
            },
        ),
    ]