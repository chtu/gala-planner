# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 17:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tablesetter', '0008_auto_20170131_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='table_sponsor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.User'),
        ),
    ]
