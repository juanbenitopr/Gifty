# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 16:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20160316_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 3, 17, 16, 41, 26, 807000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
