# Generated by Django 3.0.5 on 2020-04-23 17:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Budgeting', '0007_auto_20200328_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]