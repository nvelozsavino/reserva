# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(unique=True, null=True, blank=True)),
                ('qty', models.IntegerField(default=8)),
                ('paid', models.BooleanField(default=False)),
                ('value', models.FloatField(null=True, blank=True)),
                ('reservation_date', models.DateTimeField(auto_now=True)),
                ('payment_date', models.DateTimeField(null=True, blank=True)),
                ('payment_confirmation', models.CharField(max_length=200, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
