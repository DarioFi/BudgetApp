# Generated by Django 3.0.5 on 2020-04-27 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CardGames', '0009_auto_20200420_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='match_against_AI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1_hand', models.TextField(blank=True, max_length=22, null=True)),
                ('ai_hand', models.TextField(blank=True, max_length=22, null=True)),
                ('player1_points', models.IntegerField(blank=True, default=0, null=True)),
                ('ai_points', models.IntegerField(blank=True, default=0, null=True)),
                ('player1_takes', models.TextField(blank=True, max_length=81, null=True)),
                ('ai_takes', models.TextField(blank=True, max_length=81, null=True)),
                ('player1_scope', models.IntegerField(blank=True, default=0, null=True)),
                ('ai_scope', models.IntegerField(blank=True, default=0, null=True)),
                ('last_plays', models.TextField(blank=True, max_length=300, null=True)),
                ('ground', models.TextField(blank=True, max_length=22, null=True)),
                ('deck', models.TextField(blank=True, max_length=82, null=True)),
                ('last_used_on', models.DateField(default=django.utils.datetime_safe.datetime.now)),
                ('last_player_to_take', models.IntegerField(default=0)),
                ('is_started_game', models.BooleanField(default=False)),
                ('player', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
