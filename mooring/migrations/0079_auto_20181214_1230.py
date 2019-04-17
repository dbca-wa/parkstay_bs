# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-14 04:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mooring', '0078_auto_20181207_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmissionsLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrivalDate', models.DateField()),
                ('overnightStay', models.BooleanField(default=False)),
                ('cost', models.DecimalField(decimal_places=2, default='0.00', max_digits=8)),
            ],
        ),
        migrations.RemoveField(
            model_name='admissionsbooking',
            name='arrivalDate',
        ),
        migrations.RemoveField(
            model_name='admissionsbooking',
            name='overnightStay',
        ),
        migrations.AddField(
            model_name='admissionsline',
            name='admissionsBooking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mooring.AdmissionsBooking'),
        ),
    ]
