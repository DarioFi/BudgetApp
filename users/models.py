from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'




@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


