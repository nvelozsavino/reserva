# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='reservation_paid',
            new_name='paid',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_inscription_date',
            new_name='inscription_date',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_last_name',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='reservation_date',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='reservation_payment_confirmation',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='reservation_place',
        ),
        migrations.AddField(
            model_name='reservation',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='payment_confirmation',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='qty',
            field=models.IntegerField(default=8),
        ),
        migrations.DeleteModel(
            name='Place',
        ),
    ]
