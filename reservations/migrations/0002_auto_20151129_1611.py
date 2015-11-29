# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='paid',
        ),
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(default=b'N', max_length=1),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(unique=True, null=True),
        ),
    ]
