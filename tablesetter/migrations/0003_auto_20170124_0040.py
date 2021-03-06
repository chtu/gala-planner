# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 00:40
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0008_auto_20170122_2030'),
        ('tablesetter', '0002_auto_20170122_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gala',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gala_name', models.CharField(max_length=100)),
                ('gala_datetime', models.DateTimeField(verbose_name='event date')),
                ('gala_num_tables', models.IntegerField()),
                ('gala_total_guests', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_first_name', models.CharField(max_length=50, null=True)),
                ('guest_last_name', models.CharField(max_length=50, null=True)),
                ('guest_email', models.EmailField(max_length=200, null=True)),
                ('has_replied', models.BooleanField(default=False)),
                ('dietary_restrictions', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_size', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('gala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tablesetter.Gala')),
                ('table_sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User')),
            ],
        ),
        migrations.AddField(
            model_name='guest',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tablesetter.Table'),
        ),
    ]
