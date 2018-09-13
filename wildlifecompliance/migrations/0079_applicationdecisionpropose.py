# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-11 06:02
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wildlifecompliance', '0078_auto_20180911_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationDecisionPropose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('default', 'Default'), ('propose_decline', 'Propose Decline'), ('declined', 'Declined'), ('propose_issue', 'Propose Issue'), ('issued', 'Issued')], default='default', max_length=20, verbose_name='Action')),
                ('reason', models.TextField(blank=True)),
                ('cc_email', models.TextField(null=True)),
                ('activity_type', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('proposed_start_date', models.DateField(blank=True, null=True)),
                ('proposed_end_date', models.DateField(blank=True, null=True)),
                ('is_activity_renewable', models.BooleanField(default=False)),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wildlifecompliance.Application')),
                ('licence_activity_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wildlifecompliance.WildlifeLicenceActivityType')),
                ('officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
