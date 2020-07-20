# Generated by Django 3.0.7 on 2020-07-06 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown name', max_length=30)),
                ('created_on', models.DateField(auto_now=True)),
                ('join_slug', models.SlugField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Players_room_m2m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.GameRoom')),
            ],
        ),
        migrations.AddField(
            model_name='gameroom',
            name='players',
            field=models.ManyToManyField(through='games.Players_room_m2m', to=settings.AUTH_USER_MODEL),
        ),
    ]