# Generated by Django 3.2.10 on 2021-12-19 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkstay', '0113_auto_20211216_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='campgroundnotice',
            name='order',
            field=models.IntegerField(choices=[(0, 'Red Warning'), (1, 'Orange Warning'), (2, 'Blue Warning')], default=1),
        ),
    ]