# Generated by Django 3.1.6 on 2021-03-22 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Budgeting', '0011_categoryexpinc_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoryexpinc',
            old_name='exchange',
            new_name='balance',
        ),
    ]