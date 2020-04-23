# Generated by Django 3.0.3 on 2020-04-20 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CardGames', '0007_match_scopa_last_plays'),
    ]

    operations = [
        migrations.CreateModel(
            name='match_invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joining_id', models.TextField(max_length=20)),
                ('joining_passwd', models.TextField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='match_invitation',
            name='invited_user',
        ),
        migrations.RemoveField(
            model_name='match_invitation',
            name='match',
        ),
        migrations.RemoveField(
            model_name='match_invitation',
            name='sender_user',
        ),
        migrations.AlterField(
            model_name='match_scopa',
            name='players_amount',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='games_notification',
        ),
        migrations.DeleteModel(
            name='match_invitation',
        ),
        migrations.AddField(
            model_name='match_scopa',
            name='invite_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CardGames.match_invite'),
        ),
    ]