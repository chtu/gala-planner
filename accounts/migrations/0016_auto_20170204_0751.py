# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 07:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20170204_0654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invite',
            old_name='invite_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='invite',
            old_name='invite_complete',
            new_name='complete',
        ),
        migrations.RenameField(
            model_name='invite',
            old_name='invite_num_tables',
            new_name='num_tables',
        ),
    ]
