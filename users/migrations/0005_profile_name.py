# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-16 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160312_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
