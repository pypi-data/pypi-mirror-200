# Generated by Django 2.1.5 on 2019-02-19 12:45

import django.db.models.deletion
from django.db import migrations, models

import pretix.base.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0109_auto_20190208_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='plugins',
            field=models.TextField(blank=True, default='', verbose_name='Plugins'),
            preserve_default=False,
        ),
    ]
