# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-08-17 02:19
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkstay', '0055_auto_20181220_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='property_cache',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True),
        ),
    ]
