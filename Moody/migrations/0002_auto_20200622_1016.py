# Generated by Django 3.0.7 on 2020-06-22 08:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Moody', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moody_record',
            name='data',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=15), null=True, size=None),
        ),
    ]
