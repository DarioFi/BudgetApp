from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200621_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='User',
            name='last_login_action',
            field=models.DateTimeField(default=timezone.now)
        )
    ]
