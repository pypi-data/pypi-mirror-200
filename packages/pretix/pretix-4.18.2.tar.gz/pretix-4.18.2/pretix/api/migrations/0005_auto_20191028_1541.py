# Generated by Django 2.2.1 on 2019-10-28 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixapi', '0004_auto_20190405_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauthgrant',
            name='redirect_uri',
            field=models.CharField(max_length=2500),
        ),
    ]
