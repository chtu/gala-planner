# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 23:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_user_is_sponsor'),
        ('galasetter', '0004_auto_20170125_0546'),
    ]

    operations = [
        migrations.AddField(
            model_name='gala',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.User'),
        ),
    ]