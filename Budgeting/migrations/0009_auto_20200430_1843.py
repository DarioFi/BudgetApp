# Generated by Django 3.0.5 on 2020-04-30 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Budgeting', '0008_account_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.TextField(max_length=30),
        ),
        migrations.AlterField(
            model_name='categoryexpinc',
            name='name',
            field=models.TextField(max_length=30),
        ),
    ]
