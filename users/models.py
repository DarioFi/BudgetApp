from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, UserManager, \
    UnicodeUsernameValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'auth_user'

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # last_login_action = models.DateTimeField(_('last login action'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # test_field = models.BooleanField(null=False, default=False)

    @property
    def is_authenticated(self):
        """
        Always return True because of instantiation system
        It's an override because i need to add a last_action field
        @return: True
        """
        # self.last_login_action = timezone.now()
        # self.save()

        return True


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# todo: last login or action

# C:\Users\Dario>heroku config:get TRUSTIFI_SECRET -a=filabudget
# e15cea8651c455a6fb1f38c9c2879c78
#
# C:\Users\Dario>heroku config:get TRUSTIFI_URL -a=filabudget
# https://be.trustifi.com
#
# C:\Users\Dario>heroku config:get TRUSTIFI_KEY -a=filabudget
# fca0f2650a486c9500ee6dbe0c4d4310c664f79390c1e54f
