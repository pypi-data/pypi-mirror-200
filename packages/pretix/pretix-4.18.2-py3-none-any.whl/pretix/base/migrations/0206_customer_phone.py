# Generated by Django 3.2.9 on 2022-01-12 10:59

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0205_itemvariation_require_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
    ]
