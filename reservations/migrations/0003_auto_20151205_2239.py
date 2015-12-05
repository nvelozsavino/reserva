# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_auto_20151129_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='base_price',
            field=models.FloatField(default=2000, verbose_name='Precio m\xednimo'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='currency',
            field=models.CharField(default=b'USD', max_length=3, verbose_name='Moneda', choices=[(b'USD', 'USD')]),
        ),
        migrations.AddField(
            model_name='reservation',
            name='extra_price',
            field=models.FloatField(default=250, verbose_name='Precio extra'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='qty_cut',
            field=models.IntegerField(default=8, verbose_name='Cantidad m\xednima de personas'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(unique=True, null=True, verbose_name='Fecha del viaje'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='payment_confirmation',
            field=models.CharField(max_length=255, null=True, verbose_name='Confirmaci\xf3n de pago', blank=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='payment_date',
            field=models.DateTimeField(null=True, verbose_name='Fecha del pago', blank=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='qty',
            field=models.IntegerField(default=8, verbose_name='Cantidad de personas'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de creaci\xf3n'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(default=b'N', max_length=1, verbose_name='Status', choices=[(b'N', 'Pendiente'), (b'P', 'Pagado'), (b'C', 'Cancelado')]),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(verbose_name='Usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='value',
            field=models.FloatField(null=True, verbose_name='Precio', blank=True),
        ),
    ]
