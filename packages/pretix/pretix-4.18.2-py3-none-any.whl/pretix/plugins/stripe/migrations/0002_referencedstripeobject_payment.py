# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-22 08:01
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0096_auto_20180722_0801'),
        ('stripe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referencedstripeobject',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pretixbase.OrderPayment'),
        ),
    ]
