# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 01:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20170124_0114'),
        ('tablesetter', '0004_auto_20170124_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.User'),
        ),
    ]