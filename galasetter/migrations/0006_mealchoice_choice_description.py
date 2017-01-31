# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 05:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galasetter', '0005_gala_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealchoice',
            name='choice_description',
            field=models.CharField(default='default description', max_length=500, verbose_name='meal description'),
            preserve_default=False,
        ),
    ]
