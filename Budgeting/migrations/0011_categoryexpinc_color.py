# Generated by Django 3.0.7 on 2020-07-23 17:51

from django.db import migrations, models


def generate_colors(apps, schema_editor):
    palette = ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff', '#ff9f40', '#ff6384']
    categoryexpinc = apps.get_model('Budgeting', 'CategoryExpInc')
    categories = categoryexpinc.objects.all()
    for j in range(len(categories)):
        categories[j].color = palette[j % len(palette)]
        categories[j].save()


class Migration(migrations.Migration):
    dependencies = [
        ('Budgeting', '0010_auto_20200719_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryexpinc',
            name='color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
        migrations.RunPython(generate_colors)
    ]
