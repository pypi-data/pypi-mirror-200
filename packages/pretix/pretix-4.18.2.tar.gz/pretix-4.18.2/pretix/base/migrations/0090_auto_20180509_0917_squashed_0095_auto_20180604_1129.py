# Generated by Django 2.0.8 on 2018-09-11 14:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.crypto import get_random_string


def set_pids(apps, schema_editor):
    OrderPosition = apps.get_model('pretixbase', 'OrderPosition')  # noqa
    taken = set()
    charset = list('ABCDEFGHJKLMNPQRSTUVWXYZ3789')
    for op in OrderPosition.objects.iterator():
        while True:
            code = get_random_string(length=10, allowed_chars=charset)
            if code not in taken:
                op.pseudonymization_id = code
                taken.add(code)
                break
        op.save(update_fields=['pseudonymization_id'])


class Migration(migrations.Migration):
    replaces = [('pretixbase', '0090_auto_20180509_0917'), ('pretixbase', '0091_auto_20180513_1641'),
                ('pretixbase', '0092_auto_20180511_1224'), ('pretixbase', '0093_auto_20180528_1432'),
                ('pretixbase', '0094_auto_20180604_1119'), ('pretixbase', '0095_auto_20180604_1129')]

    dependencies = [
        ('pretixbase', '0089_auto_20180315_1322'),
        ('pretixapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='internal_name',
            field=models.CharField(blank=True,
                                   help_text='If you set this, this will be used instead of the public name in the '
                                             'backend.',
                                   max_length=255, null=True, verbose_name='Internal name'),
        ),
        migrations.AddField(
            model_name='itemcategory',
            name='internal_name',
            field=models.CharField(blank=True,
                                   help_text='If you set this, this will be used instead of the public name in the '
                                             'backend.',
                                   max_length=255, null=True, verbose_name='Internal name'),
        ),
        migrations.AddField(
            model_name='order',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AddField(
            model_name='item',
            name='original_price',
            field=models.DecimalField(blank=True, decimal_places=2,
                                      help_text='If set, this will be displayed next to the current price to show '
                                                'that the current price is a discounted one. This is just a cosmetic '
                                                'setting and will not actually impact pricing.',
                                      max_digits=7, null=True, verbose_name='Original price'),
        ),
        migrations.AddField(
            model_name='orderposition',
            name='pseudonymization_id',
            field=models.CharField(db_index=True, max_length=16, null=True, unique=True),
        ),
        migrations.RunPython(
            code=set_pids,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='orderposition',
            name='pseudonymization_id',
            field=models.CharField(db_index=True, default='', max_length=16, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='logentry',
            name='oauth_application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to=settings.OAUTH2_PROVIDER_APPLICATION_MODEL),
        ),
    ]
