# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 17:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_likesuser_user'),
        ('gifts', '0007_list_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeGiftProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gifts.Gift')),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gifts.List')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
        ),
    ]
