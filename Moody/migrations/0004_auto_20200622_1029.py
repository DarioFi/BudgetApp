# Generated by Django 3.0.7 on 2020-06-22 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Moody', '0003_auto_20200622_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moody_record',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='moody_user', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]