# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 22:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_invite_gala_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invite',
            old_name='num_tables',
            new_name='table_size',
        ),
    ]
