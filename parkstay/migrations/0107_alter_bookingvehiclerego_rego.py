# Generated by Django 3.2.4 on 2021-12-03 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkstay', '0106_auto_20211201_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingvehiclerego',
            name='rego',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]