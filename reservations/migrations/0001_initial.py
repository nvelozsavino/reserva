# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(unique=True, null=True, verbose_name='Fecha del viaje')),
                ('qty', models.IntegerField(default=8, verbose_name='Cantidad de personas', validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('status', models.CharField(default=b'N', max_length=1, verbose_name='Status', choices=[(b'N', 'Pendiente'), (b'P', 'Pagado'), (b'C', 'Cancelado')])),
                ('value', models.FloatField(null=True, verbose_name='Precio', blank=True)),
                ('reservation_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de creaci\xf3n')),
                ('payment_date', models.DateTimeField(null=True, verbose_name='Fecha del pago', blank=True)),
                ('payment_confirmation', models.CharField(max_length=255, null=True, verbose_name='Confirmaci\xf3n de pago', blank=True)),
                ('qty_cut', models.IntegerField(default=8, verbose_name='Cantidad m\xednima de personas')),
                ('base_price', models.FloatField(default=2000, verbose_name='Precio m\xednimo')),
                ('extra_price', models.FloatField(default=250, verbose_name='Precio extra')),
                ('currency', models.CharField(default=b'USD', max_length=3, verbose_name='Moneda', choices=[(b'USD', 'USD')])),
                ('user', models.ForeignKey(verbose_name='Usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
