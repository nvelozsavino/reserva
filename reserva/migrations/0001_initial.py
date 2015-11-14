# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reservation_date', models.DateTimeField()),
                ('reservation_paid', models.BooleanField(default=False)),
                ('reservation_payment_confirmation', models.CharField(max_length=200)),
                ('reservation_place', models.ForeignKey(to='reserva.Place')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=200)),
                ('user_last_name', models.CharField(max_length=200)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_inscription_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(to='reserva.User'),
        ),
    ]
