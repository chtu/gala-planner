# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 20:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20170129_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_sponsor',
            field=models.BooleanField(default=False, verbose_name='is sponsor'),
        ),
    ]
