# Generated by Django 3.2.4 on 2021-10-27 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkstay', '0092_additionalbooking_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalbooking',
            name='fee_description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='additionalbooking',
            name='identifier',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]