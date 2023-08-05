# Generated by Django 3.2.17 on 2023-02-08 09:39

import django.core.serializers.json
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0229_invoice_payment_provider_stamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemvariation',
            name='checkin_attention',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='valid_if_pending',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='blocked',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='valid_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='valid_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='BlockedTicketSecret',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('secret', models.TextField(db_index=True)),
                ('blocked', models.BooleanField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_secrets', to='pretixbase.event')),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blocked_secrets', to='pretixbase.orderposition')),
            ],
            options={
                'unique_together': {('event', 'secret')},
            } if 'mysql' not in settings.DATABASES['default']['ENGINE'] else {}
        ),
    ]
