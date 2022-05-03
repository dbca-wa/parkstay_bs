# Generated by Django 3.2.4 on 2021-11-29 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkstay', '0100_parkstaypermission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parkstaypermission',
            name='emailuser_id',
        ),
        migrations.AddField(
            model_name='parkstaypermission',
            name='email',
            field=models.CharField(default='jason.moore@dbca.wa.gov.au', max_length=300),
            preserve_default=False,
        ),
    ]