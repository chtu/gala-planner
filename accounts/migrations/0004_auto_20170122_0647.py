# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=True, verbose_name='staff'),
        ),
    ]
